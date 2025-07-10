from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from PIL import Image
import pytesseract
import tempfile
import torch
import os
import cv2
import shutil

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from datetime import datetime

router = APIRouter()

# Environment Setup
os.environ["TRANSFORMERS_NO_TF"] = "1"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Models & Pipelines
emotion_pipe = pipeline(
    "text-classification",
    model=AutoModelForSequenceClassification.from_pretrained("bhadresh-savani/bert-base-uncased-emotion").to(device),
    tokenizer=AutoTokenizer.from_pretrained("bhadresh-savani/bert-base-uncased-emotion"),
    device=device.index if torch.cuda.is_available() else -1
)

intent_pipe = pipeline(
    "text-classification",
    model=AutoModelForSequenceClassification.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain").to(device),
    tokenizer=AutoTokenizer.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain"),
    device=device.index if torch.cuda.is_available() else -1
)

# Caste-based hate templates
caste_templates = [
    "you people are inferior", "lower caste", "dalit dogs", "ban sc/st",
    "no reservation", "dirty caste", "brahmins are superior", "destroy quota",
    "kill the dalits", "hate sc", "hate st", "hate obc"
]

# Request body for text
class TextRequest(BaseModel):
    username: str
    text: str

# Text preprocessing
def clean_text(text):
    return text.lower().strip()

# Template match check
def hybrid_check(text):
    text = clean_text(text)
    for phrase in caste_templates:
        if phrase in text:
            return True, phrase
    return False, None

# Intent analysis
def check_intent(output):
    if not output:
        return "unknown", {}
    scores = {x['label'].lower(): x['score'] for x in output}
    top = max(scores, key=scores.get)
    if top == "normal" and scores[top] < 0.6:
        scores.pop("normal", None)
        if scores:
            top = max(scores, key=scores.get)
    return top, scores

# Text analyzer
def analyze_text(text):
    flagged, matched = hybrid_check(text)
    emotion = emotion_pipe(text)[0]['label']
    intent_output = intent_pipe(text)
    intent, scores = check_intent(intent_output)

    reasons = []
    if flagged:
        reasons.append(f"Matched template: {matched}")
    if intent != "normal" and scores.get(intent, 0) > 0.65:
        flagged = True
        reasons.append(f"Intent: {intent} ({scores[intent]:.2f})")
    if flagged:
        reasons.append(f"Emotion: {emotion}")

    return flagged, emotion, intent, scores, reasons

# Image OCR
def extract_text_from_image(upload_file):
    try:
        image = Image.open(upload_file.file).convert("RGB")
        return pytesseract.image_to_string(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Image reading failed")

# Video OCR
def extract_text_from_video(video_file, skip=15, max_frames=5):
    try:
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, "temp_video.mp4")
        with open(temp_path, "wb") as f:
            f.write(video_file.file.read())

        cap = cv2.VideoCapture(temp_path)
        texts, count, processed = [], 0, 0
        while cap.isOpened() and processed < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            if count % skip == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(Image.fromarray(gray)).strip()
                if text:
                    texts.append(text)
                    processed += 1
            count += 1
        cap.release()
        shutil.rmtree(temp_dir)
        return "\n".join(texts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video processing failed: {str(e)}")

# Logging utility
def build_log(username, source_type, original_text, flagged, emotion, intent, scores, reasons):
    return {
        "username": username,
        "source_type": source_type,
        "original_text": original_text,
        "flagged": flagged,
        "emotion": emotion,
        "intent": intent,
        "scores": scores,
        "reasons": reasons,
        "created_at": datetime.utcnow()
    }

# API Routes

@router.post("/analyze/text")
async def analyze_text_api(request: Request, body: TextRequest):
    flagged, emotion, intent, scores, reasons = analyze_text(body.text)

    log = build_log(
        username=body.username,
        source_type="text",
        original_text=body.text,
        flagged=flagged,
        emotion=emotion,
        intent=intent,
        scores=scores,
        reasons=reasons
    )
    await request.app.state.mongo.AnalysisLogs.insert_one(log)

    return {
        "input": body.text,
        "flagged": flagged,
        "emotion": emotion,
        "intent": intent,
        "scores": scores,
        "reasons": reasons
    }

@router.post("/analyze/image")
async def analyze_image_api(request: Request, username: str = Form(...), image: UploadFile = File(...)):
    ocr_text = extract_text_from_image(image)
    flagged, emotion, intent, scores, reasons = analyze_text(ocr_text)

    log = build_log(
        username=username,
        source_type="image",
        original_text=ocr_text,
        flagged=flagged,
        emotion=emotion,
        intent=intent,
        scores=scores,
        reasons=reasons
    )
    await request.app.state.mongo.AnalysisLogs.insert_one(log)

    return {
        "ocr_text": ocr_text,
        "flagged": flagged,
        "emotion": emotion,
        "intent": intent,
        "scores": scores,
        "reasons": reasons
    }

@router.post("/analyze/video")
async def analyze_video_api(request: Request, username: str = Form(...), video: UploadFile = File(...)):
    ocr_text = extract_text_from_video(video)
    flagged, emotion, intent, scores, reasons = analyze_text(ocr_text)

    log = build_log(
        username=username,
        source_type="video",
        original_text=ocr_text,
        flagged=flagged,
        emotion=emotion,
        intent=intent,
        scores=scores,
        reasons=reasons
    )
    await request.app.state.mongo.AnalysisLogs.insert_one(log)

    return {
        "ocr_text": ocr_text,
        "flagged": flagged,
        "emotion": emotion,
        "intent": intent,
        "scores": scores,
        "reasons": reasons
    }
