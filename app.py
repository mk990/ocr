from fastapi import FastAPI, UploadFile, File, HTTPException
from paddleocr import PaddleOCR
import tempfile
import os

app = FastAPI(title="Invoice OCR Service")

ocr = PaddleOCR(
    lang="fa",
    device="cpu",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "paddleocr"
    }


@app.post("/ocr")
async def process_ocr(file: UploadFile = File(...)):

    allowed = {
        "image/jpeg",
        "image/png",
        "application/pdf"
    }

    if file.content_type not in allowed:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp:

        content = await file.read()
        temp.write(content)
        temp_path = temp.name

    try:
        result = ocr.predict(temp_path)

        output = []

        for res in result:
            data = res.json

            output.append(data)

        return {
            "success": True,
            "filename": file.filename,
            "pages": output
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
