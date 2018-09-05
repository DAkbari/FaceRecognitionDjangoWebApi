import face_recognition
import os
import numpy


def calculate(facePicture):
    Data_face_encoding = face_recognition.face_encodings(facePicture)[0]
    numpy.save()

    for file in os.listdir("C:/FaceDetect/TrainData"):
        print(file)
        Data_face_image = face_recognition.load_image_file("C:/FaceDetect/TrainData/" + file)
        try:
            Data_face_encoding = face_recognition.face_encodings(Data_face_image)[0]
        except:
            print("error")
            continue
        numpy.save("C:/FaceDetect/Encodes/" + file.split('.')[0] + ".txt", Data_face_encoding)
        os.remove("C:/FaceDetect/TrainData/" + file)
    return 6



def fetch():
    known_face_encodings = []
    known_face_names = []

    if len(os.listdir("C:\FaceDetect\Encodes")) < 1:
        print("NO RECORDS!")

    for file in os.listdir("C:\FaceDetect\Encodes"):
        known_face_names.append(file.split('.')[0])
        known_face_encodings.append(numpy.load("C:/FaceDetect/Encodes/" + file))

    return known_face_encodings, known_face_names


def detect(FaceEncodings, FNames):
    unknown_image_path = "C:/FaceDetect/Uploads/unknown.jpg"
    drawed_image_path = "C:/FaceDetect/Results/result.jpg"
    detected_names_path = "C:/FaceDetect/Personells/"
    command_file_path = "C:/FaceDetect/command.txt"

    treshold = 0.6
    known_face_encodings = FaceEncodings
    known_face_names = FNames
    names = list()
    try:
        unknown_image = face_recognition.load_image_file(unknown_image_path)
    except:
        print("file doesnt exists")
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        try:
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            name = "Unknown"

            if face_distances.min() < treshold:
                indices = [i for i, x in enumerate(face_distances) if x == face_distances.min()]
                # If a match was found in known_face_encodings, just use the first one.
                if len(indices) == 1:
                    name = known_face_names[indices[0]]
                    names.append(name)
        except:
            print("Error in measuring distance!")


    return ','.join(names)