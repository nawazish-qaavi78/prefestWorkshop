import speech_recognition as sr
import requests # for connection error
import pyrebase

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

def re_run_program(count):
    if(count<5):
        print(f"Recording {count+1}")
        record(count+1)
    else:
        print("Your presence undetected")  ##
        return False
        
def find_user(text):
    try:
        users = database.child("Users").order_by_child("Text").equal_to(text.lower()).get()
        if not len(users.each()):  
            print("User not found")  ###
        else:
            for user in users.each():
                if (user.val()!=""):
                    print("Welcome, {}" .format(user.key()))
                    database.child("Stages").update({"stage1":1})
                    return True
            return False
    except requests.exceptions.ConnectionError:
        print("Connection Failed! Check Your Internet Connection")
        return False
    except Exception as ex:
        print(ex)
        return False
    
        
        
def recognize_audio(recorded_audio, count):
    try:
        print("Recognizing the text")
        text = recognizer.recognize_google(
                recorded_audio, 
                language="en-US"
        )

        print("Decoded Text : {}".format(text))
        return find_user(text)
         
    except sr.exceptions.UnknownValueError:
        print("Couldn't comprehend. Please speak clearly")
        re_run_program(count)
    except sr.exceptions.RequestError:
        print("Failed!!! Please check your internet connection")
        return False
    except Exception as ex:
        print(ex)
        return False
           

''' recording the sound '''

def record(count):
    
    with sr.Microphone() as source:
        print("Adjusting noise ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Recording for 4 seconds")
        try:
            recorded_audio = recognizer.listen(source, timeout=4) 
            print("Done recording")
            return recognize_audio(recorded_audio, count)
               
        except sr.exceptions.WaitTimeoutError:
            print("Recording Time out. Please speak while recording")
            re_run_program(count+1)
            
        except sr.exceptions.RequestError:
            print("Failed!!! Please check your internet connection")
            return False
            
        except Exception as ex:
            print(ex)
            return False
        




