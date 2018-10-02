import face_recognition
import os
import sys
from PIL import Image, ImageDraw
from time import sleep
import time
import numpy
from identify.models import Person

def faceDetection(userID):
    treshold = 0.6
    known_face_encodings = list()
    known_face_ids = list()
    detectedIDs = list()

    Ids = [i[0] for i in Person.objects.filter(associatedUser=userID).values_list('id')]

    for iden in Ids:
        try:
            known_face_encodings.append(numpy.load('numpySave/' + str(iden) + '.npy'))
            known_face_ids.append(iden)
        except Exception as e:
            print(e)


    people = list()
    names = list()
    indices = list()

    # Load an image with an unknown face
    try:
        unknown_image = face_recognition.load_image_file('recorded/newPhoto.png')
        # Find all the faces and face encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    except:
        print("Error in ecoding unknown image!")

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        name = "Unknown"

        try:
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if len(face_distances) > 0 and face_distances.min() < treshold:
                indices = [i for i, x in enumerate(face_distances) if x == face_distances.min()]
                # If a match was found in known_face_encodings, just use the first one.
                if len(indices) == 1:
                    # name = fNames[indices[0]] + " " + lNames[indices[0]]
                    id = known_face_ids[indices[0]]
                    detectedIDs.append(id)
        except:
            print("Error in measuring distance!")





    return detectedIDs

