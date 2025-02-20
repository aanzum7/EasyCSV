from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import io
import json
from utils import convert_json_to_csv

app = FastAPI()

@app.post("/convert/")
async def convert_json_file(file: UploadFile = File(...)):
    """Endpoint to convert uploaded JSON file to CSV."""
    try:
        contents = await file.read()
        json_data = json.loads(contents)

        df = convert_json_to_csv(json_data)
        if df is None:
            raise HTTPException(status_code=400, detail="Invalid JSON format")

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')

        return {"filename": file.filename, "csv_data": csv_buffer.getvalue()}
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
