from typing import Annotated
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI(title="Mostrador de Boletines")

# Conexión a la BD
def obtener_boletin_db(boletin_id: str, correo: str):
    conn = sqlite3.connect('boletines.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, contenido, s3_url FROM boletines WHERE id = ? AND correo = ?", 
        (boletin_id, correo)
    )
    resultado = cursor.fetchone()
    
    # Marcar como leído si existe
    if resultado:
        cursor.execute("UPDATE boletines SET leido = 1 WHERE id = ?", (boletin_id,))
        conn.commit()
        
    conn.close()
    return resultado

@app.get(
    "/boletines/{boletin_id}", 
    response_class=HTMLResponse,
    responses={404: {"description": "Boletín no encontrado o el correo es incorrecto"}}
)
def obtener_boletin(
    boletin_id: str, 
    correo_electronico: Annotated[
        str, 
        Query(
            alias="correoElectronico",
            regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )
    ]
):
    
    boletin = obtener_boletin_db(boletin_id, correo_electronico)
    
    if not boletin:
        raise HTTPException(status_code=404, detail="Boletín no encontrado o el correo es incorrecto")
        
    _, contenido, s3_url = boletin
    
    # Generamos un pequeño HTML para mostrar literalmente la imagen
    html_content = f"""
    <html>
        <head><title>Tu Boletín</title></head>
        <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            <h1>Boletín: {boletin_id}</h1>
            <p><strong>Mensaje:</strong> {contenido}</p>
            <br/>
            <img src="{s3_url}" alt="Imagen del boletin" style="max-width: 500px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"/>
            <br/><br/>
            <a href="{s3_url}" target="_blank">Enlace directo a la imagen en S3</a>
        </body>
    </html>
    """
    return html_content

