import speech_recognition as sr
import pyrebase

count=1

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

''' recording the sound '''

def main(c):
    
    with sr.Microphone() as source:
        print("Adjusting noise ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Recording for 4 seconds")
       
        recorded_audio = recognizer.listen(source, timeout=4) # Listening timeout error raises while waiting for the text to start
        print("Done recording")
      
            

    ''' Recorgnizing the Audio '''
    try:
        print("Recognizing the text")
        text = recognizer.recognize_google(
                recorded_audio, 
                language="en-US"
        )
        # text="Google"
        print("Decoded Text : {}".format(text))
        # x=text.split()
        # print(x)
        users = database.child("Users").order_by_child("Text").equal_to(text.lower()).get()
        
        if not len(users.each()):  
            print("User not found")  ###
        else:
            for user in users.each():
                if (user.val()!=""):
                    print("Welcome, {}" .format(user.val()["Name"]))   


        
    except Exception as ex:
        if(c<5):
            print(f"Recording {c+1}")
            main(c+1)
        else:
            print("Your presence undetected")  ##
main(count)
