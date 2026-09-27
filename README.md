# Invoice OCR Service

HTTP service that extracts Persian (`fa`) text from invoice images and PDFs using [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) on CPU.

## Run

The image is built and published to GitHub Container Registry by GitHub Actions — nothing needs to be built locally.

```bash
docker run -d -p 8000:8000 ghcr.io/<owner>/<repo>:latest
```

The OCR models are baked into the image, so the container starts without internet access.

## API

Interactive docs are at `http://localhost:8000/docs`.

### `GET /health`

```json
{ "status": "ok", "service": "paddleocr" }
```

### `POST /ocr`

Upload one file as multipart form field `file`. Accepted types: `image/jpeg`, `image/png`, `application/pdf`.

```bash
curl -F "file=@invoice.jpg" http://localhost:8000/ocr
```

Response — one entry in `pages` per image or PDF page, each being PaddleOCR's JSON result (recognized texts in `res.rec_texts`, confidence in `res.rec_scores`, boxes in `res.rec_boxes`):

```json
{
  "success": true,
  "filename": "invoice.jpg",
  "pages": [ { "res": { "rec_texts": ["..."], "rec_scores": [0.98], "...": "..." } } ]
}
```

Unsupported file types return `400`. Requests are processed one at a time; others wait in line.

## Image tags

Published by `.github/workflows/docker-publish.yml`:

| Trigger | Tags |
|---|---|
| Push to `main` / `master` | `latest`, branch name, `sha-<short>` |
| Push tag `v1.2.3` | `1.2.3`, `sha-<short>` |
| Manual run (Actions tab) | same as a push to the selected branch |

New packages on GHCR are private — make it public in the package settings, or `docker login ghcr.io` before pulling.

## Project layout

| File | Purpose |
|---|---|
| `app.py` | FastAPI app and endpoints |
| `ocr_engine.py` | PaddleOCR configuration; also run at build time to download models |
| `Dockerfile` | CPU image (PaddlePaddle 3.2.0, Python 3.11) |
| `requirements.txt` | Pinned Python dependencies |
