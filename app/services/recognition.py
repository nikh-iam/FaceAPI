import numpy as np
import cv2
from app.models import initialize_face_analysis, load_known_embeddings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class FaceRecognitionSystem:
    def __init__(self):
        try:
            self.detection = initialize_face_analysis()
            self.known_faces = load_known_embeddings()

        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            self.known_faces = {}
            self.detection = None

    def recognize_face(self, embedding):
        if not self.known_faces:
            return "Unknown", 0

        best_match, best_score = None, -1
        for name, ref_embedding in self.known_faces.items():
            similarity = np.dot(embedding, ref_embedding) / (
                np.linalg.norm(embedding) * np.linalg.norm(ref_embedding)
            )
            if similarity > best_score:
                best_score, best_match = similarity, name

        confidence = (best_score + 1) / 2 * 100
        return best_match if best_score > 0.5 else "Unknown", confidence

    def process_frame(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        if self.detection is None:
            return []
        
        faces = self.detection.get(small_frame)
        faces.sort(key=lambda face: (face.bbox[2] - face.bbox[0]) * (face.bbox[3] - face.bbox[1]), reverse=True)
        for face in faces:
            face.label, _ = self.recognize_face(face.embedding)
        return faces

recognition_system = FaceRecognitionSystem()
