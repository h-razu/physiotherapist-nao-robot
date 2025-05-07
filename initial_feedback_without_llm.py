# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time

# Define keyword-based intents
INTENTS = {
    'report_feeling': ['relaxed', 'sore', 'better', 'pain', 'tired'],
    'exercise_difficulty': ['hard', 'challenging', 'stretches', 'balance', 'squats'],
    'request_variation': ['yes', 'variation', 'try', 'show'],
    'ask_home_exercise': ['home', 'same', 'practice'],
    'thanks': ['thank', 'session'],
}

# Define NAO’s extra reaction based on specific keywords
RESPONSES = {
    # report_feeling
    'relaxed': "That's great to hear. Relaxation means your body is responding well.",
    'sore': "That's normal. Some muscle soreness happens after therapy.",
    'better': "Wonderful! Glad you're feeling better.",
    'pain': "I understand. Some pain is expected, but it should go away soon.",
    'tired': "That means you’ve worked hard. Good job!",

    # exercise_difficulty
    'hard': "That's okay! Some exercises are more difficult at first.",
    'challenging': "Challenging exercises help you improve. We’ll keep working on it.",
    'stretches': "Stretches can be tough. I can show easier ones.",
    'balance': "Balance can be tricky. We'll improve it step by step.",
    'squats': "Squats take practice. We can try a modified version next time.",

    # request_variation
    'yes': "Okay! I’ll prepare a modified version for you.",
    'variation': "Sure! I’ll show you a variation to make it easier.",
    'try': "Great! Let's try it together.",
    'show': "I'll show you how to do a simpler version.",

    # ask_home_exercise
    'home': "Yes, you can do these exercises at home as well.",
    'same': "Please do the same exercises at home, but gently.",
    'practice': "Keep practicing at home for better results.",

    # thanks
    'thank': "You're very welcome!",
    'session': "I'm glad I could help in today's session.",
}

# Dialogue steps
CONVO_FLOW = {
    'start': ("Great job today! How do you feel after the session?", 'report_feeling'),
    'report_feeling': ("Was any particular exercise difficult for you?", 'exercise_difficulty'),
    'exercise_difficulty': ("I can modify it to make it easier. Would you like to see a variation?", 'request_variation'),
    'request_variation': ("I'll show you a variation. Would you like to do it now or later?", 'ask_home_exercise'),
    'ask_home_exercise': ("Yes, but take it slow. If you feel any sharp pain, stop and rest.", 'thanks'),
    'thanks': ("You're welcome! Keep up the good work. See you next time!", None),
}

# Create combined vocabulary for recognition
vocabulary = list(set([word for kw in INTENTS.values() for word in kw]))


def get_voice_input(speech_recog, memory):
    try:
        memory.removeData("WordRecognized")
    except RuntimeError:
        pass  # It may not exist yet

    speech_recog.pause(True)
    speech_recog.setVocabulary(vocabulary, False)
    speech_recog.subscribe("MyApp")
    speech_recog.pause(False)

    print("Listening...")

    for i in range(20):  # max 10 seconds
        time.sleep(0.5)
        try:
            data = memory.getData("WordRecognized")
        except RuntimeError:
            data = None  # If the key doesn't exist yet

        if data and isinstance(data, list) and len(data) > 1 and data[1] > 0.4:
            word = data[0].lower()
            print("Heard:", word)
            speech_recog.unsubscribe("MyApp")
            try:
                memory.removeData("WordRecognized")
            except RuntimeError:
                pass
            return word

    speech_recog.unsubscribe("MyApp")
    return ""

def get_intent(word):
    for intent, keywords in INTENTS.items():
        if word in keywords:
            return intent
    return 'unknown'

def say_reaction(tts, word):
    if word in RESPONSES:
        tts.say(RESPONSES[word])
        print("NAO:", RESPONSES[word])



def initial_feedback_session(IP, PORT):
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    speech_recognition = ALProxy("ALSpeechRecognition", IP, PORT)

    memory = ALProxy("ALMemory", IP, PORT)

    state = 'start'
    while state:
        prompt, expected_intent = CONVO_FLOW[state]
        tts.say(prompt)
        recognized_word = get_voice_input(speech_recognition, memory)
        print(recognized_word)

        if not recognized_word:
            print("No input detected. Waiting silently.")
            time.sleep(1)
            continue

        # React to the word
        say_reaction(tts, recognized_word)

        # Determine intent
        intent = get_intent(recognized_word)
        if intent == expected_intent:
            state = intent

            # Check if this is the end of conversation
            if CONVO_FLOW[state][1] is None:
                # Speak the final message
                tts.say(CONVO_FLOW[state][0])
                break  # Exit the loop
        else:
            tts.say("Sorry, I didn't catch that. Could you repeat?")

    tts.say("Thank you for your feedback.")

    

    