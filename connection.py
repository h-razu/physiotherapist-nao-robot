from naoqi import ALProxy

def connect(NAO_IP, PORT):
    tts = ALProxy("ALTextToSpeech", NAO_IP, PORT)
    motion = ALProxy("ALMotion", NAO_IP, PORT)

    motion.wakeUp()
    tts.setLanguage("English")
    text = "Hello!, I am Thera NAO. Nice to meet you."
    tts.say(text)
    print("Connected")


def disconnect(NAO_IP, PORT):
    tts = ALProxy("ALTextToSpeech", NAO_IP, PORT)
    motion = ALProxy("ALMotion", NAO_IP, PORT)

    motion.wakeUp()
    tts.say("Thera NAO Sign Out")
    motion.rest()
    print ("Exit Successful")



#physical robot
NAO_IP = "172.18.16.30"
PORT = 9559

# #virutal robot
# NAO_IP = "127.0.0.1"
# PORT = 58590

connect(NAO_IP, PORT)
# disconnect(NAO_IP, PORT)