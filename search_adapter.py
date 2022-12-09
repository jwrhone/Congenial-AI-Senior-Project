from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from EmotionDetect_HaarCascade import EmotionDetect_HaarCacasde
from difflib import SequenceMatcher
import time
import serial



class SearchAdapter(LogicAdapter):
    """
       The search adapter will make the software go into user search mode when commanded.


       """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from chatterbot.conversation import Statement

    def can_process(self, statement):
        phrase = str(statement)
        listen = 'enter search mode'
        ratio = SequenceMatcher(None, phrase, listen).ratio()

        if ratio >= .7:
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        
        
        #if __name__ == '__main__': #this sets up interfacing with the arduino
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()
        time.sleep(2)
        ser.write(b"6\n")
        print("writing to pi!")
        while True:
            mood = EmotionDetect_HaarCacasde() #use mood recognition for now to find user
            mood.model_loading()
            mood.emotion_detect_run()
            print("Seeking user . . .")
            time.sleep(1)
        
            if mood.emotion == None:
                print('User has not been located') 
            else:
                print('user has been located. stopping. . . ')
                ser.write(b"7\n") #write to the pi
                
                break
            
        response = Statement(text='I am now facing you.')
        response.confidence = 1
        return response

