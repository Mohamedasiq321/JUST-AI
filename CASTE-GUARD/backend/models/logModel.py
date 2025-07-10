# models/logModel.py

from datetime import datetime

def create_log_doc(username, source_type, original_text, flagged, emotion, intent, scores, reasons):
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
