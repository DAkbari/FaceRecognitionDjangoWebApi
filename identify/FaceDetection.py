import face_recognition
import os
import sys
from PIL import Image, ImageDraw
from time import sleep
import time


def faceDetection(picture, personellencodes, personellCodes):
    treshold = 0.6
    known_face_encodings = []

    names = list()
    # Load an image with an unknown face
    try:
        unknown_image = face_recognition.load_image_file(picture)
        # Find all the faces and face encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    except:
        print("Error in ecoding unknown image!")

    for (top, right, bottom, left), face_encoding in zip(face_locations, personellencodes):
        # See if the face is a match for the known face(s)
        name = "Unknown"
        try:
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if face_distances.min() < treshold:
                indices = [i for i, x in enumerate(face_distances) if x == face_distances.min()]
                # If a match was found in known_face_encodings, just use the first one.
                if len(indices) == 1:
                    name = personellCodes[indices[0]]

        except:
            print("Error in measuring distance!")

        names.append(name)

    return names.join(',')

