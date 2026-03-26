FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/.local/bin:${PATH}"
ENV UV_PROJECT_ENVIRONMENT="/app/.venv"

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --frozen
#RUN ls -lah /app && find /app -maxdepth 3 -type f | sort
#RUN find / -path "*/bin/pip" 2>/dev/null | head -50

RUN /app/.venv/bin/python -m ensurepip
RUN /app/.venv/bin/python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

COPY app ./app

CMD ["/app/.venv/bin/python", "app/main.py"]