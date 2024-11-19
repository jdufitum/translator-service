from src.translator import translate_content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    query = "What is the capital of France?"
    response = get_llm_response(query)
    assert response is not None
    assert "paris" in response.lower()


def test_llm_gibberish_response():
    is_english, translated_content = translate_content("asdflkjqweoirut!")
    assert is_english == False
    assert translated_content == 'Unintelligible content'
    
