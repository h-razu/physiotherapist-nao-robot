# -*- coding: utf-8 -*-
import time
from naoqi import ALProxy
from groq_wrapper import get_groq_response

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
    'relaxed': "That's great to hear. Relaxation means your body is responding well.",
    'sore': "That's normal. Some muscle soreness happens after therapy.",
    'better': "Wonderful! Glad you're feeling better.",
    'pain': "I understand. Some pain is expected, but it should go away soon.",
    'tired': "That means you’ve worked hard. Good job!",
    'hard': "That's okay! Some exercises are more difficult at first.",
    'challenging': "Challenging exercises help you improve. We’ll keep working on it.",
    'stretches': "Stretches can be tough. I can show easier ones.",
    'balance': "Balance can be tricky. We'll improve it step by step.",
    'squats': "Squats take practice. We can try a modified version next time.",
    'yes': "Okay! I’ll prepare a modified version for you.",
    'variation': "Sure! I’ll show you a variation to make it easier.",
    'try': "Great! Let's try it together.",
    'show': "I'll show you how to do a simpler version.",
    'home': "Yes, you can do these exercises at home as well.",
    'same': "Please do the same exercises at home, but gently.",
    'practice': "Keep practicing at home for better results.",
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


def get_groq_advice(word):
    # Prompt for each intent
    prompts = {
    'sore': "A patient is feeling sore after doing some exercises. What should I say to give them some advice? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'pain': "A patient feels pain after doing some exercise. What should I say to give them advice? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'tired': "A patient feels tired after the session. What should I say to give them advice? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'hard': "A patient found the exercises hard. What should I say to give them advice? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'challenging': "A patient found the exercises challenging. What should I say to give them advice? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'balance': "A patient is working on balance exercises. What should I say to encourage them? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'squats': "A patient is doing squats. What should I say to help them improve? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'relaxed': "A patient feels relaxed after the session. What should I say to keep them motivated? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'better': "A patient feels better after the session. What should I say to encourage them further? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'thank': "A patient thanked me for the session. What should I say in response? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'stretches': "A patient is doing stretches. What should I say to guide and motivate them? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'variation': "A patient is asking for a variation of the exercise. What should I say to offer a helpful and safe alternative? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'yes': "A patient responded positively and is ready to try something new. What should I say to support and guide them? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'try': "A patient wants to try a different version of the exercise. What should I say to encourage and suggest a variation? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'show': "A patient is asking me to show them a new exercise variation. What should I say to introduce a safe and effective variation? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'home': "A patient wants to know if they can do the exercises at home. What should I say to guide them? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'same': "A patient asks if they can repeat the same exercises at home. What should I say to guide them? It should not be long, max 5 sentences. should be in one paragraph. just the response",
    'practice': "A patient wants to practice the exercises outside of our sessions. What should I say to encourage and guide them? It should not be long, max 5 sentences. should be in one paragraph. just the response",
}


    prompt = prompts.get(word, "I'm not sure how to respond to this input. Please provide more details.")

    # Get advice from Groq
    return get_groq_response(prompt)


def initial_feedback_session(IP, PORT):
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    animated_speech = ALProxy("ALAnimatedSpeech", IP, PORT)
    speech_recognition = ALProxy("ALSpeechRecognition", IP, PORT)
    dialog = ALProxy("ALDialog", IP, PORT)
    memory = ALProxy("ALMemory", IP, PORT)

    state = 'start'
    while state:
        prompt, expected_intent = CONVO_FLOW[state]
        tts.say(prompt)
        recognized_word = get_voice_input(speech_recognition, memory)
        print(recognized_word)

        if not recognized_word:
            print("No input detected. Waiting silently.")
            time.sleep(5)
            continue  

        # React to the word
        say_reaction(tts, recognized_word)
        advices = get_groq_advice(recognized_word)
        # Determine intent
        intent = get_intent(recognized_word)
        if intent == expected_intent:
            # Show a waiting message while waiting for Groq response
            tts.say("Please wait a moment while I get some advice...")
            time.sleep(5)

           # Get advice from Groq
            print(advices)
            print("hi")
            tts.say(str(advices))
            # if advices:
            #     for sentence in advices:
            #         if isinstance(sentence, str) and sentence.strip():
            #             time.sleep(1)
            #             tts.say(sentence)
            # else:
            #     tts.say("Sorry, I don't have anything to say at the moment.")




            state = intent

            # Check if this is the end of conversation
            if CONVO_FLOW[state][1] is None:
                # Speak the final message
                tts.say(CONVO_FLOW[state][0])
                break  # Exit the loop
        else:
            tts.say("Sorry, I didn't catch that. Could you repeat?")

    tts.say("Thank you for your feedback.")
