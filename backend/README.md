## 🧰 Getting Started

Follow these steps to run the system locally.

---

### 🐳 Start Required Docker Services

#### 1. Start MongoDB
```bash
docker compose -f docker-compose.mongo.yml up -d
```
#### 2. Start MinIO Storage
```bash
docker compose -f docker-compose.minio.yml up -d
```

### 🚀 Start the FastAPI Backend at KMS-SofwareDesign folder
```bash
uvicorn backend.app:app --reload
```
