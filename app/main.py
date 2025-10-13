import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routers.image_generator_router import ImageGeneratorRouter
import uvicorn

app = FastAPI(title="Image Generator API")

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set up templates
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Set up static files with no-cache headers for development
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

class NoCacheStaticFiles(StaticFiles):
    def file_response(self, *args, **kwargs):
        response = super().file_response(*args, **kwargs)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

app.mount("/static", NoCacheStaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Create router instance
image_generator_router = ImageGeneratorRouter()


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("image_generator.html", {"request": request})


from fastapi import Body
from typing import Dict

@app.post("/api/generate_image")
async def generate_image(user_input: str = Body(..., embed=True)):
    response = image_generator_router.generate_image(user_input)
    
    # Check if the response contains an error
    if isinstance(response, tuple) and len(response) == 2 and 'error' in response[0]:
        error_message = response[0]['error']
        status_code = response[1]
        raise HTTPException(status_code=status_code, detail=error_message)
    
    return response

@app.get("/api/get_images")
async def get_images():
    return image_generator_router.get_images()

@app.get("/api/get_csv_log")
async def get_csv_log():
    return image_generator_router.get_csv_log()

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)