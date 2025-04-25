import os
import pickle
from insightface.app import FaceAnalysis
from app.config import EMBEDDINGS_DIR

def initialize_face_analysis():
    detection = FaceAnalysis(
        name='buffalo_s',
        providers=['CPUExecutionProvider'],
        allowed_modules=['detection', 'recognition']
    )
    detection.prepare(ctx_id=0, det_size=(640, 640))
    return detection

def load_known_embeddings():
    known_faces = {}
    if not os.path.exists(EMBEDDINGS_DIR):
        os.makedirs(EMBEDDINGS_DIR)
        return known_faces

    for file in os.listdir(EMBEDDINGS_DIR):
        if file.endswith('.pkl'):
            name = os.path.splitext(file)[0]
            with open(os.path.join(EMBEDDINGS_DIR, file), "rb") as f:
                known_faces[name] = pickle.load(f)
    return known_faces
