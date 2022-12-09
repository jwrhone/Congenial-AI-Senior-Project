from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from EmotionDetect_HaarCascade import EmotionDetect_HaarCacasde
from difflib import SequenceMatcher
global mood


class CameraAdapter(LogicAdapter):
    """
       The CameraAdapter takes data from facial recognition for the chatbot to use.


       """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from chatterbot.conversation import Statement

    def can_process(self, statement):
        phrase = str(statement)
        listen = 'Can you see me?'
        ratio = SequenceMatcher(None, phrase, listen).ratio()

        if ratio >= .7:
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        global mood

        mood = EmotionDetect_HaarCacasde()
        mood.model_loading()
        mood.emotion_detect_run()

        if mood.emotion == None:
            response = Statement(text='No, I cannot see you.')
            response.confidence = 1
            return response
        else:
            emotion = 'Yes, I can see you. You look ' + str(mood.emotion) + '.'
            response = Statement(text=emotion)
            response.confidence = 1
            return response

