import speech_recognition as sr

def convert_speech_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        print("about to convert_speech_to_text")
        print(text)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        raise Exception(f"API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing audio: {str(e)}")

