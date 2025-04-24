from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import io
from barcode_decoder import decode_from_bytes # Importar la nueva función

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
        
        # Usar la función del módulo separado para decodificar
        results = decode_from_bytes(file_bytes, content_type)

        # Determinar el número de páginas para la respuesta JSON
        # Esto requiere una pequeña modificación ya que decode_from_bytes no devuelve 'images'
        # Si es PDF, asumimos que cada resultado con página > 1 proviene de una página diferente
        num_pages = 1
        if content_type == "application/pdf" and results:
             num_pages = max([res.get("pagina", 1) for res in results])


        return JSONResponse(
            content={
                "archivo": file.filename,
                "paginas": num_pages,
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
