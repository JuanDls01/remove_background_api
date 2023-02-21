from fastapi import FastAPI, UploadFile
from model_ai import *
from fastapi.responses import HTMLResponse
from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO
import pybase64
from model_mp import remove_background_mediapipe

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root(file: UploadFile):
    image = remove_background_mediapipe(file)
    
    img_bytes = BytesIO()
    Image.fromarray(image).save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # convierte los bytes en un string base64 para usarlo en la etiqueta <img> de HTML
    img_data = pybase64.b64encode(img_bytes.read()).decode()

    # return Response(content=img_data, media_type="image/png")
    return f"""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <img src="data:image/png;base64,{img_data}" />
        </body>
    </html>
    """