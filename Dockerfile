
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip git && \
    apt-get clean

# Install PyTorch with CUDA support
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install embedding models
RUN pip install sentence-transformers

WORKDIR /app
COPY app ./app

CMD ["python3", "app/test_gpu.py"]
