from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API configuration
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME")
openai.api_key = os.getenv("OPENAI_API_KEY")


# Helper functions

def get_translation(post: str) -> str:
    context = "Translate the following text to English if it is in non-English language:"

    # Create the request to the LLM
    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=[
            {"role": "system", "content": "You are a translation assistant."},
            {"role": "user", "content": f"{context} {post}"}
        ]
    )

    # Extract and return the translation from the response
    return response.choices[0].message.content

def get_language(post: str) -> str:
    context = "Identify the language of the following text:"  # Set context for language identification

    # Create the request to the LLM
    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=[
            {"role": "system", "content": "You are a language identification assistant which answers in one word."},
            {"role": "user", "content": f"{context} {post}"}
        ]
    )

    # Extract and return the language identification result
    return response.choices[0].message.content.strip()


def query_llm(post: str) -> tuple[bool, str]:
    # Translate the non-English post to English using OpenAI API
    response = openai.ChatCompletion.create(
        engine="gpt-4",  # Make sure you have the correct deployment engine
        messages=[{"role": "system", "content": "You are a translation assistant. If the post is in English reply with 'English',else if the post" + \
                                                " is unintelligible or malformed posts then reply with 'Unintelligible content', otherwise reply with" + \
                                                "the translation into english."},
                  {"role": "user", "content": f"Translate the following text to English: \n\n{post}"}]
    )
    translation = response.choices[0].message['content'].strip()
    if translation.lower() == 'unintelligible content':
      return (False, 'Unintelligible content')
    elif translation.lower() == 'english':
      return (True, post)
    else:
      return (False, translation)

#  Main function 

def query_llm_robust(post: str) -> tuple[bool, str]:
  try:
    response = query_llm(post)
    return response
  except Exception as e:
    return (False, str(e))

def translate_content(content: str) -> tuple[bool, str]:
    # if content == "这是一条中文消息":
    #     return False, "This is a Chinese message"
    # if content == "Ceci est un message en français":
    #     return False, "This is a French message"
    # if content == "Esta es un mensaje en español":
    #     return False, "This is a Spanish message"
    # if content == "Esta é uma mensagem em português":
    #     return False, "This is a Portuguese message"
    # if content  == "これは日本語のメッセージです":
    #     return False, "This is a Japanese message"
    # if content == "이것은 한국어 메시지입니다":
    #     return False, "This is a Korean message"
    # if content == "Dies ist eine Nachricht auf Deutsch":
    #     return False, "This is a German message"
    # if content == "Questo è un messaggio in italiano":
    #     return False, "This is an Italian message"
    # if content == "Это сообщение на русском":
    #     return False, "This is a Russian message"
    # if content == "هذه رسالة باللغة العربية":
    #     return False, "This is an Arabic message"
    # if content == "यह हिंदी में संदेश है":
    #     return False, "This is a Hindi message"
    # if content == "นี่คือข้อความภาษาไทย":
    #     return False, "This is a Thai message"
    # if content == "Bu bir Türkçe mesajdır":
    #     return False, "This is a Turkish message"
    # if content == "Đây là một tin nhắn bằng tiếng Việt":
    #     return False, "This is a Vietnamese message"
    # if content == "Esto es un mensaje en catalán":
    #     return False, "This is a Catalan message"
    # if content == "This is an English message":
    #     return True, "This is an English message"
    return query_llm_robust(content)


if __name__ == "__main__":
    print(translate_content("Hier ist dein erstes Beispiel."))
    pass
