from EmotionDetect_HaarCascade import EmotionDetect_HaarCacasde

global mood


def start():
    global mood
    mood = EmotionDetect_HaarCacasde()
    mood.model_loading()
    mood.emotion_detect_run()

#  print("Last Emotion Detected:", m.emotion)
#  print("Last Emotion Detected Weights:", m.emotionWeights)
