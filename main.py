from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
from pyzbar.pyzbar import decode
from PIL import Image
import io

app = FastAPI()


@app.post("/decode/")
async def decode_barcodes(file: UploadFile = File(...)):
    # Validar tipo de archivo
    content_type = file.content_type
    if not content_type.startswith("image/") and content_type != "application/pdf":
        raise HTTPException(
            status_code=415, detail="Formato no soportado. Use: PNG, JPG, PDF"
        )

    try:
        file_bytes = await file.read()
        results = []

        if content_type == "application/pdf":
            images = convert_from_bytes(file_bytes)
            for page_num, image in enumerate(images, 1):
                decoded = decode(image)
                for barcode in decoded:
                    results.append(
                        {
                            "pagina": page_num,
                            "tipo": barcode.type,
                            "datos": barcode.data.decode("utf-8"),
                            "ubicacion": {
                                "izquierda": barcode.rect.left,
                                "superior": barcode.rect.top,
                                "ancho": barcode.rect.width,
                                "alto": barcode.rect.height,
                            },
                        }
                    )
        else:
            image = Image.open(io.BytesIO(file_bytes))
            decoded = decode(image)
            for barcode in decoded:
                results.append(
                    {
                        "pagina": 1,
                        "tipo": barcode.type,
                        "datos": barcode.data.decode("utf-8"),
                        "ubicacion": {
                            "izquierda": barcode.rect.left,
                            "superior": barcode.rect.top,
                            "ancho": barcode.rect.width,
                            "alto": barcode.rect.height,
                        },
                    }
                )

        return JSONResponse(
            content={
                "archivo": file.filename,
                "paginas": len(images) if content_type == "application/pdf" else 1,
                "codigos_encontrados": len(results),
                "resultados": results,
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error procesando archivo: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
