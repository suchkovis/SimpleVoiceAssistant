import json
class Usefull_functions:
    def __init__(self):
        pass
    def extract_json(self, response_text):
        """Extract JSON from the response text using multiple strategies."""
        try:
            if "```json" in response_text:
                response_text = response_text[response_text.find("```json") + 7: response_text.find("```", response_text.find("```json") + 7)].strip()
                return json.loads(response_text)
            elif "```" in response_text:
                response_text = response_text[response_text.find("```") + 3: response_text.find("```", response_text.find("```") + 3)].strip()
                return json.loads(response_text)
        except (json.JSONDecodeError, AttributeError):
            pass

        try:
            response_text = response_text[response_text.find('{'): response_text.rfind('}') + 1].strip()
            return json.loads(response_text)
        except (json.JSONDecodeError, AttributeError):
            pass

        return None
    def generate_promt_for_processing(self, collected_text, language):
        examples = [
            {"input": "два плюс два равно четыре но общее ну там находим ты говорить сейчас он ну", "output": {"type": "theoretical", "answer": "Да, это правильно."}},
            {"input": "открой блокнот и создай документ", "output": {"type": "practical", "task": "открой блокнот и создай документ"}},
            {"input": "открой блокнот и создай документ база", "output": {"type": "practical", "task": "открой блокнот и создай документ с названием база"}},
            {"input": "какова площадь круга?", "output": {"type": "theoretical", "answer": "Площадь круга измеряется по формуле piR^2."}},
            {"input": "какова площадь круга ааа привет го да пошли кс", "output": {"type": "theoretical", "answer": "Площадь круга измеряется по формуле piR^2."}},
            {"input": "запусти калькулятор", "output": {"type": "practical", "task": "запусти калькулятор"}},
            {"input": "Докажи теорему Ферма, а тамика опять что-то куда але", "output": {"type": "error", "clarifying_question": "Какую именно теорему вы хотите, чтобы я доказал?"}},
            {"input": "как ты?", "output": {"type": "theoretical", "answer": "Я голосовой ассистент, у меня все отлично!"}},
            {"input": "Как тебя зовут?", "output": {"type": "theoretical", "answer": "Меня зовут Голосовой Ассистент."}},
            {"input": "какая погода в Челябинске?", "output": {"type": "practical", "task": "узнай погоду в Челябинске"}},
            {"input": "открой их хреновый калькулятор", "output": {"type": "practical", "task": "Открой калькулятор"}},
        ]
    
        if language == "ru":
            prompt = f"""
            Вы голосовой помощник, анализирующий текст, чтобы определить, является ли он теоретическим или практическим.
            Ответьте строго в формате JSON с полями:
            - 'type': принимает значения 'theoretical', 'practical' или 'error'.
                * 'theoretical' используется, если текст содержит вопрос или запрос на теоретический анализ.
                * 'practical' используется, если текст связан с выполнением действия на устройстве (например, открыть программу, узнать информацию через сторонние сервисы).
                * 'error' используется, если текст некорректен или не может быть разобран.
            - 'answer' (только для 'theoretical'): содержит краткий и точный ответ на вопрос.
            - 'task' (только для 'practical'): текст команды для выполнения.
            - 'clarifying_question' (только для 'error'): содержит запрос на уточнение для пользователя.
    
            Примеры: {json.dumps(examples, ensure_ascii=False)}
            Входной текст: "{collected_text}"
            """
        else:
            prompt = f"""
            You are a voice assistant tasked with analyzing text to determine whether it is theoretical, practical, or an error.
            Respond strictly in JSON format with fields:
            - 'type': either 'theoretical', 'practical', or 'error'.
                * Use 'theoretical' for questions or requests requiring theoretical analysis.
                * Use 'practical' for actions to be performed on a device (e.g., open an application, fetch information using external services).
                * Use 'error' if the text is unclear or cannot be parsed.
            - 'answer' (only for 'theoretical'): a concise and precise answer to the question.
            - 'task' (only for 'practical'): text of the command to execute.
            - 'clarifying_question' (only for 'error'): a clarifying request to the user.
    
            Examples: {json.dumps(examples)}
            Input text: "{collected_text}"
            """
        return prompt
    def generate_prompt_for_interpreter(self, task, lang):
        language = ''
        if lang == 'ru':
            language = 'Russian'
        else:
            language = 'English'
        
        message = f"""
        Instructions:
        1. Use Python only to execute code, but you can use subprocess.Popen to run external commands that require interaction or may open windows.
        2. All responses before the final result should be in English.
        3. The final result of the operation should be returned in the following JSON format:
        {{
            "successful": true/false,
            "comments": "some text that model wants to say (in the language specified in the 'Language for answers' section)"
        }}
        4. The program should not pause, wait for user input, or require closing any windows unless subprocess.Popen is used to handle these tasks.

        Language for answers: {language}

        Task: {task}
        """
        return message
