from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI()


class DetectionResult(BaseModel):
    detected_objects: List[str]
    filename: str

# uvicorn predict:app --reload
@app.post("/detect")
async def detect(image: UploadFile = File(...)):
    img = await image.read()
    with open(image.filename, "wb") as f:
        f.write(img)

    model = YOLO("best.pt")  # build a new model from scratch
    results = model.predict(source=image.filename)
    names = model.names

    detected_objects = []
    for r in results:
        for c in r.boxes.cls:
            print(names[int(c)])
            detected_objects.append(names[int(c)])

    return {"detected_objects": detected_objects, "filename": image.filename}

@app.get("/")
def read_root():
    return {"Hello": "World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)