"""
This code is for obtaining voice recognition results from google cloud.
"""
import speech_recognition as sr
import sqlite3 as sq3

GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "strong-zephyr-304715",
  "private_key_id": "69114b39b4bdaa9cafc7465b5124e6611ca5f806",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC1cLDELkKnVdnw\n2F62GcEY3HhtxjwEFB+TtwIbgFEQywMb5jn6Pq2T6WPwTHIBZXM5wzWaqA14b+Yb\naEB7xegTQiQqPBBkXswCEZFKSiPrftL5q3o7quzTssrrGCqNmV9+7P5RxJkL9+Di\n02GSsxKTMQrBpjgSBGV0Qs9y0/6pe/8pg0J1hLwyEqbtbTRdAl3mWcMJBMsQ/KVc\nABVj5YJv6Y1N1ab9duGYVdKsXEz4MvXLVE8bUuqLnnm0hdgL0OpYbBdb4P2gvegI\nknV7AsjfdURI/LlSl2SeuMquuXaRB0W+zVtrMGVew3gehrDYOcbAk6nGhiPadq0f\naUCfjLdpAgMBAAECggEAA14BRc7G+WSIPCZD0bTWJtA2ovDmHbxC3sKrdRezSXC/\nEMY7xrdhkMhozKWaiwiXNBf5l3Jtd5H6DwGnCrUAStU0Jx2Av2AcAKDTVbHdC0qJ\n/0ytosxYA1DC38yNw514Tnp2+M0Bex2hTIxYN/j/TACBvtjHGxx+RoNT5sFk7T/C\nFFkdBIxXYRFvubYTrMpTR6JkHCzxBypkBdq59lS7iI3zzz/4tPxb7deruvcB9kK7\n2/HB+jaPAZ+LbVRuZYhS69GbNenW7zs42eO0F31TgsY4xDlKi+7aEGXAy5vSeYWy\nknvXA0S7gAHYYR6Rw1sq/FKrVCYQXTNlhz1jQkhOYQKBgQDqKzRKiGkwT8dpdNf3\nNWyheSQEZwyv3MKYCuc9umg4YALap8hI9kCnmLvmI7l83Br84+L/IowRli/IyE5t\nenYP9S+KrXxL44p9n67no3nPXR9EOKue3ak8SRgV2NsFppTbaILKzdceZD3+W+ub\nLBb0Z5e8DzG4P27V1BdAwQf+WQKBgQDGWwnM5qo3clsR3rV3fIPHEIJBpPUrVgbC\nfbg3eO6cP3krh1CtpwHVjjww6YNp6pbDWeu5iQCvI7pZY2Ezvp1tlyrc3wEdfc//\naIJQmnWpqYrFMUxCCHKayOfcl9tfHDCempyMfMcKTx2S0KqUc5VOHRGugRmxYKwF\nrVFeSaP/kQKBgQDB9CsJmNbXRxz6AednQH7Ld9UXOGtPtmAPIujJPf5Yw11Z0iKY\nHC8NIfpv8iMOghhwYih//hNZ9bV6bj5Xe1kSeph4Gp2bFcp9pqduAP9Be/YLwYyU\ntzAXWMt0PPucQI+G85dxdvC4oXqflW8eRXR11t/cyhD6dL/OqC7iWX/PcQKBgQCY\nVfqk3tIDW1QN2VjMt1gNXeRrveB8s8jlPeBo2fuHDEhm4blYZFbISEB54B0JDx1S\nUpDzIQDhgTLwy54vO0l0jRBiKPKWT7WalgzfEoEjGA53e3DxlcNOlNVdWVMlLGU6\nqctpKbtDc5dm1dLryAj2wOR/fK7axz/V7FH9c9j7wQKBgDnr3iHq+x+SsESGty8l\nRlpKOPilpdzwbtMnngVZhBUzsDUeyBB8XfFqS7znZEfZVDBPc4UEh6SrypEUfa3W\nckuiwdImLYBEXkkk9nlG2B3jin9TnOKjRpvglkLpNl/Eir9FFokds18bfskfWi5h\ne11e0/w3d3/n8koelfW35pUk\n-----END PRIVATE KEY-----\n",
  "client_email": "tarp-726@strong-zephyr-304715.iam.gserviceaccount.com",
  "client_id": "107869845586705771064",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/tarp-726%40strong-zephyr-304715.iam.gserviceaccount.com"
} """

connection = sq3.connect("Parameters.db")
cursor = connection.cursor()

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
                        if "track" in text:
                            if test[0][1] == 0:
                                cursor.execute("UPDATE parameters SET status = 1 WHERE parameter = 'track'")
                            else:
                                cursor.execute("UPDATE parameters SET status = 0 WHERE parameter = 'track'")
                            connection.commit()
                            """print("Track")
                            cursor.execute("SELECT * FROM parameters")
                            print(cursor.fetchall())"""
                            break
                        elif "auto" in text:
                            if test[1][1] == 0:
                                cursor.execute("UPDATE parameters SET status = 1 WHERE parameter = 'autoOff'")
                            else:
                                cursor.execute("UPDATE parameters SET status = 0 WHERE parameter = 'autoOff'")
                            connection.commit()
                            """print("autoOff")
                            cursor.execute("SELECT * FROM parameters")
                            print(cursor.fetchall())"""
                            break
                        elif "camera" in text:
                            if test[2][1] == 0:
                                cursor.execute("UPDATE parameters SET status = 1 WHERE parameter = 'userView'")
                            else:
                                cursor.execute("UPDATE parameters SET status = 0 WHERE parameter = 'userView'")
                            connection.commit()
                            """print("userView")
                            cursor.execute("SELECT * FROM parameters")
                            print(cursor.fetchall())"""
                            break
                        elif "default" in text:
                            if test[3][1] == 0:
                                cursor.execute("UPDATE parameters SET status = 1 WHERE parameter = 'default'")
                            else:
                                cursor.execute("UPDATE parameters SET status = 0 WHERE parameter = 'default'")
                            connection.commit()
                            """print("default")
                            cursor.execute("SELECT * FROM parameters")
                            print(cursor.fetchall())"""
                            break
                    except sr.RequestError as exception:
                        print("Could not request results from Google Cloud Speech service; {0}".format(exception))
                    except sr.UnknownValueError:
                        print("Unable to understand sentence")

        except sr.RequestError as exception:
            print("Could not request results from Google Cloud Speech service; {0}".format(exception))
        except sr.UnknownValueError:
            print("Unable to understand sentence")
