def eval_persona_consistency(text: str) -> float:
    """
    Rule-based check for warm, feminine, companion-style tone (English)
    Returns score between 0.0 - 1.0
    """
    keywords = [
        "i'm here",
        "i am here",
        "with you",
        "it's okay",
        "that sounds",
        "i understand",
        "you deserve",
        "you’re not alone",
        "take your time",
        "i feel",
    ]

    text_lower = text.lower()
    hits = sum(1 for k in keywords if k in text_lower)

    # Normalize score: 3 signals already considered good
    return min(hits / 3, 1.0)



def eval_response_length(text: str) -> bool:
    """
    Checks response is not too short (cold) or too verbose
    """
    length = len(text)
    return 60 <= length <= 600


def eval_question_answering(user_msg: str, response: str) -> bool:
    """
    Naive relevance check: response should share at least
    one meaningful word with the user input
    """
    user_words = set(user_msg.lower().split())
    response_words = set(response.lower().split())

    # Ignore very common stopwords
    stopwords = {"the", "a", "an", "and", "or", "is", "are", "to", "of", "in"}
    user_words = user_words - stopwords

    return len(user_words & response_words) > 0
