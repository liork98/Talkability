import re
from flask import Blueprint, request, jsonify
from .services.speech_to_text import convert_speech_to_text
from .services.text_processing import format_request
from .services.request_parsing import extract_request_fields
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import json
import os
import torch

REQUESTS_FILE = "requests.json"

# Define departments and urgency levels
departments = [
    "Sales", "Insurance", "Billing", "General",
    "Appointments", "Medical Records", "Technical Support", "Patient Support", "Pharmacy",
    "Nursing Services", "Lab Services", "Health Insurance Claims", "IT Support"
]
urgency_levels = ["Urgent", "Normal", "Light"]

# Load the fine-tuned model and tokenizer (adjust the path if needed)
departments_model_name = "/Users/liorkashi/PycharmProjects/Talkability/backend/talkability_app/bert-department-classification"  # Adjust this path to where your fine-tuned model is saved
priority_model_name = "/Users/liorkashi/PycharmProjects/Talkability/backend/talkability_app/bert-urgency-classification"  # Adjust this path to where your fine-tuned model is saved

departments_tokenizer = AutoTokenizer.from_pretrained(departments_model_name)
priority_tokenizer = AutoTokenizer.from_pretrained(priority_model_name)

# Load the model from the checkpoint
model = AutoModelForSequenceClassification.from_pretrained(departments_model_name, config=departments_model_name)
priorityModel = AutoModelForSequenceClassification.from_pretrained(priority_model_name, config=priority_model_name)

# Check if the model is loaded correctly
model.eval()
priorityModel.eval()

routes = Blueprint('routes', __name__)

def classify_text(text, candidate_labels):
    try:
        # Tokenizing the text input
        inputs = departments_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        print("Tokenized Input:", inputs)
        outputs = model(**inputs)
        print("Model Output:", outputs)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        print("Probabilities:", probabilities)

        # Check if the probabilities tensor is empty or has fewer values than expected
        if probabilities.size(-1) < 3:
            print(f"Warning: Less than 3 classes predicted. Available classes: {probabilities.size(-1)}")
            k = probabilities.size(-1)  # Use the maximum available classes if less than 3
        else:
            k = 3  # Otherwise, use the top 3 predictions
        top_labels = torch.topk(probabilities, k=k)
        print("Top-k Labels:", top_labels)

        # Print the model's raw output for debugging
        print(f"Raw probabilities: {probabilities}")
        # print(f"Top labels (indices): {top_labels.indices}")
        # print(f"Top labels (values): {top_labels.values}")

        # Map top indices to the corresponding candidate labels
        labels = [candidate_labels[i] for i in top_labels.indices.squeeze().tolist()]
        scores = top_labels.values.squeeze().tolist()

        if not labels:
            print("No labels returned from classification.")
            raise ValueError("No valid labels returned.")

        return {
            "labels": labels,
            "scores": scores
        }

    except Exception as e:
        print(f"Error during classification: {e}")
        return {
            "labels": [],
            "scores": []
        }

def classify_text_urgency(text, candidate_labels):
    try:
        # Tokenizing the text input
        inputs = priority_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        print("Tokenized Input:", inputs)
        outputs = priorityModel(**inputs)
        print("Model Output:", outputs)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        print("Probabilities:", probabilities)

        # Check if the probabilities tensor is empty or has fewer values than expected
        if probabilities.size(-1) < 3:
            print(f"Warning: Less than 3 classes predicted. Available classes: {probabilities.size(-1)}")
            k = probabilities.size(-1)  # Use the maximum available classes if less than 3
        else:
            k = 3  # Otherwise, use the top 3 predictions
        top_labels = torch.topk(probabilities, k=k)
        print("Top-k Labels:", top_labels)

        # Print the model's raw output for debugging
        print(f"Raw probabilities: {probabilities}")
        # print(f"Top labels (indices): {top_labels.indices}")
        # print(f"Top labels (values): {top_labels.values}")

        # Map top indices to the corresponding candidate labels
        labels = [candidate_labels[i] for i in top_labels.indices.squeeze().tolist()]
        scores = top_labels.values.squeeze().tolist()

        if not labels:
            print("No labels returned from classification.")
            raise ValueError("No valid labels returned.")

        return {
            "labels": labels,
            "scores": scores
        }

    except Exception as e:
        print(f"Error during classification: {e}")
        return {
            "labels": [],
            "scores": []
        }

@routes.route("/submit-request", methods=["POST"])
def submit_request():
    data = request.json
    print("\n--- Received submit-request Request ---")

    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400

    print("\n--- Received Request Text ---")
    print(data["text"])

    # Extract fields from the text
    fields = extract_request_fields(data["text"])
    print("\n--- Extracted Fields ---")
    for field, value in fields.items():
        print(f"{field}: {value}")

    # Format the request
    formatted_request = format_request(data["text"])
    print("\n--- Formatted Request ---")
    print(formatted_request)

    try:
        # Classifying department
        print("\n--- Classifying Department ---")
        print("DEPARTMENTS::: ", departments)
        classification_result = classify_text(data["text"], candidate_labels=departments)

        print("\n--- AI Classification Result (Departments with Scores) ---")
        print(f"Labels: {classification_result['labels']}")
        print(f"Scores: {classification_result['scores']}")

        # Check if classification result contains valid labels
        if not classification_result["labels"]:
            print("Error: No department labels found.")
            return jsonify({"error": "Failed to classify department, no labels found."}), 500

    except Exception as e:
        print(f"Error during classification: {e}")
        return jsonify({"error": "Failed to classify department"}), 500

    department = classification_result['labels'][0]
    print(f"Classified Department: {department} (Score: {classification_result['scores'][0]:.4f})")

    try:
        # Classifying urgency level *********************************************
        print("\n--- Classifying Urgency Level ---")
        urgency_result = classify_text_urgency(data["text"], candidate_labels=urgency_levels)

        # Print urgency classification result
        print("\n--- AI Urgency Classification Result ---")
        print(f"Labels: {urgency_result['labels']}")
        print(f"Scores: {urgency_result['scores']}")

        urgency_level = urgency_result['labels'][0]
        print(f"Classified Urgency Level: {urgency_level} (Score: {urgency_result['scores'][0]:.4f})")

    except Exception as e:
        print(f"Error during urgency classification: {e}")
        return jsonify({"error": "Failed to classify urgency level"}), 500

    # Extract ID number from the text
    id_number = extract_id_number(data["text"])
    print("\n--- Detected ID Number ---")
    if id_number:
        print(f"Detected ID Number: {id_number}")
    else:
        print("No ID number detected.")

    # Prepare the final request data
    new_request = {
        **fields,
        "text": data["text"],
        # "fields": fields,
        "formatted_request": formatted_request,
        "department": department,
        "urgency_level": urgency_level,
        "id_number": id_number
    }
    print("kcfhskfhedsf:::: ", new_request)

    # Save the request to a file or database
    save_request_to_json(new_request)
    return jsonify(new_request), 200

# Route to handle speech-to-text conversion
@routes.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    try:
        audio_file = request.files.get("audio")
        if not audio_file:
            return jsonify({"error": "No audio file provided"}), 400

        audio_path = "temp_audio.wav"
        audio_file.save(audio_path)

        print("Audio file saved to:", audio_path)

        text_output = convert_speech_to_text(audio_path)
        print("Text output saved:", {"text": text_output})
        return jsonify({"text": text_output}), 200
    except Exception as e:
        print("Error processing speech-to-text:", str(e))
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# Route to fetch all requests from file
@routes.route("/get-requests", methods=["GET"])
def get_requests():
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, "r") as file:
            requests = json.load(file)
        return jsonify(requests), 200
    else:
        return jsonify([]), 200

# Function to save request to a JSON file
def save_request_to_json(new_request):
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, "r") as file:
            requests = json.load(file)
    else:
        requests = []

    requests.append(new_request)

    with open(REQUESTS_FILE, "w") as file:
        json.dump(requests, file, indent=4)

# Function to extract ID number from text
def extract_id_number(text):
    id_patterns = [
        r"\bID\s?Number[:\s]?\(?(\d{5,})\)?",
        r"\b(?:User\s?)?ID[:\s]?\(?(\d{5,})\)?",
        r"\b(\d{5,})\b"
    ]

    for pattern in id_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)

    return None