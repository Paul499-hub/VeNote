
# 🧪 VectorNotepad – GPU Docker Compatibility Test

This branch provides a **minimal, isolated test** to verify that **CUDA GPU acceleration works inside Docker** on any machine.  
It is intended as a compatibility check **before** using GPU‑dependent features in the full VectorNotepad project.

---

# 🎯 Purpose of This Branch

✔ Test if the user's machine supports **Docker GPU passthrough**  
✔ Confirm **CUDA runtime** works inside a container  
✔ Test if a **local embedding model** loads on GPU  
✔ Provide a small, simple, reproducible environment  
✔ Detect configuration issues early (drivers, Docker, WSL, toolkit)

This branch does **not** contain any production code.  
It is only a **GPU + Docker validation utility**.

---

# 🧱 Requirements

Before running this test:

## 🟢 1. NVIDIA GPU (CUDA‑capable)
Any RTX / GTX card with modern drivers.

## 🟢 2. Latest NVIDIA GPU Driver Installed
Your host machine must have a driver supporting **CUDA ≥ 12.2**.

Check it with:
```sh
nvidia-smi
```

## 🟢 3. NVIDIA Container Toolkit Installed

This enables GPU passthrough to Docker.
Installation guide:
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
To verify GPU passthrough works:
```sh
docker run --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

If you see your GPU — you are good.

---

## 📁 Project Structure (minimal)

vectornotepad-gpu-test/
│
├── docker-compose.yml
├── Dockerfile
└── app/
    └── test_gpu.py

## 🐳 Docker GPU Test Instructions

### 1️⃣ Clone this branch

```sh
git checkout gpu-docker-test
```

### 2️⃣ Build & run the test container

```sh
docker-compose up --build
```

### 3️⃣ Expected successful output

CUDA available: True
GPU name: NVIDIA GeForce RTX 3070
Embedding shape: torch.Size([1, 384])
Embedding first 5 values: tensor([...], device='cuda:0')

## 🛠 Troubleshooting

### ❌ “CUDA available: False”
Likely causes:

- NVIDIA Container Toolkit not installed
- Docker Desktop GPU support disabled
- WSL2 not using GPU backend
- Old NVIDIA drivers

### ❌ “NVIDIA-SMI has failed”
This indicates the GPU driver is broken or missing.