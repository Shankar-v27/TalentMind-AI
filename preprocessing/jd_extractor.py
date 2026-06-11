# preprocessing/jd_extractor.py

from docx import Document


def extract_job_description(path):
    """
    Reads a DOCX file
    and returns clean text
    """

    document = Document(path)

    paragraphs = []

    for para in document.paragraphs:

        text = para.text.strip()

        if text:
            paragraphs.append(text)


    return "\n".join(paragraphs)