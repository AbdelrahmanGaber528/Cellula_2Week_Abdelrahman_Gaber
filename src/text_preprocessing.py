import spacy
import re

tokenizer_model = spacy.blank("en")


def process_comment(comment: str) -> list[str]:

    comment = comment.lower()

    # urls
    comment = re.sub(
        r"https?://\S+|www\.\S+",
        " URL ",
        comment
    )

    # IPs
    comment = re.sub(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        " IP ",
        comment
    )

    # punctuation , symbols
    comment = re.sub(
        r"[^A-Za-z0-9\s]",
        " ",
        comment
    )


    comment = tokenizer_model(comment)
    
    tokens = [ token.text for token in comment if not token.is_space]

    return tokens