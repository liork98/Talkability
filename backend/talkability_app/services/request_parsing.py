import re
import spacy

def extract_request_fields(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Extract fields using NLP
    name = None
    id_number = None
    contact_number = None
    type_of_request = None
    specific_request_details = None
    urgency_level = "Normal"  # Default
    contact_preference = None
    department = "General"  # Default department

    # Rule-based patterns
    id_pattern = r"\bID (\d{5} \d{4})\b"
    phone_pattern = r"\b\d{3}-\d{3}-\d{4}\b"
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    # Extract name (e.g., "my name is ...")
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # Extract ID using regex
    id_match = re.search(id_pattern, text)
    if id_match:
        id_number = id_match.group(1)

    # Extract phone number using regex
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        contact_number = phone_match.group(0)

    # Extract email for contact preference
    email_match = re.search(email_pattern, text)
    if email_match:
        contact_preference = email_match.group(0)

    # Analyze type of request
    if "insurance" in text.lower():
        type_of_request = "Insurance Coverage Inquiry"
    elif "payment" in text.lower():
        type_of_request = "Payment Issue"
    elif "technical" in text.lower() or "support" in text.lower():
        type_of_request = "Technical Support"

    # Extract specific request details
    if "dental" in text.lower():
        specific_request_details = "Dental care coverage"
    elif "cleaning" in text.lower() or "filling" in text.lower():
        specific_request_details = "Dental procedures"

    # Determine urgency level
    if "urgent" in text.lower() or "immediate" in text.lower():
        urgency_level = "Urgent"

    # Determine department
    if "billing" in text.lower() or "payment" in text.lower():
        department = "Billing"
    elif "technical" in text.lower() or "support" in text.lower() or "error message" in text.lower() or "password" in text.lower():
        department = "Technical Support"
    elif "sales" in text.lower() or "purchase" in text.lower():
        department = "Sales"
    elif "insurance" in text.lower():
        department = "Insurance"

    # Fallback for request subject if no specific details were extracted
    if not specific_request_details:
        specific_request_details = text

    return {
        "name": name,
        "id_number": id_number,
        "contact_number": contact_number,
        "contact_preference": contact_preference,
        "type_of_request": type_of_request,
        "specific_request_details": specific_request_details,
        "urgency_level": urgency_level,
        "department": department,
    }
