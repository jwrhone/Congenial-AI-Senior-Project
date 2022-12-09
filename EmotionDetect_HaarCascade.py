# use this command to install CV2 package if not already installed: pip install cv2-python
import cv2

# These will need to be replaced with tflite equivalent import statement
import tflite_runtime.interpreter as tflite1

# **********************************************************************

import numpy as np
import os


class EmotionDetect_HaarCacasde:

    def __init__(self):
        self.fC = None
        self.eC = None
        self.eL = ['Angry', 'Happy', 'Neutral', 'Sad']  # emotion labels

        # Variable that hold emotion detected, for extraction purposes
        self.emotion = None

        # Testing variables
        self.emotionWeights = None
        self.predictedNPasArray = None
        self.predictedRESHAPE = None
        self.predictedExpandedDim = None

    def model_loading(self):
        # may be redundant *****************************************************
        dir = os.getcwd()
        print("Current Working Directory:", dir)

        interpreter = tflite1.Interpreter(model_path=dir + '//model.tflite') #dir+"//test.mp4"
        interpreter.allocate_tensors()
        # ***********************************************************************

        self.fC = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def set_input_tensor(self, interpreter, image):
        tensor_index = interpreter.get_input_details()[0]['index']

        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image

    def classify_image(self, interpreter, image):
        interpreter.invoke()

        output_details = interpreter.get_output_details()[0]

        scores = interpreter.get_tensor(output_details['index'])[0]
        print("Predicted class label score =", np.max(np.unique(scores)))

        max_score_index = np.where(scores == np.max(np.unique(scores)))[0][0]

        if max_score_index == 0:
            print("Detected Emotion: Angry")
        elif max_score_index == 1:
            print("Detected Emotion: Happy")
        elif max_score_index == 2:
            print("Detected Emotion: Neutral")
        elif max_score_index == 3:
            print("Detected Emotion: Sad")

        return max_score_index

    def emotion_detect_run(self):

        dir = os.getcwd()
        print("Current Working Directory:", dir)

        interpreter = tflite1.Interpreter(model_path=dir + '//model.tflite')
        interpreter.allocate_tensors()

        cap = cv2.VideoCapture(0)  # start webcam capture dir+"//test.mp4"

        while True:  # endless loop until key 'q' is pressed

            _, frame = cap.read()  # assign webcam input images to object frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert input image to grayscale for model
            faces = self.fC.detectMultiScale(gray)  # create array of faces detected through haarcascade

            for (x, y, w, h) in faces:  # for all image dimensions in each image in the faces array
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # draw box around detected face(s)
                roi_gray = gray[y:y + h, x:x + w]  # assign Region Of Interest strictly to whatever is inside above box
                roi_gray = cv2.resize(roi_gray, (48, 48),
                                      interpolation=cv2.INTER_AREA)  # resize Region Of Interest to 48x48 to work with model

                if np.sum([roi_gray]) != 0:  # if a face(s) is detected
                    roi = roi_gray.astype(
                        'float') / 255.0  # normalize by dividing Region of Intererst of by 255 (the greatest possible value when dealing with grayscale, 255=white)
                    toBePredicted = np.asarray(roi,
                                               dtype=np.float32)  # converting Region of Interest into a float 32 array. It is in the form of (1, 48, 48)

                    self.predictedNPasArray = toBePredicted

                    toBePredicted = toBePredicted.reshape((toBePredicted.shape[0], toBePredicted.shape[1],
                                                           1))  # Reshape region on interest array into the form of (48, 48, 1)

                    self.predictedRESHAPE = toBePredicted

                    self.set_input_tensor(interpreter, toBePredicted)

                    toBePredicted = np.expand_dims(roi,
                                                   axis=0)  # make sure Region of Interest array is in mxn format (1xn in this case). Now in the form of (48, 48)

                    self.predictedExpandedDim = toBePredicted

                    label_id = self.classify_image(interpreter, roi)

                    if label_id == 0:
                        self.emotion = "angry"
                    elif label_id == 1:
                        self.emotion = "happy"
                    elif label_id == 2:
                        self.emotion = "neutral"
                    elif label_id == 3:
                        self.emotion = "sad"

                    label = self.emotion  # assign that emotion from self.emotion for extraction use

                    label_position = (x, y)
                    cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                2)  # print label name near Region of Interest
                else:
                    cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                                2)  # print 'No faces' if no faces are detected
            cv2.imshow('Emotion Detector', frame)  # show box drawn and emotion identified around face(s) detected
            #if cv2.waitKey(1) & 0xFF == ord('q'):  # press 'q' key to terminate program
            break

        print('Emotion Detection Haar Cascade Finished Running')