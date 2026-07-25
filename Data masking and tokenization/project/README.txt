Data Masking & Tokenization System

Features:
- Secure file upload (CSV format)
- Automatic Data Masking for names (e.g., Ah*****)
- Secure Data Tokenization for emails (using UUIDs)
- Automatic processed file download
- Archiving original and processed files

How to Run:
1. pip install fastapi uvicorn pandas python-multipart
2. uvicorn main:app --reload
3. Open browser: http://127.0.0.1:8000