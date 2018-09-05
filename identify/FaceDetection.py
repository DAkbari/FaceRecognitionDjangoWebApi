import face_recognition
import os
import sys
from PIL import Image, ImageDraw
import StoringRecords
from time import sleep
import time


#def faceDetection(train, treshold):
def faceDetection():
    treshold = 0.6
    known_face_encodings = []
    known_face_names = []

    last_train = 0
    upload = 0
    processed = 0

    unknown_image_path = "C:/FaceDetect/Uploads/unknown.jpg"
    drawed_image_path = "C:/FaceDetect/Results/result.jpg"
    detected_names_path = "C:/FaceDetect/Personells/"
    command_file_path = "C:/FaceDetect/command.txt"


    #if train == "True":
    #   StoringRecords.calculate()

    known_face_encodings, known_face_names = StoringRecords.fetch()


    Commandfh = open(command_file_path, "w")
    Commandfh.close()


    while True:
        sleep(0.1)
        Commandfh = open(command_file_path, "r")
        Commands = Commandfh.read().split('\t')
        if len(Commands) < 2:
            continue
        #train 3/ 
        upload = int(Commands[0])
        command = Commands[1]

        if command == "train" and upload > last_train:
            try:
                StoringRecords.calculate()
                known_face_encodings, known_face_names = StoringRecords.fetch()
            except:
                print("couldn't load encodes!")
            processed = last_train = upload
            continue


        strupload = str(upload)


        if upload > processed:
            startTime = time.time()
            names = list();
            # Load an image with an unknown face
            try:
                unknown_image = face_recognition.load_image_file(unknown_image_path)
                # Find all the faces and face encodings in the unknown image
                face_locations = face_recognition.face_locations(unknown_image)
                face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
            except:
                print("Error in ecoding unknown image!")
                processed = upload
                continue
            # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
            # See http://pillow.readthedocs.io/ for more about PIL/Pillow
            #pil_image = Image.fromarray(unknown_image)
            # Create a Pillow ImageDraw Draw instance to draw with
            #draw = ImageDraw.Draw(pil_image)


            # Loop through each face found in the unknown image
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                try:
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    name = "Unknown"

                    if(face_distances.min() < treshold ):
                        indices = [i for i, x in enumerate(face_distances) if x == face_distances.min()]
                        # If a match was found in known_face_encodings, just use the first one.
                        if len(indices) == 1:
                            name = known_face_names[indices[0]]

                except:
                    print("Error in measuring distance!")

                print("detected face is :" + name)
                names.append(name);
                # Draw a box around the face using the Pillow module
                #draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

                # Draw a label with a name below the face
                #text_width, text_height = draw.textsize(name)
                #draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
                #draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))


            # Remove the drawing library from memory as per the Pillow docs
            #del draw

            # Display the resulting image
            #pil_image.show()
            endTime = time.time()
            # You can also save a copy of the new image to disk if you want by uncommenting this line

            #pil_image.save(drawed_image_path)
            detected_namesfh = open(detected_names_path + strupload + '.txt', "w")

            detected_namesfh.write(','.join(names))
            detected_namesfh.write("\n" + str(endTime-startTime))
            detected_namesfh.close()

            processed = upload


if __name__ == "__main__":
    #train = sys.argv[1]
    #treshold = float(sys.argv[2])
    #faceDetection(train, treshold)
    faceDetection()
