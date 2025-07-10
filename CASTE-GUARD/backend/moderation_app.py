import os
import torch
import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from PIL import Image
import pytesseract
import tempfile
import cv2
import datetime

# --- Configuration ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["USE_TF"] = "0"
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# --- Load Models ---
@st.cache_resource
def load_models():
    try:
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
        clip_pipe = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")
        return emotion_pipe, intent_pipe, clip_pipe
    except Exception as e:
        st.error(f"Error loading models: {e}")
        raise

emotion_model, intent_model, clip_model = load_models()

# --- Phrase Templates ---
hate_phrases = [
    "you people are inferior", "are shit eaters", "are pigs", "are dogs", " they are pigs" ," they are dogs ", "dont let them live", "are frauds", "are criminals", "dont deserves respect",
    "dalits are theives", "are pigs", "let dalits eat our shit", "dont respect", "rape sc", "rape dalit",
    "are filths", "fuck dalits", "are untouchables", "hate dalits", "should be killed", "lower caste",
    "dalit dogs", "ban sc/st", "scs don't deserve", "wipe out dalits", "stop reservation"
]
positive_phrases = [
    "equality for all", "not dogs", "not pigs", "make peace", "respect them", "treat them equally", "are equal", "support equality",
    "dont hate dalits", "deserves education", "we are all humans", "inclusive society", "diversity is beautiful",
    "end caste system", "unity is strength", "love wins", "equal rights"
]

# --- Utility Functions ---
def clean_text(text):
    return text.lower().strip()

def hybrid_check(text, phrases):
    text = clean_text(text)
    for phrase in phrases:
        if phrase in text:
            return True, phrase
    return False, None

def enhanced_check_intent(output):
    try:
        scores = {o['label'].lower(): o['score'] for o in output}
        top_label = max(scores, key=scores.get)
        if top_label == "normal" and scores["normal"] < 0.65:
            alt_scores = {k: v for k, v in scores.items() if k != "normal"}
            if alt_scores:
                top_label = max(alt_scores, key=alt_scores.get)
        return top_label, scores
    except:
        return "unknown", {}

def analyze_text(text):
    try:
        text = clean_text(text)
        matched_hate, hate_phrase = hybrid_check(text, hate_phrases)
        matched_positive, pos_phrase = hybrid_check(text, positive_phrases)
        emotion = emotion_model(text)[0]["label"]
        intent_output = intent_model(text)
        intent_label, intent_scores = enhanced_check_intent(intent_output)

        flagged, reasons = False, []

        if matched_hate:
            flagged = True
            reasons.append(f"**Template Match:** '{hate_phrase}' found")

        if intent_label != "normal" and intent_scores.get(intent_label, 0) > 0.65:
            flagged = True
            reasons.append(f"**ML Prediction:** Intent - {intent_label.upper()} ({intent_scores[intent_label]:.2f})")
            reasons.append(f"**Emotion:** {emotion}")

        if matched_positive:
            reasons.append(f"**Positive Sentiment:** '{pos_phrase}' found")

        return flagged, emotion, intent_label, intent_scores, reasons
    except Exception as e:
        return False, "unknown", "unknown", {}, [f"Error during analysis: {e}"]

def extract_ocr_from_image(img):
    try:
        return pytesseract.image_to_string(img)
    except Exception as e:
        return f"Error in OCR: {e}"

def extract_text_from_video(file, frame_skip=15, max_frames=5):
    try:
        path = os.path.join(tempfile.gettempdir(), "temp_video.mp4")
        with open(path, "wb") as f:
            f.write(file.read())
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
    except Exception as e:
        return f"Error processing video: {e}"

# --- Streamlit UI ---
st.title("🛡 JUST-AI 2.0 - Social Media Filter")
username = st.text_input("Enter your name:")
text = st.text_area("Write your post below:")
image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])
video = st.file_uploader("Upload a video (optional)", type=["mp4", "mov", "avi", "mpeg"])

# --- Moderation Logic ---
if st.button("Submit"):
    st.subheader("🔍 Moderation Results")
    flagged = False
    all_reasons = []

    # --- Text ---
    if text:
        caste_flag, emotion, intent, intent_scores, reasons = analyze_text(text)
        with st.expander("📝 Text Analysis"):
            st.write(f"**Input Text:** {text}")
            st.write(f"**Emotion:** {emotion}")
            st.write(f"**Intent:** {intent}")
            st.write(f"**Scores:** {intent_scores}")
        if caste_flag:
            flagged = True
            all_reasons.extend(reasons)
        else:
            st.success(f"✅ No hate detected. Emotion: {emotion}, Intent: {intent}")

    # --- Image ---
    if image:
        try:
            img = Image.open(image)
            ocr_text = extract_ocr_from_image(img)
            caste_flag, emotion, intent, intent_scores, reasons = analyze_text(ocr_text)
            with st.expander("🖼️ Image OCR Analysis"):
                st.write(f"**Extracted Text:** {ocr_text}")
                st.write(f"**Emotion:** {emotion}")
                st.write(f"**Intent:** {intent}")
                st.write(f"**Scores:** {intent_scores}")
            if caste_flag:
                flagged = True
                all_reasons.extend(reasons)

            clip_results = clip_model(img, candidate_labels=["nudity", "abuse", "violence", "normal"])
            top_clip = clip_results[0]
            with st.expander("🧠 CLIP Visual Scan"):
                for r in clip_results:
                    st.write(f"{r['label']} - {r['score']:.2f}")
            if top_clip["label"] != "normal" and top_clip["score"] > 0.7:
                flagged = True
                all_reasons.append(f"**CLIP Alert:** {top_clip['label']} ({top_clip['score']:.2f})")
        except Exception as e:
            st.error(f"Error processing image: {e}")

    # --- Video ---
    if video:
        vtext = extract_text_from_video(video)
        if vtext.strip():
            caste_flag, emotion, intent, intent_scores, reasons = analyze_text(vtext)
            with st.expander("🎥 Video OCR Analysis"):
                st.write(f"**Extracted Text:** {vtext}")
                st.write(f"**Emotion:** {emotion}")
                st.write(f"**Intent:** {intent}")
                st.write(f"**Scores:** {intent_scores}")
            if caste_flag:
                flagged = True
                all_reasons.extend(reasons)

    # --- Final Verdict ---
    if flagged:
        st.error("⚠️ Post flagged for review.")
        for reason in all_reasons:
            st.write(f"🔸 {reason}")
    else:
        st.success("✅ Post approved!")
        st.markdown(f"👤 **{username}** posted at **{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**")
        if text:
            st.markdown(f"✍️ _{text}_")
        if image:
            st.image(img, caption="Uploaded Image", use_column_width=True)
        if video:
            st.video(video)
