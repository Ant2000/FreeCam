"""
This code is for obtaining voice recognition results from google cloud.
"""
import speech_recognition as sr
import sqlite3 as sq3

with open("./key.json", 'r') as f:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

connection = sq3.connect("Parameters.db")
cursor = connection.cursor()
cursor.execute("UPDATE parameters SET status = 1 WHERE parameter = 'track'")
cursor.execute("UPDATE parameters SET status = 1 WHERE parameter = 'userView'")
cursor.execute("UPDATE parameters SET status = 1 WHERE parameter = 'autoOff'")
cursor.execute("UPDATE parameters SET status = 0 WHERE parameter = 'default'")
connection.commit()

# cursor.execute("""CREATE TABLE IF NOT EXISTS
# parameters(parameter TEXT PRIMARY KEY, status INTEGER)""")
# cursor.execute("INSERT INTO parameters VALUES ('track', 1)")
# cursor.execute("INSERT INTO parameters VALUES ('autoOff', 1)")
# cursor.execute("INSERT INTO parameters VALUES ('autoOff', 1)")
# cursor.execute("INSERT INTO parameters VALUES ('default', 0)")

r = sr.Recognizer()

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    while True:
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=2)
        try:
            text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
            print(text)
            if "system" in text:
                cursor.execute("SELECT * FROM parameters")
                test = cursor.fetchall()
                print(test)
                while True:
                    print("Command: ")
                    audio = r.listen(source, phrase_time_limit=2)
                    try:
                        text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
                        text = text.lower()
                        if "track" in text:
                            if test[0][1] == 0:
                                cursor.execute("UPDATE parameters SET status = 1 WHERE parameter = 'track'")
                            else:
                                cursor.execute("UPDATE parameters SET status = 0 WHERE parameter = 'track'")
                            connection.commit()
                            print("Track")
                            cursor.execute("SELECT * FROM parameters")
                            print(cursor.fetchall())
                            break
                        elif "auto" in text:
                            if test[1][1] == 0:
                                cursor.execute("UPDATE parameters SET status = 1 WHERE parameter = 'autoOff'")
                            else:
                                cursor.execute("UPDATE parameters SET status = 0 WHERE parameter = 'autoOff'")
                            connection.commit()
                            print("autoOff")
                            cursor.execute("SELECT * FROM parameters")
                            print(cursor.fetchall())
                            break
                        elif "camera" in text:
                            if test[2][1] == 0:
                                cursor.execute("UPDATE parameters SET status = 1 WHERE parameter = 'userView'")
                            else:
                                cursor.execute("UPDATE parameters SET status = 0 WHERE parameter = 'userView'")
                            connection.commit()
                            print("userView")
                            cursor.execute("SELECT * FROM parameters")
                            print(cursor.fetchall())
                            break
                        elif "default" in text:
                            if test[3][1] == 0:
                                cursor.execute("UPDATE parameters SET status = 1 WHERE parameter = 'default'")
                            else:
                                cursor.execute("UPDATE parameters SET status = 0 WHERE parameter = 'default'")
                            connection.commit()
                            print("default")
                            cursor.execute("SELECT * FROM parameters")
                            print(cursor.fetchall())
                            break
                    except sr.RequestError as exception:
                        print("Could not request results from Google Cloud Speech service; {0}".format(exception))
                    except sr.UnknownValueError:
                        print("Unable to understand sentence")

        except sr.RequestError as exception:
            print("Could not request results from Google Cloud Speech service; {0}".format(exception))
        except sr.UnknownValueError:
            print("Unable to understand sentence")
