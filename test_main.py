import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock
import io

client = TestClient(app)

# Pruebas para el endpoint /decode/
def test_decode_image_success():
    # Crear un archivo de imagen simulado (un archivo vacío para la prueba)
    # En un escenario real, usarías un archivo de imagen con códigos de barras
    file_content = b"fake image content"
    files = {"file": ("test_image.png", io.BytesIO(file_content), "image/png")}
    
    # Simular la función decode_from_bytes para que devuelva un resultado conocido
    with patch("main.decode_from_bytes") as mock_decode:
        mock_decode.return_value = [{"type": "QRCODE", "data": "testdata", "page": 1, "location": {"left": 1, "top": 1, "width": 10, "height": 10}}]
        response = client.post("/decode/", files=files)

    assert response.status_code == 200
    assert response.json() == {
        "file": "test_image.png",
        "pages": 1,
        "barcodes_found": 1,
        "results": [{"type": "QRCODE", "data": "testdata", "page": 1, "location": {"left": 1, "top": 1, "width": 10, "height": 10}}],
    }

def test_decode_pdf_success():
    # Crear un archivo PDF simulado (un archivo vacío para la prueba)
    file_content = b"fake pdf content"
    files = {"file": ("test_pdf.pdf", io.BytesIO(file_content), "application/pdf")}
    
    # Simular la función decode_from_bytes para que devuelva resultados de múltiples páginas
    with patch("main.decode_from_bytes") as mock_decode:
        mock_decode.return_value = [
            {"type": "QRCODE", "data": "data1", "page": 1, "location": {"left": 1, "top": 1, "width": 10, "height": 10}},
            {"type": "CODE128", "data": "data2", "page": 2, "location": {"left": 5, "top": 5, "width": 20, "height": 20}},
        ]
        response = client.post("/decode/", files=files)

    assert response.status_code == 200
    assert response.json() == {
        "file": "test_pdf.pdf",
        "pages": 2,
        "barcodes_found": 2,
        "results": [
            {"type": "QRCODE", "data": "data1", "page": 1, "location": {"left": 1, "top": 1, "width": 10, "height": 10}},
            {"type": "CODE128", "data": "data2", "page": 2, "location": {"left": 5, "top": 5, "width": 20, "height": 20}},
        ],
    }

def test_decode_unsupported_file_type():
    # Crear un archivo de texto simulado
    file_content = b"fake text content"
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    
    response = client.post("/decode/", files=files)

    assert response.status_code == 415
    assert response.json() == {"detail": "Unsupported format. Use: PNG, JPG, PDF"}

def test_decode_internal_error():
    # Crear un archivo de imagen simulado
    file_content = b"fake image content"
    files = {"file": ("test_image.png", io.BytesIO(file_content), "image/png")}
    
    # Simular un error en decode_from_bytes
    with patch("main.decode_from_bytes") as mock_decode:
        mock_decode.side_effect = Exception("Simulated internal error")
        response = client.post("/decode/", files=files)

    assert response.status_code == 500
    assert "Error processing file:" in response.json()["detail"]

# Pruebas unitarias para la función decode_from_bytes en barcode_decoder.py
# Nota: Para pruebas más completas de decode_from_bytes, necesitarías
# imágenes y PDFs reales con códigos de barras y mockear las funciones
# externas como convert_from_bytes y pyzbar.decode.
# Aquí se presenta una estructura básica y un ejemplo simple.

from barcode_decoder import decode_from_bytes

def test_decode_from_bytes_image_no_barcode():
    # Simular una imagen sin códigos de barras
    mock_image = MagicMock()
    mock_decode_pyzbar = MagicMock(return_value=[]) # pyzbar.decode devuelve lista vacía si no encuentra nada

    with patch("barcode_decoder.Image.open", return_value=mock_image), \
         patch("barcode_decoder.decode", mock_decode_pyzbar):
        
        file_content = b"fake image content"
        results = decode_from_bytes(file_content, "image/png")
        
        assert results == []

def test_decode_from_bytes_pdf_with_barcodes():
    # Simular un PDF con códigos de barras en dos páginas
    mock_image1 = MagicMock()
    mock_image2 = MagicMock()
    mock_images = [mock_image1, mock_image2]

    # Simular la decodificación de pyzbar para cada imagen
    mock_decode_pyzbar = MagicMock()
    mock_decode_pyzbar.side_effect = [
        [MagicMock(type="QRCODE", data=b"data1", rect=MagicMock(left=1, top=1, width=10, height=10))], # Resultados para la página 1
        [MagicMock(type="CODE128", data=b"data2", rect=MagicMock(left=5, top=5, width=20, height=20))], # Resultados para la página 2
    ]

    with patch("barcode_decoder.convert_from_bytes", return_value=mock_images), \
         patch("barcode_decoder.decode", mock_decode_pyzbar):
        
        file_content = b"fake pdf content"
        results = decode_from_bytes(file_content, "application/pdf")
        
        assert len(results) == 2
        assert results[0]["page"] == 1
        assert results[0]["type"] == "QRCODE"
        assert results[0]["data"] == "data1"
        assert results[1]["page"] == 2
        assert results[1]["type"] == "CODE128"
        assert results[1]["data"] == "data2"
