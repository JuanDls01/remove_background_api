from fastapi import FastAPI, UploadFile, Response
from model import *
from fastapi.responses import HTMLResponse
from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO
import pybase64
from model_mp import remove_background_mediapipe, custom_background

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root(file: UploadFile, background: UploadFile):

    # Convierte la imagen numpy en un objeto BytesIO

    image = remove_background_mediapipe(file, background)
    # image_with_custom_bg = custom_background(background, image)
    
    img_bytes = BytesIO()
    Image.fromarray(image).save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # convierte los bytes en un string base64 para usarlo en la etiqueta <img> de HTML
    img_data = pybase64.b64encode(img_bytes.read()).decode()
    response = {"file": img_data}
    return Response(content=img_data, media_type="image/png")
    # return f"""
    # <html>
    #     <head>
    #         <title>Some HTML in here</title>
    #     </head>
    #     <body>
    #         <img src="data:image/png;base64,{img_data}" />
    #     </body>
    # </html>
    # """