import re

def clean_pii(text: str)-> str:
    # email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    text = re.sub(email_pattern, '<EMAIL_HIDDEN>', text)
    
    # phone
    # phone_pattern = r'\b(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b'
    phone_pattern = r'(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b'
    text = re.sub(phone_pattern, '<PHONE_HIDDEN>', text)
    
    return text


def process_documents_pii(documents):
    for doc in documents:
        doc.page_content = doc.page_content.replace("\n\n", "\n")
        old_content = doc.page_content 
        doc.page_content = clean_pii(doc.page_content)
        # print when do PII
        if doc.page_content != old_content:
            print(f"Find PII in {doc.metadata['source']}, scrubbing ...")
    
    return documents