from fastapi import FastAPI
from model import *
from fastapi.responses import HTMLResponse
from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO
import pybase64

# TODO: Upload your file and define the filename input_file
# Optional: Also upload or define the background file/url
input_file = 'content/CopiaPerfil.jpg'
background_url = 'https://images.unsplash.com/photo-1475139441338-693e7dbe20b6?auto=format&fit=crop&w=640&q=427'

background_file = '/content/background.jpg'
foreground_file = '/content/foreground.png'
output_file = '/content/final.jpg'

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():

    deeplab_model = load_model()
    foreground, bin_mask = remove_background(deeplab_model, input_file)

    # Convierte la imagen numpy en un objeto BytesIO
    img_bytes = BytesIO()
    Image.fromarray(foreground).save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # convierte los bytes en un string base64 para usarlo en la etiqueta <img> de HTML
    img_data = pybase64.b64encode(img_bytes.read()).decode()

    # guarda la imagen procesada en disco
    # Image.fromarray(foreground).save(output_file)

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