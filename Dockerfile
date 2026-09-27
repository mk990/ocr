FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgomp1 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    paddlepaddle==3.2.0 \
    -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Models are cached in the image; skip the hoster check on startup
ENV PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True

COPY ocr_engine.py .

RUN python ocr_engine.py

COPY app.py .

RUN mkdir -p /app/uploads

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
