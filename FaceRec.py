import time
from turtle import colormode
import face_recognition
from PIL import Image
import matplotlib.pyplot as plt
import dlib
dlib.DLIB_USE_CUDA
import cv2
import numpy as np
import os



class FaceRecognition_DLIB:
    def assign_name(str):
        self.tempname = str

    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.fC = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.tempName = None
        self.token = 1
        self.name = None
        self.inputname = None
    
    def  learn_face(self):
        dir = os.getcwd()
        image_directory = dir + '/data'
        print(image_directory)
        # Load a sample picture and learn how to recognize it.
        CarlosCordova_image = face_recognition.load_image_file("data/CarlosCordova.jpeg")
        face_locations = face_recognition.face_locations(CarlosCordova_image)

        CarlosCordova_encoding = face_recognition.face_encodings(CarlosCordova_image)[0]

        self.known_face_encodings.append(CarlosCordova_encoding)
        self.known_face_names.append("Carlos Cordova")

        if os.path.exists ("UnknownPerson1Info.txt") == True: 
            self.token = 2

        if os.path.exists ("UnknownPerson2Info.txt") == True: 
            self.token = 3

        if os.path.exists ("UnknownPerson3Info.txt") == True: 
            self.token = 4

        if os.path.exists ("UnknownPerson4Info.txt") == True: 
            self.token = 5
        
        if os.path.exists ("UnknownPerson5Info.txt") == True: 
            self.token = 1




        print(" ")
        print("cap device")
        print(' ')

        cap = cv2.VideoCapture(0) #start webcam capture
        while True: #endless loop until key 'q' is pressed

            _, frame = cap.read()#assign webcam input images to object frame
            #coloredImage = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)#convert input image to grayscale for model
            #detect mulitscale may produce potential array index out of bounds error: look into detect only one face
            faces = self.fC.detectMultiScale(frame)#create array of faces detected through haarcascade

            for (x,y,w,h) in faces:#for all image dimensions in each image in the faces array
                #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),)#draw box around detected face(s)
                roi= frame[y:y+h+100,x:x+w+100]#assign Region Of Interest strictly to whatever is inside above box

                while True :
                    if self.inputname != None:
                        print(self.inputname)
                        newName = self.inputname
                    else:
                        print("Inputname was not given.")
                        newName = self.tempName
                    #self.tempName = input("Enter Name:\n")
                    print(f'Your name is {self.tempName}')

                    filename = image_directory + '/' + newName + '.jpg'
                    cv2.imwrite(filename, roi)
                    print("File Name: ", filename)
                    break
            break

        if(self.token == 5):
            person5_image = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(person5_image)

            person5_encoding = face_recognition.face_encodings(person5_image)[0]

            self.known_face_encodings.append(person5_encoding)
            self.known_face_names.append(newName)
            token = 1
            
            lines = ['person5_image = face_recognition.load_image_file(r' + '"'+ filename + '"' +')',
                     'face_locations = face_recognition.face_locations(person5_image)',
                      'person5_encoding = face_recognition.face_encodings(person5_image)[0]',
                       'self.known_face_encodings.append(person5_encoding)',
                        'self.known_face_names.append(' + '"'+ newName +'"'+ ')']

            with open('UnknownPerson5Info.txt', 'w') as f:
                for line in lines:
                    f.write(line)
                    f.write('\n')


        if(self.token == 4):
            person4_image = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(person4_image)

            person4_encoding = face_recognition.face_encodings(person4_image)[0]

            self.known_face_encodings.append(person4_encoding)
            self.known_face_names.append(newName)
            token = 5

            lines = ['person4_image = face_recognition.load_image_file(r' + '"'+ filename + '"' +')',
                     'face_locations = face_recognition.face_locations(person4_image)',
                      'person4_encoding = face_recognition.face_encodings(person4_image)[0]',
                       'self.known_face_encodings.append(person4_encoding)',
                        'self.known_face_names.append(' + '"'+ newName +'"'+ ')']

            with open('UnknownPerson4Info.txt', 'w') as f:
                for line in lines:
                    f.write(line)
                    f.write('\n')


        if (self.token == 3):    
            person3_image = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(person3_image)

            person3_encoding = face_recognition.face_encodings(person3_image)[0]

            self.known_face_encodings.append(person3_encoding)
            self.known_face_names.append(newName)
            token = 4
            
            lines = ['person3_image = face_recognition.load_image_file(r' + '"'+ filename + '"' +')',
                     'face_locations = face_recognition.face_locations(person3_image)',
                      'person3_encoding = face_recognition.face_encodings(person3_image)[0]',
                       'self.known_face_encodings.append(person3_encoding)',
                        'self.known_face_names.append(' + '"'+ newName +'"'+ ')']

            with open('UnknownPerson3Info.txt', 'w') as f:
                for line in lines:
                    f.write(line)
                    f.write('\n')


        if (self.token == 2):
            person2_image = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(person2_image)

            person2_encoding = face_recognition.face_encodings(person2_image)[0]

            self.known_face_encodings.append(person2_encoding)
            self.known_face_names.append(newName)
            token = 3
            
            lines = ['person2_image = face_recognition.load_image_file(r' + '"'+ filename + '"' +')',
                     'face_locations = face_recognition.face_locations(person2_image)',
                      'person2_encoding = face_recognition.face_encodings(person2_image)[0]',
                       'self.known_face_encodings.append(person2_encoding)',
                        'self.known_face_names.append(' + '"'+ newName +'"'+ ')']

            with open('UnknownPerson2Info.txt', 'w') as f:
                for line in lines:
                    f.write(line)
                    f.write('\n')


        if(self.token == 1):
            person1_image = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(person1_image)

            person1_encoding = face_recognition.face_encodings(person1_image)[0]

            self.known_face_encodings.append(person1_encoding)
            self.known_face_names.append(newName)
            self.token = 2

            lines = ['person1_image = face_recognition.load_image_file(r' + '"'+ filename + '"' +')',
                     'face_locations = face_recognition.face_locations(person1_image)',
                      'person1_encoding = face_recognition.face_encodings(person1_image)[0]',
                       'self.known_face_encodings.append(person1_encoding)',
                        'self.known_face_names.append(' + '"'+ newName +'"'+ ')']

            with open('UnknownPerson1Info.txt', 'w') as f:
                for line in lines:
                    f.write(line)
                    f.write('\n')
                   # f.close()
            
    def learn_unknown_faces_group(self):
        if os.path.exists ("UnknownPerson1Info.txt") == True: 
            exec(open("./UnknownPerson1Info.txt").read())

        if os.path.exists ("UnknownPerson2Info.txt") == True: 
            exec(open("./UnknownPerson2Info.txt").read())

        if os.path.exists ("UnknownPerson3Info.txt") == True: 
            exec(open("./UnknownPerson3Info.txt").read())

        if os.path.exists ("UnknownPerson4Info.txt") == True: 
            exec(open("./UnknownPerson4Info.txt").read())
        
        if os.path.exists ("UnknownPerson5Info.txt") == True: 
            exec(open("./UnknownPerson5Info.txt").read())
        #Learning/loading previously unknown user 1 info 
      


    def  learn_face_group(self):
        # Load a sample picture and learn how to recognize it.
        CarlosCordova_image = face_recognition.load_image_file("data/CarlosCordova.jpeg")
        face_locations = face_recognition.face_locations(CarlosCordova_image)

        JacobRhone_image = face_recognition.load_image_file("data/JacobRhone.jpg")
        face_locations = face_recognition.face_locations(JacobRhone_image)

        AlbertoBarrera_image = face_recognition.load_image_file("data/AlbertoBarrera.jpg")
        face_locations = face_recognition.face_locations(AlbertoBarrera_image)

        RafaelPerez_image = face_recognition.load_image_file("data/RafaelPerez.jpg")
        face_locations = face_recognition.face_locations(RafaelPerez_image)

        RyanMarquez_image = face_recognition.load_image_file("data/RyanMarquez.jpg")
        face_locations = face_recognition.face_locations(RyanMarquez_image)

        #VianneyCordova_image = face_recognition.load_image_file("data/VianneyCordova.jpg")
        #face_locations = face_recognition.face_locations(VianneyCordova_image)

        CarlosCordova_encoding = face_recognition.face_encodings(CarlosCordova_image)[0]
        JacobRhone_encoding = face_recognition.face_encodings(JacobRhone_image)[0]
        AlbertoBarrera_encoding = face_recognition.face_encodings(AlbertoBarrera_image)[0]
        RafaelPerez_encoding = face_recognition.face_encodings(RafaelPerez_image)[0]
        RyanMarquez_encoding = face_recognition.face_encodings(RyanMarquez_image)[0]
        #VianneyCordova_encoding = face_recognition.face_encodings(VianneyCordova_image)[0]

        self.known_face_encodings.append(CarlosCordova_encoding)
        self.known_face_names.append("Carlos Cordova")

        self.known_face_encodings.append(JacobRhone_encoding)
        self.known_face_names.append("Jacob Rhone")

      #  self.known_face_encodings.append(AlbertoBarrera_encoding)
      # self.known_face_names.append("Alberto Barrera")

      #  self.known_face_encodings.append(RafaelPerez_encoding)
      #  self.known_face_names.append("Rafael Perez")

        self.known_face_encodings.append(RyanMarquez_encoding)
        self.known_face_names.append("Ryan Marquez")

            





    def RecFace (self):
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    self.name = "unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        self.name = self.known_face_names[best_match_index]

                    face_names.append(self.name)

            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), self.name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                color = (0, 255, 0)
                
                if self.name == "unknown":
                    color = (0, 0, 255)

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, self.name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

           # # Display the resulting image
            #cv2.imshow('Video', frame)

           # try:
            #    timeout = time.time() + 5
            #    while time.time() < timeout:
                    #_, frame = video_capture.read()
            #        cv2.waitKey(1)
             #       cv2.imshow('Frame', frame)
            #except:
             #   break

            video_capture.release()
            cv2.destroyAllWindows()
            break


            '''
            try : 
                # Hit 'q' on the keyboard to quit!
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    # Release handle to the webcam
                    video_capture.release()
                    cv2.destroyAllWindows()            
                    break
                
            except:
                break
            '''
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()




