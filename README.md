# 📦 FastBar - Barcode Decoding API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Docker](https://img.shields.io/badge/docker-%20✓-blue)

FastAPI-powered REST API for barcode decoding from images and PDF documents. The core decoding logic has been refactored into a separate module (`barcode_decoder.py`) for better organization and reusability.

## 🚀 Features
- ✅ PDF document processing (multi-page support)
- 📸 Image support (PNG, JPG, BMP)
- 📍 Barcode location coordinates
- 🛡️ Error handling with detailed responses
- 🐳 Docker container ready
- 🖥️ Command-line interface for file decoding

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
  "file": "document.pdf",
  "pages": 3,
  "barcodes_found": 5,
  "results": [
    {
      "page": 1,
      "type": "CODE128",
      "data": "ABC-123",
      "location": {
        "left": 145,
        "top": 890,
        "width": 300,
        "height": 75
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

## 🖥️ Command-Line Usage

You can use the `barcode_decoder.py` script directly from the command line to decode barcodes from a file path.

```bash
python barcode_decoder.py <filepath>
```

Example:

```bash
python barcode_decoder.py path/to/your/document.pdf
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

Unit tests for the API endpoints and decoding logic are located in `test_main.py`. Unit tests for the core decoding logic in `barcode_decoder.py` have also been added.

## 📄 License
MIT License - See [LICENSE](LICENSE) for details
