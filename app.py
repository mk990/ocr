from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
from ocr_engine import create_ocr
import tempfile
import threading
import os

app = FastAPI(title="Invoice OCR Service")

ocr = create_ocr()

# PaddleOCR is not thread-safe; serialize inference
ocr_lock = threading.Lock()


def run_ocr(path: str):
    with ocr_lock:
        return [res.json for res in ocr.predict(path)]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "paddleocr"
    }


@app.post("/ocr")
async def process_ocr(file: UploadFile = File(...)):

    allowed = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/pdf": ".pdf",
    }

    if file.content_type not in allowed:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    suffix = allowed[file.content_type]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp:

        content = await file.read()
        temp.write(content)
        temp_path = temp.name

    try:
        output = await run_in_threadpool(run_ocr, temp_path)

        return {
            "success": True,
            "filename": file.filename,
            "pages": output
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
