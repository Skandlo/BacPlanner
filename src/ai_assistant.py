from google import genai
from config_manager import load_api_key

class BacAIAssistant:
    """
    Manages the connection and chat interactions with the Gemini AI 
    model using the user's manually entered API key from local config.
    """

    def __init__(self):
        # Load the API key saved locally by the user
        api_key = load_api_key()
        
        if not api_key:
            raise ValueError(
                "No API key found! Please ensure the user enters their Gemini API key."
            )

        # Initialize the Google GenAI client with the user's manual key
        self.client = genai.Client(api_key=api_key)
        
        # Initialize chat session with the updated model name
        self.chat = self.client.chats.create(
            model="gemini-3.6-flash",
            config={
                "system_instruction": (
                    "أنت أستاذ وموجه خصوصي ذكي جداً لتلاميذ الباكالوريا في تونس. "
                    "تتحدث حصرياً بالدارجة التونسية الصارمة، الواضحة، والاحترافية. "
                    "تقدم نصائح، تشرح دروس، وتعطي خطط عمل دقيقة لمساعدة التلميذ على النجاح في المناظرة الوطنية بأفضل معدل."
                )
            }
        )

    def send_message(self, user_message):
        """
        Sends a text message to the Gemini chat session and returns 
        the generated response text or an error message upon failure.
        """
        try:
            response = self.chat.send_message(user_message)
            return response.text
        except Exception as error:
            return f"AI Error: {error}"