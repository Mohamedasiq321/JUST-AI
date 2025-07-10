import os
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from PIL import Image
import pytesseract
import cv2
import tempfile

# --- Device Config ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- Load Models ---
emotion_model = pipeline(
    "text-classification",
    model=AutoModelForSequenceClassification.from_pretrained("bhadresh-savani/bert-base-uncased-emotion").to(device),
    tokenizer=AutoTokenizer.from_pretrained("bhadresh-savani/bert-base-uncased-emotion"),
    device=device.index if torch.cuda.is_available() else -1
)

intent_model = pipeline(
    "text-classification",
    model=AutoModelForSequenceClassification.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain").to(device),
    tokenizer=AutoTokenizer.from_pretrained("Hate-speech-CNERG/bert-base-uncased-hatexplain"),
    device=device.index if torch.cuda.is_available() else -1
)

clip_model = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")

# --- Phrase Checks ---
hate_phrases = [
    "you people are inferior",
    "rape dalit",
    "kill the dalits",
    "ban sc/st",
    "caste is curse",
    "sc st dogs",
    "burn the reservation"
]

positive_phrases = [
    "equality for all",
    "treat them equally",
    "support reservation",
    "break caste barriers",
    "every life matters"
]

# --- Utilities ---
def clean_text(text): return text.lower().strip()

def hybrid_hate_check(text):
    text = clean_text(text)
    for phrase in hate_phrases:
        if phrase in text:
            return True, phrase
    return False, None

def hybrid_positive_check(text):
    text = clean_text(text)
    for phrase in positive_phrases:
        if phrase in text:
            return True, phrase
    return False, None

def enhanced_check_intent(output):
    if not output or not isinstance(output, list):
        return "unknown", {}
    scores = {o['label'].lower(): o['score'] for o in output if 'label' in o and 'score' in o}
    if not scores:
        return "unknown", {}
    top_label = max(scores, key=scores.get)
    if top_label == "normal" and scores["normal"] < 0.65:
        alt_scores = {k: v for k, v in scores.items() if k != "normal"}
        if alt_scores:
            top_label = max(alt_scores, key=alt_scores.get)
        else:
            return "normal", scores
    return top_label, scores

def analyze_text(text):
    text = clean_text(text)
    matched_hate, hate_phrase = hybrid_hate_check(text)
    matched_positive, pos_phrase = hybrid_positive_check(text)
    emotion = emotion_model(text)[0]["label"]
    intent_output = intent_model(text)
    intent_label, intent_scores = enhanced_check_intent(intent_output)

    flagged = False
    reasons = []

    if matched_hate:
        flagged = True
        reasons.append(f"🚨 Template Match: '{hate_phrase}'")

    if intent_label != "normal" and intent_scores.get(intent_label, 0) > 0.65:
        flagged = True
        reasons.append(f"🔍 ML Intent: {intent_label.upper()} ({intent_scores[intent_label]:.2f})")
        reasons.append(f"🎭 Emotion: {emotion}")

    if matched_positive:
        reasons.append(f"🌟 Positive Phrase: '{pos_phrase}'")

    return flagged, emotion, intent_label, intent_scores, reasons

def extract_text_from_image(image_file):
    img = Image.open(image_file)
    return pytesseract.image_to_string(img)

def extract_text_from_video(video_file, frame_skip=15, max_frames=5):
    path = os.path.join(tempfile.gettempdir(), "temp_video.mp4")
    with open(path, "wb") as f:
        f.write(video_file.read())
    cap = cv2.VideoCapture(path)
    result, count, processed = [], 0, 0
    while cap.isOpened() and processed < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_skip == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ocr = pytesseract.image_to_string(Image.fromarray(gray))
            if ocr.strip():
                result.append(ocr.strip())
                processed += 1
        count += 1
    cap.release()
    return "\n".join(result)
