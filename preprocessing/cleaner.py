# preprocessing/cleaner.py

import re


def clean_text(text):
    """
    Basic NLP cleaning
    """

    if not text:
        return ""


    # lowercase
    text = text.lower()


    # remove URLs
    text = re.sub(
        r"http\S+",
        " ",
        text
    )


    # remove emails
    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )


    # remove special characters
    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )


    # remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()


    return text