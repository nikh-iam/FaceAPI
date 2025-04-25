import json
import numpy as np
import cv2
from fastapi import WebSocket, WebSocketDisconnect
from app.services.recognition import recognition_system
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def websocket_endpoint(websocket: WebSocket):
    """ 
    1. Accepts client
    2. Recieves frames as Bytes [...]
    3. Process with Recognition class
    4. Send Responses
    5. Disconnects client
    """
    await websocket.accept()
    logger.info("Client Connected")

    try:
        while True:
            data = await websocket.receive_bytes()
            frame = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            if frame is None:
                await websocket.send_text(
                    json.dumps({
                        "error": "Failed to decode image", 
                        "code": 422
                    })
                )
                continue

            faces = recognition_system.process_frame(frame)
            face_data = [{"label": face.label} for face in faces]

            if not face_data:
                await websocket.send_text(
                    json.dumps({
                        "error": "No valid face detected", 
                        "code": 404
                    })
                )
                continue

            logger.info("After Recognition: " + json.dumps(face_data))
            await websocket.send_text(json.dumps(face_data))

    except WebSocketDisconnect:
        logger.info("Client Disconnected")
        
    except Exception as e:
        await websocket.send_text(
            json.dumps({
                "error": f"Internal Server Error: {str(e)}",
                "code": 500
            })
        )
