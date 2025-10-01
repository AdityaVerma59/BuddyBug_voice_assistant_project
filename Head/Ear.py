import speech_recognition as sr

def takeCommand(duration=7):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("🔎 Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            return query
        except sr.WaitTimeoutError:
            # No speech detected → just restart listening
            print("⏳ No speech detected, listening again...")
            return ""
        except sr.UnknownValueError:
            print("😕 Couldn’t understand, please repeat...")
            return ""
        except sr.RequestError:
            print("❌ Network error")
            return ""
