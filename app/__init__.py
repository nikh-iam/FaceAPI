from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from app.routes.websocket_handler import websocket_endpoint
from app.services.recognition import recognition_system

app = FastAPI(
    title="FaceAPI",
    version="2.0"
)

@app.get("/")
async def status():
    """
    Check server status and return system details.
    """
    num_identities = len(recognition_system.known_faces)

    if num_identities == 0:
        return JSONResponse(
            status_code=503,
            content={
                "status_message": "Server not ready. No available faces found, please upload.",
                "no_faces_uploaded": 0
            }
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "Face Recognition Server is running",
            "faces_uploaded_count": num_identities
        }
    )

@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    """
    This is a WebSocket function.
    The input from client is image as byte format
    Output: 
    [
        {"label":"face1"},
        {"label":"face2"},
        ...
    ]
    """
    await websocket_endpoint(websocket)

