# 📦 FastBar - Barcode Decoding API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Docker](https://img.shields.io/badge/docker-%20✓-blue)

FastAPI-powered REST API for barcode decoding from images and PDF documents.

## 🚀 Features
- ✅ PDF document processing (multi-page support)
- 📸 Image support (PNG, JPG, BMP)
- 📍 Barcode location coordinates
- 🛡️ Error handling with detailed responses
- 🐳 Docker container ready

## 🔌 API Reference

### POST /decode/
```python
@app.post("/decode/")
async def decode_barcodes(file: UploadFile = File(...))
```

#### Parameters
- `file`: Supported formats:
  - PDF (`application/pdf`)
  - Images (`image/png`, `image/jpeg`, `image/bmp`)

#### Success Response
```json
{
  "archivo": "document.pdf",
  "paginas": 3,
  "codigos_encontrados": 5,
  "resultados": [
    {
      "pagina": 1,
      "tipo": "CODE128",
      "datos": "ABC-123",
      "ubicacion": {
        "izquierda": 145,
        "superior": 890,
        "ancho": 300,
        "alto": 75
      }
    }
  ]
}
```

#### Error Responses
- `415 Unsupported Media Type`: Invalid file format
- `500 Internal Server Error`: Processing failure

## ⚙️ Installation

```bash
# Clone repository
git clone https://github.com/yourusername/fastbar.git
cd fastbar

# Install dependencies
pip install -r requirements.txt

# Install system dependencies (PDF support)
sudo apt-get install poppler-utils
```

## 🏃 Running the Server

```bash
uvicorn main:app --reload --port 8000
```

## 🐳 Docker Usage

```bash
# Build and run
docker build -t fastbar .
docker run -p 8000:8000 fastbar

# Test container
docker exec -it fastbar curl http://localhost:8000/docs
```

## 💻 Usage Example

```bash
# Decode PDF document
curl -X POST -F "file=@document.pdf" http://localhost:8000/decode/

# Decode image file
curl -X POST -F "file=@barcode.png" http://localhost:8000/decode/
```

## 🛠️ Development

```bash
# Run tests
pytest tests/

# Code formatting
black main.py

# Linting
flake8 main.py
```

## 📄 License
MIT License - See [LICENSE](LICENSE) for details