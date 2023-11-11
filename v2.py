import speech_recognition as sr
import pyrebase
import langcodes

config = {
  "apiKey": "AIzaSyClastSM-d8sm0AWajY03OnezmkPVCrO04",
  "authDomain": "fir-topythonsample.firebaseapp.com",
  "projectId": "fir-topythonsample",
  "storageBucket": "fir-topythonsample.appspot.com",
  "databaseURL":"https://fir-topythonsample-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "messagingSenderId": "936536554705",
  "appId": "1:936536554705:web:f4d0b91b36e8174d7e99f0",
  "measurementId": "G-JL324VD9EC"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()


recognizer = sr.Recognizer()

count = 0

def find_user(text):
    users = database.child("Users").order_by_child("Text").equal_to(text.lower()).get()
    if not len(users.each()):  
            print("User not found")  ###
    else:
        for user in users.each():
            if (user.val()!=""):
                print("Welcome, {}" .format(user.val()["Name"]))   
        
def recognize_audio(recorded_audio, lang_code):
    try:
        print("Recognizing the text")
        text = recognizer.recognize_google(
                recorded_audio, 
                language=lang_code
        )

        print("Decoded Text : {}".format(text))
        return text 
    except sr.exceptions.UnknownValueError:
        print("Couldn't comprehend. Please speak clearly")
       
    except Exception as ex:
        print(ex)
        
    

''' recording the sound '''

def record(lang_code):
    
    with sr.Microphone() as source:
        print("Adjusting noise ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Recording for 4 seconds")
        try:
            recorded_audio = recognizer.listen(source, timeout=4) 
            print("Done recording")
            return recognize_audio(recorded_audio, lang_code)
               
        except sr.exceptions.WaitTimeoutError:
            print("Recording Time out. Please speak while recording")
              
        except Exception as ex:
            print(ex)
            
def find_lang():
    for i in range(0,3):
        print(f"Recording {i+1}")
        lang = record("en-US") 
        if(lang):
            return lang

lang = find_lang()
if(lang):
    for i in range(0,5):
        print(f'Recording {i+1}')
        try: 
            code_word = record(langcodes.find(lang).language)
            if(code_word):
                find_user(code_word)
                break
        except LookupError:
            print("No such language found")
            if(count<3):
                count+=1
                lang = find_lang()
            else:
                print("Language not supported")
                break
                

