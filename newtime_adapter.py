from datetime import datetime
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from difflib import SequenceMatcher

class NewTimeLogicAdapter(LogicAdapter):
    """
    The TimeLogicAdapter returns the current time.
    Modified from the original Time Logic Adapter. Uses Sequence Matcher instead of Naive Bayes Classification.

    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        phrase = str(statement)
        listen = 'What time is it?'
        ratio = SequenceMatcher(None, phrase, listen).ratio()
        listen = 'Can you tell me the time?'
        if ratio < SequenceMatcher(None, phrase, listen).ratio():
            ratio = SequenceMatcher(None, phrase, listen).ratio()


        if ratio >= .7:
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        now = datetime.now()
        response = Statement(text='The current time is ' + now.strftime('%I:%M %p'))
        response.confidence = 1
        return response
