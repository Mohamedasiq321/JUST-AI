from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from .moderation_utils import analyze_text, extract_text_from_image, extract_text_from_video
import traceback  # ← Add this

app = FastAPI()

@app.post("/analyze/text")
def analyze_text_route(text: str = Form(...)):
    try:
        print(f"Received text: {text}")  # Log input
        result = analyze_text(text)
        print(f"Analysis result: {result}")  # Log output
        return {"result": result}
    except Exception as e:
        traceback.print_exc()  # ← Print full error
        return JSONResponse(status_code=500, content={"error": str(e)})
