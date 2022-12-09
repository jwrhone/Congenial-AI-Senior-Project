from difflib import SequenceMatcher

from chatterbot.logic import LogicAdapter


class SimilarResponseAdapter(LogicAdapter):
    """
    Return a specific response to a phrase that's similar.
    Modification of the specific response adapter. Uses sequence matcher to determine response confidence.

    :kwargs:
        * *input_text* (``str``) --
          The input text that triggers this logic adapter.
        * *output_text* (``str``) --
          The output text returned by this logic adapter.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from chatterbot.conversation import Statement

        self.input_text = kwargs.get('input_text')
        output_text = kwargs.get('output_text')
        self.similarity_threshold = kwargs.get('similarity_threshold')
        self.response_statement = Statement(text=output_text)

    def can_process(self, statement):
        phrase = str(statement)
        ratio = SequenceMatcher(None, phrase, self.input_text).ratio()
        if ratio > self.similarity_threshold:
            return True
        else:
            return False

    def process(self, statement, additional_response_selection_parameters=None):
        phrase = str(statement)
        ratio = SequenceMatcher(None, phrase, self.input_text).ratio()
        self.response_statement.confidence = ratio

        return self.response_statement
