import io
import argparse
import sys
import mimetypes
import json
from pdf2image import convert_from_bytes
from pyzbar.pyzbar import decode
from PIL import Image

def decode_from_bytes(file_bytes: bytes, content_type: str) -> list:
    """
    Decodifica códigos de barras de bytes de archivo de imagen o PDF.

    Args:
        file_bytes: Contenido del archivo en bytes.
        content_type: Tipo MIME del archivo ('image/...' o 'application/pdf').

    Returns:
        Una lista de diccionarios con los resultados de la decodificación.
    """
    results = []

    if content_type == "application/pdf":
        images = convert_from_bytes(file_bytes)
        for page_num, image in enumerate(images, 1):
            decoded = decode(image)
            for barcode in decoded:
                results.append(
                    {
                        "page": page_num,
                        "type": barcode.type,
                        "data": barcode.data.decode("utf-8"),
                        "location": {
                            "left": barcode.rect.left,
                            "top": barcode.rect.top,
                            "width": barcode.rect.width,
                            "height": barcode.rect.height,
                        },
                    }
                )
    else:
        image = Image.open(io.BytesIO(file_bytes))
        decoded = decode(image)
        for barcode in decoded:
            results.append(
                {
                    "page": 1,
                    "type": barcode.type,
                    "data": barcode.data.decode("utf-8"),
                    "location": {
                        "left": barcode.rect.left,
                        "top": barcode.rect.top,
                        "width": barcode.rect.width,
                        "height": barcode.rect.height,
                    },
                }
            )

    return results

def decode_from_filepath(filepath: str) -> list:
    """
    Decodifica códigos de barras de un archivo dado su ruta.

    Args:
        filepath: Ruta al archivo de imagen o PDF.

    Returns:
        Una lista de diccionarios con los resultados de la decodificación.
    """
    try:
        with open(filepath, "rb") as f:
            file_bytes = f.read()
        content_type, _ = mimetypes.guess_type(filepath)
        if content_type is None:
             # Default to image if type cannot be guessed
            content_type = "image/unknown"
        return decode_from_bytes(file_bytes, content_type)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decodes barcodes from a file.")
    parser.add_argument("filepath", help="Path to the image or PDF file.")
    args = parser.parse_args()

    results = decode_from_filepath(args.filepath)
    print(json.dumps(results, indent=4))
