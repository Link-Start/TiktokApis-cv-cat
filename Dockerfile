FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    NODE_ENV=production

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    nodejs \
    npm \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    libjpeg62-turbo-dev \
    libgif-dev \
    librsvg2-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY static/package.json static/package-lock.json ./static/
RUN cd static && npm ci --omit=dev

COPY api ./api
COPY static ./static
COPY utils ./utils
COPY README.md ./

CMD ["python", "-c", "import api.tiktok, api.tiktok_chat; print('TikTok Reverse API image ready')"]
