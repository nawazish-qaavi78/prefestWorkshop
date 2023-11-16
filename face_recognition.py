import face_recognition
import cv2
import numpy as np
import os
import pyrebase

config = {
  "apiKey": "AIzaSyClastSM-d8sm0AWajY03OnezmkPVCrO04",
  "authDomain": "fir-topythonsample.firebaseapp.com",
  "projectId": "fir-topythonsample",
  "storageBucket": "fir-topythonsample.appspot.com",
  "databaseURL":"https://fir-topythonsample-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "messagingSenderId": "936536554705",
  "appId": "1:936536554705:web:f4d0b91b36e8174d7e99f0",
  "measurementId": "G-JL324VD9EC"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

def load_known_faces(DIR, people):
    known_face_encodings = []
    known_faces = []

    for person in people:
        sub_folder = os.path.join(DIR, person)
        for img in os.listdir(sub_folder):
            img_path = os.path.join(sub_folder, img)
            img_array = face_recognition.load_image_file(img_path)
            img_encoding = face_recognition.face_encodings(img_array)
            
            if img_encoding:
                known_face_encodings.extend(img_encoding)
                known_faces.extend([person] * len(img_encoding))
            else:
                print(f"No faces found in {img_path}")

    return known_face_encodings, known_faces

def recognize_faces(video_capture, known_face_encodings, known_faces):
    k=[]
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            matches, confidence_scores = match_faces(known_face_encodings, face_encodings, known_faces)
            
            k=display_results(frame, face_locations, matches, confidence_scores)
            cv2.imshow("video", frame)

        process_this_frame = not process_this_frame
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return k
def match_faces(known_face_encodings, face_encodings, known_faces):
    matches = []
    confidence_scores = []

    for face_encoding in face_encodings:
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if face_distances[best_match_index] < 0.4:
            matches.append(known_faces[best_match_index])
            confidence_scores.append(1 - face_distances[best_match_index])
        else:
            matches.append("Unknown")
            confidence_scores.append(0)

    return matches, confidence_scores

def display_results(frame, face_locations, matches, confidence_scores):
    a=[]
    for (top, right, bottom, left), name, confidence_score in zip(face_locations, matches, confidence_scores):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        cv2.putText(frame, f"{confidence_score:.2f}", (left - 100, bottom + 100), font, 1.0, (255, 255, 255), 1)
        a.append(confidence_score)
    return a
def main():
    x=[]
    video_capture = cv2.VideoCapture(0)
    people = ["bose", "ganesh", "varun", "yash"]
    DIR = r"C:\Users\thirn\OneDrive\Desktop\face"

    known_face_encodings, known_faces = load_known_faces(DIR, people)
    x=recognize_faces(video_capture, known_face_encodings, known_faces)
    avg_confidence=sum(x)/len(x)
    if(avg_confidence>=0.65):
        database.child("Stages").update({"stage2":1})
        print("working")
    else:
        print("Invalid User!")
    
