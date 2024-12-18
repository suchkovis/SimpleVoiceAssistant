
import queue
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time
from openai import OpenAI
from interpreter import interpreter
import pyttsx3
from some_funcs import Usefull_functions
#from ollama import chat
#gpt-4o-mini
class VoiceLogic:
    def __init__(self, vosk_model_path, api_key, base_url = 'https://api.rockapi.ru/openai/v1',
                 wake_word="привет", stop_phrase="хватит", language='ru', print_status_interpreter = True,
                 model_for_interpreter="gpt-3.5-turbo", model_for_process = "gpt-3.5-turbo"):
        self.state = "waiting"  # Possible states: waiting, listening, processing, executing
        self.wake_word = wake_word
        self.stop_phrase = stop_phrase
        self.model = Model(vosk_model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.audio_queue = queue.Queue()
        self.is_running = True
        self.collected_text = ""  # Accumulated text during listening
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_type = model_for_process
        self.silence_timer = None  # Timer for detecting silence
        self.default_silence_threshold = 15.0  # Default silence threshold for wake word
        self.active_silence_threshold = 2.0  # Reduced threshold once user starts speaking
        self.silence_threshold = self.default_silence_threshold  # Current threshold
        self.language = language #ru / en
        
        interpreter.offline = False
        interpreter.llm.model = f"openai/{model_for_interpreter}"
        interpreter.llm.api_key = api_key
        interpreter.llm.api_base = base_url
        interpreter.safe_mode = 'off'
        self.print_status_interpreter = print_status_interpreter
        
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1)
        self.use_funcs = Usefull_functions()
        
    def process_audio(self):
        p = pyaudio.PyAudio()
        #TODO: Если плохо работает, нужно поменять значения. Норм работало на frames_ = 8000, .read(4000)
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=3000)
        stream.start_stream()

        while self.is_running:
            data = stream.read(3000, exception_on_overflow=False)
            self.audio_queue.put(data)

            if self.recognizer.AcceptWaveform(data):
                result = self.recognizer.Result()
                self.handle_command(result)

            elif self.state == "listening":
                self.check_silence()  # Check for silence during listening

        stream.stop_stream()
        stream.close()
        p.terminate()

    def handle_command(self, result):
        text = json.loads(result).get("text", "")

        if self.state == "waiting" and self.wake_word in text:
            self.state = "listening"
            wake_word_index = text.find(self.wake_word)
            after_wake_word = text[wake_word_index + len(self.wake_word):].strip()
            self.silence_threshold = self.default_silence_threshold  # Reset to default threshold
            if self.stop_phrase in after_wake_word:
                stop_phrase_index = after_wake_word.find(self.stop_phrase)
                self.collected_text = after_wake_word[:stop_phrase_index].strip()
                self.state = "processing"
                self.processing(self.collected_text)
            else:
                self.collected_text = after_wake_word
                self.reset_silence_timer()
        elif self.state == "listening":
            if self.stop_phrase in text:
                stop_phrase_index = text.find(self.stop_phrase)
                self.collected_text += " " + text[:stop_phrase_index].strip()
                self.state = "processing"
                self.processing(self.collected_text.strip())
            else:
                self.collected_text += " " + text.strip()  # Accumulate recognized text
                self.silence_threshold = self.active_silence_threshold  # Switch to active threshold
                self.reset_silence_timer()

    def check_silence(self):
        if self.silence_timer and time.time() - self.silence_timer >= self.silence_threshold:
            self.state = "processing"
            self.processing(self.collected_text.strip())

    def reset_silence_timer(self):
        self.silence_timer = time.time()
                

    def speak_response(self, answer):
        self.engine.say(answer)
        self.engine.runAndWait()

  
    def processing(self, collected_text):
        # Detect language of the collected text
        print(collected_text)
        #detected_language = "ru" if any("а" <= char <= "я" for char in collected_text.lower()) else "en"
        prompt = self.use_funcs.generate_promt_for_processing(collected_text, self.language)
        response = self.client.chat.completions.create(
            model=self.model_type,
            messages=[{"role": "system", "content": "You are a voice assistant."}, {"role": "user", "content": prompt}]
        )
        #print(f'Detected language: {detected_language}')
        preprocessed_data = self.use_funcs.extract_json(response.choices[0].message.content)
    
        if not preprocessed_data:
            print("Error decoding response from model.")
            print(response.choices[0].message.content)
            self.state = "waiting"
            return
        
        if isinstance(preprocessed_data, list):
            preprocessed_data = preprocessed_data[0].get("output", {})
        if preprocessed_data.get('output') != None:
            preprocessed_data = preprocessed_data.get('output')
        print(f"Preprocessed data: {preprocessed_data}")
        
    
        if preprocessed_data.get("type") == "practical":
            self.execute_command(preprocessed_data.get("task", ""))
        elif preprocessed_data.get("type") == "theoretical":
            print(f"Answer: {preprocessed_data.get('answer', '')}")
            self.speak_response(preprocessed_data.get('answer', ''))
            self.state = "waiting"
        elif preprocessed_data.get("type") == "error":
            print(f"Clarifying question: {preprocessed_data.get('clarifying_question', 'Could you repeat?')}")
            self.speak_response(preprocessed_data.get('clarifying_question', 'Could you repeat?'))
            self.state = "waiting"
        else:
            self.state = "waiting"
    def execute_command(self, command):
        self.state = "executing"
        message = self.use_funcs.generate_prompt_for_interpreter(command, self.language)
        for chunk in interpreter.chat(message, display=False, stream=True):
            if self.print_status_interpreter:
                print(f'Now state of interpterter: {chunk}')
        answer = self.use_funcs.extract_json(interpreter.messages[-1].get('content'))
        if not answer:
            print('Parsing execute result error')
            self.state = "waiting"
            return
        print(f"Result of executing: {answer.get('comments')}")
        self.speak_response(answer.get('comments'))
        self.state = "waiting"
