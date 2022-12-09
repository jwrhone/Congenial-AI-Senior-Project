import logging
import os
from EmotionDetect_HaarCascade import EmotionDetect_HaarCacasde
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from gtts import gTTS
#from playsound import playsound
import pygame
import speech_recognition as sr
import time
import serial
from fileinput import filename
from FaceRec import FaceRecognition_DLIB
global mood

# Upon running for the first time, you need to edit chatbotfun\venv\Lib\site-packages\sqlalchemy\util\compat.py
# go to line 264, replace time.clock with time.process_time()

def text2speech(tts): #this function is for text 2 speech
    speech = gTTS(text=tts, lang='en', slow=False)
    speech.save("talk.mp3")
    pygame.mixer.init()
    nextline = pygame.mixer.music.load('talk.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    pygame.quit()
    os.remove("talk.mp3")

paused = False
#mic setup
mic_name = "USB PnP Sound Device: Audio (hw:" #you may need to manually configure mic
sample_rate = 48000
chunk_size = 2048
r = sr.Recognizer()
mic_list = sr.Microphone.list_microphone_names()
for i, microphone_name in enumerate(mic_list):
    print(microphone_name)
    if mic_name in microphone_name:
        device_id = i
#device_id = 0
print('m = FaceRecognition_DLIB()') #facerec setup
m = FaceRecognition_DLIB()
m.learn_face_group()
m.learn_unknown_faces_group()

bad_words = ['jabroni', 'doofus', 'dumbass', 'pinhead', 'penis', 'vagina',
             'cock', 'shit', 'fuck', 'rectal', 'viagra', 'pee', 'HIV',
             'ford', 'rape', 'urine', 'asparagus']  # the bot will not say phrases containing these words

name = "User"  # we want the user's name

bot = ChatBot(  # defining properties and attributes
    'spork',
    read_only=True,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',  # this defines the database the bot will use to learn
    preprocessors=[  # these will clean up the text so the bot can understand
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    logic_adapters=[
        {
            'import_path': 'camera_adapter.CameraAdapter'
        },
        {
            'import_path': 'similar_response.SimilarResponseAdapter',
            'input_text': 'what\'s 9 + 10',
            'output_text': ('21. Hahaha I am kidding. 9 + 10 = 19'),
            'similarity_threshold': 0.7
        },
        
        {
            'import_path': 'similar_response.SimilarResponseAdapter',
            'input_text': 'Are you ready',
            'output_text': ('Yes, I am ready. Let us begin the demonstration.'),
            'similarity_threshold': 0.9
        },
        {
            'import_path': 'similar_response.SimilarResponseAdapter',
            'input_text': 'What is your name?',
            'output_text': 'I am Congenial A.I. You can call me whatever you like',
            'similarity_threshold': 0.7
        },
        {
            'import_path': 'NewBestMatch.NewBestMatchAdapter',  # if the bot can't think of a response, it will give a
            'default_response': 'Sorry, I don\'t quite understand.',  # default response
            'maximum_similarity_threshold': 0.35,
            'excluded_words': bad_words
        },

        'chatterbot.logic.MathematicalEvaluation',  # this gives the bot the ability to solve math equations
        {
           'import_path': 'mood_adapter.MoodAdapter'
         },
        {
            'import_path': 'newtime_adapter.NewTimeLogicAdapter',  # this gives the bot the ability to tell time
        },#,
        {
            'import_path': 'search_adapter.SearchAdapter',  # adds search on command
        }

    ],
    database_url='sqlite://database.sqlite3'
)
print('Starting bot. . . . ')

print('Chatbot is now active')
print('Seeking user')
tts = "seeking user"
text2speech(tts)
newUser = False

#User search routine: the chatbot will try to rotate to find the user via camera + sound

if __name__ == '__main__': #this sets up interfacing with the arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    time.sleep(2)
    ser.write(b"6\n")
    
    while True:
        m.RecFace()
        print("name: ", m.name)
        print("Seeking user . . .")
        time.sleep(1)

        if m.name == None:
            print('User has not been located')
            
        else:
            print('user has been located. stopping. . . ')
            ser.write(b"7\n") #write to the pi
            #time.sleep(2)
            tts = ("I see you.")
            text2speech(tts)
            if m.name == 'unknown':
                tts = ("I do not recognize you.")
                text2speech(tts)
                newUser = True
            break
#end of user search

firstloop = True
time.sleep(5)
while True:
    try:
        starttimer = time.time()
        with sr.Microphone(device_index = device_id, sample_rate = sample_rate,
                    chunk_size = chunk_size) as source:
            r.adjust_for_ambient_noise(source)
            endtimer = time.time()
            print(endtimer - starttimer)
            print("Speak into the mic")
            if firstloop == True:
                if newUser == True:
                    tts = ("Please give me your name.")
                    text2speech(tts)
                    
                    while True:
                        audio = r.listen(source)
                        givenName = r.recognize_google(audio)
                        print(name + ': ' + givenName)
                            
                        tts = ("You said " + givenName +". Is that correct? Yes or no?")
                        text2speech(tts)
                        validName = False
                            
                        while True:
                                audio = r.listen(source)
                                choice = r.recognize_google(audio)  # tts option
                                print(name + ': ' + choice)
                                if choice == 'yes':
                                    validName = True
                                    break
                                if choice == 'no':
                                    givenName = "unknown"
                                    tts = ("Please repeat your name.")
                                    text2speech(tts)
                                    break
                                else:
                                    tts = ("I did not understand. Yes or no?")
                                    text2speech(tts)
                            
                        if validName == True:
                            break
                            
                    tts = ("Understood. Please hold still for the camera.")
                    text2speech(tts)          
                    m.inputname = givenName
                    name = givenName
                    m.learn_face()
                    print("Writing to file!")
                    m.RecFace()
                    print("name: ", m.name)
                    validName == False
                    name = givenName       
                else:
                    name = m.name   
                tts = ("Hello, " + name + ". You can speak now.")
                text2speech(tts)
                firstloop = False
            audio = r.listen(source)
            request = r.recognize_google(audio)
            print(name + ': ' + request)
                    
        if request == "Bye" or request == 'bye' or request == 'goodbye' or request == 'Goodbye' or request == 'shut up':
            print('Chatbot: Bye. Shutting down. . . .')  # if you say these things to the bot, it will quit
            tts = ('Bye. Shutting down')
            text2speech(tts)
            break
        elif request == "what is my name" or request == "who am i":
            print('Chatbot: Your name is' + name + '.')
            tts = ('Your name is ' + name + '.')
            text2speech(tts)
        elif request == "pause":
             tts = ("I am paused. I will resume when you say unpause.")
             text2speech(tts)
            # paused = True
             while True:
                 try:
                     with sr.Microphone(device_index = device_id, sample_rate = sample_rate,
                     chunk_size = chunk_size) as source:
                         r.adjust_for_ambient_noise(source)
                         audio = r.listen(source)
                         freeze = r.recognize_google(audio)
                         if freeze == "unpause":
                           #  paused = False
                             break
                         else:
                             print("Standing by")
                 except sr.UnknownValueError:
                     print('standing by')
                     continue
             print('Chatbot: Resuming operation. You may speak now.')
             tts = ("Resuming operation. You may speak now.")
             text2speech(tts)

        else:
            response = bot.get_response(request)
            print("Chatbot: ", end='')
            print(response)
            tts = (str(response))
            text2speech(tts)
                
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
    except sr.UnknownValueError:
            print('Chatbot: I couldn\'t understand you. Can you repeat that?') 
            text2speech('I couldn\'t understand you. Can you repeat that?')
            continue
       