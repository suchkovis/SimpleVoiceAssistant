
SimpleVoiceAssistant
=========================

SimpleVoiceAssistant is a Python-based voice assistant that uses Vosk for speech recognition, OpenAI for processing, and Pyttsx3 for text-to-speech capabilities. This project is designed to enable natural interaction via voice commands, supporting both practical and theoretical queries.

Installation:
-------------
* Clone the repository: `git clone https://github.com/suchkovis/SimpleVoiceAssistant`
* Navigate to the project directory: `cd SimpleVoiceAssistan`
* Install the required dependencies: `pip install -r requirements.txt`
* [Download](https://github.com/kercre123/vosk-models) Vosk model files as per the project requirements. 

Usage:
------
* Run the main script: `python main_ui.py`
* Speak the wake word followed by a command (by default — "привет").
* Listen to the assistant's response.

Features:
---------
* Wake word detection to start listening.
* Handles both practical (task execution) and theoretical (question answering) queries.
* Text-to-speech responses with adjustable parameters.
* Flexible language support (default: Russian).

Author:
-------
Svyatoslav Artemyev, Ivan Suchkov

Example:
--------
Here is a basic example of how to call this project from Python:

```python
from main_ui import *

vosk_model_path = "path_to_vosk_model" #for example, "vosk-model-small-ru-0.22"
api_key = "your_openai_api_key" #API key here
language = "ru" #or "en", but remember, thar vosk model must have same language
wake_word = "привет"

app = QApplication(sys.argv)
logic = VoiceLogic(vosk_model_path, api_key, language=language, wake_word=wake_word )
ui = VoiceUI(logic)
ui.show()
sys.exit(app.exec_()) 
```

