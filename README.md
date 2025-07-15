JUST-AI: AI-Powered Hate Speech Detection

JUST-AI is a multi-modal content moderation tool that detects caste-based hate speech in user-generated content. It uses a combination of machine learning models and rule-based logic to analyze text, images, and video content. The system was developed as a student innovation project to support anti-discrimination efforts using responsible AI.

Key Features:
Text Moderation
Detects hate speech and offensive content using pre-trained BERT-based models.
Also includes emotion detection to provide additional context.

Image Moderation
Extracts and analyzes text from uploaded images using OCR (Tesseract).
Supports basic visual content analysis using OpenAI’s CLIP model to detect categories like abuse, violence, and nudity.

Video Moderation
Extracts text from selected frames in short videos and analyzes it for hate speech.
Helps flag harmful content in reels, stories, and user-uploaded clips.

Twitter Scraper (Optional)
Scrapes tweets from public accounts and runs hate speech detection on the content.
Built as a CLI feature; can be integrated into the UI in future updates.

Technology Stack:
Python 3.10,
Streamlit (for the user interface),
HuggingFace Transformers (for text classification),
OpenCV and PIL (for image/video processing),
Tesseract OCR (for text extraction),
Git LFS (for handling large model files).

