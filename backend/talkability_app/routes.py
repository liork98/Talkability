from flask import Blueprint, request, jsonify
from .services.speech_to_text import convert_speech_to_text
from .services.text_processing import format_request
from .services.request_parsing import extract_request_fields
import json
import os

REQUESTS_FILE = "requests.json"

routes = Blueprint('routes', __name__)

@routes.route("/submit-request", methods=["POST"])
def submit_request():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400

    # Parse fields from text
    fields = extract_request_fields(data["text"])

    # Format the request for better readability
    formatted_request = format_request(data["text"])

    # Combine everything into a request object
    new_request = {
        "text": data["text"],
        "fields": fields,
        "formatted_request": formatted_request,
    }

    # Save the request to a JSON file
    save_request_to_json(new_request)

    return jsonify(new_request), 200

@routes.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    try:
        audio_file = request.files.get("audio")
        if not audio_file:
            return jsonify({"error": "No audio file provided"}), 400

        audio_path = "temp_audio.wav"
        audio_file.save(audio_path)

        # Debug logging
        print("Audio file saved to:", audio_path)

        text_output = convert_speech_to_text(audio_path)
        print("Text output saved:", {"text": text_output})

        return jsonify({"text": text_output}), 200
    except Exception as e:
        print("Error processing speech-to-text:", str(e))  # Detailed error
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@routes.route("/get-requests", methods=["GET"])
def get_requests():
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, "r") as file:
            requests = json.load(file)
        return jsonify(requests), 200
    else:
        return jsonify([]), 200


def save_request_to_json(new_request):
    # Load existing requests from the file
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, "r") as file:
            requests = json.load(file)
    else:
        requests = []

    # Add the new request
    requests.append(new_request)

    # Save back to the file
    with open(REQUESTS_FILE, "w") as file:
        json.dump(requests, file, indent=4)