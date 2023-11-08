import pyrebase
# from speech2text import text

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

data = [{"Name": "Ridhi", "Text": "enjoy the rhythm"},
        {"Name": "Valarmathi", "Text": "looking to help you"},
        {"Name": "Selvi", "Text": "welcome to the world"},
        {"Name": "Franc", "Text": "trial is good"}]

database.child("Users").set(data)
