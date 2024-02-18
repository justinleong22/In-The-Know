from fastapi import FastAPI, File, UploadFile, Response
import uvicorn

from detect import *
from model import *
from all import predict_location

app = FastAPI()

@app.get("/api")
def server_test() -> dict[str, list[str]]:
    return {"messages": ["Server healthy."]}

@app.post("/api/update")
def update_user_info(files: list[UploadFile], latitude: list[float], longitude: list[float], res: Response):
    send_files = []
    send_lat = []
    send_long = []
    for i in range(len(files)):
        # safety check for file type
        if not files[i].content_type.startswith("audio/"):
            return {"error": "Invalid file type"}
        # safety check for lat. long. format
        if(len(latitude) != len(longitude)):
            return {"error": "Invalid coordinates"}
        
        else:
            # if there is an anomaly in the audio
            if(detect_gunshots(files[i])):
                # send to model along with lat and long
                send_files.append(files[i])
                send_lat.append(latitude[i])
                send_long.append(longitude[i])

    if(len(send_files) == 0):
        res.status_code = 500
        return "No detected anomalies"
    else:
        res.status_code = 200
        send(send_files, send_lat, send_long)
        return "Detected anomalies"
    
@app.get("/api/shooter_location")
def get_shooter_location():
    return predict_location()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)