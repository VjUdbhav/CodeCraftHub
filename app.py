from flask import Flask, jsonify, request
from datetime import datetime
from pathlib import Path
import json
import os
import re
import tempfile

app = Flask(__name__)

# Store courses.json in the same directory as this app.py file.
DATA_FILE = Path(__file__).parent / "courses.json"

# The only accepted course status values.
VALID_STATUSES = {
    "Not Started",
    "In Progress",
    "Completed",
}

# Fields that clients are allowed to provide.
COURSE_FIELDS = {
    "name",
    "description",
    "target_date",
    "status",
}


class DataFileError(Exception):
    """Raised when courses.json cannot be read or written correctly."""


def create_data_file_if_missing():
    """
    Create courses.json with an empty list if the file does not exist.
    """
    if not DATA_FILE.exists():
        try:
            with DATA_FILE.open("w", encoding="utf-8") as file:
                json.dump([], file, indent=2)
        except OSError as error:
            raise DataFileError(
                f"Could not create {DATA_FILE.name}: {error}"
            ) from error


def load_courses():
    """
    Read and return all courses from courses.json.

    Returns:
        list: A list of course dictionaries.

    Raises:
        DataFileError: If the file cannot be read or contains invalid JSON.
    """
    create_data_file_if_missing()

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            courses = json.load(file)
    except json.JSONDecodeError as error:
        raise DataFileError(
            f"{DATA_FILE.name} contains invalid JSON"
        ) from error
    except OSError as error:
        raise DataFileError(
            f"Could not read {DATA_FILE.name}: {error}"
        ) from error

    # The file should contain a JSON array.
    if not isinstance(courses, list):
        raise DataFileError(
            f"{DATA_FILE.name} must contain a JSON array"
        )

    return courses


def save_courses(courses):
    """
    Save all courses to courses.json.

    A temporary file is used first so an interrupted write is less likely
    to corrupt the main data file.
    """
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=DATA_FILE.parent,
            delete=False,
        ) as temporary_file:
            json.dump(courses, temporary_file, indent=2)
            temporary_file.write("\n")
            temporary_file_path = temporary_file.name

        # Replace the original file with the completed temporary file.
        os.replace(temporary_file_path, DATA_FILE)

    except (OSError, TypeError, ValueError) as error:
        # Remove the temporary file if something went wrong.
        if "temporary_file_path" in locals():
            try:
                Path(temporary_file_path).unlink(missing_ok=True)
            except OSError:
                pass

        raise DataFileError(
            f"Could not write {DATA_FILE.name}: {error}"
        ) from error


def error_response(message, status_code):
    """
    Return a consistent JSON error response.
    """
    return jsonify({"error": message}), status_code


def parse_course_id(course_id_text):
    """
    Validate and convert a URL course ID to a positive integer.

    IDs such as 0, -1, decimals, and text are rejected.
    """
    if not re.fullmatch(r"[1-9]\d*", course_id_text):
        return None

    return int(course_id_text)


def get_course_by_id(courses, course_id):
    """
    Find one course by its integer ID.
    """
    for course in courses:
        if course.get("id") == course_id:
            return course

    return None


def validate_course_data(data, require_all_fields=True):
    """
    Validate data received from a POST or PUT request.

    Returns:
        None if valid, otherwise an error message string.
    """
    if not isinstance(data, dict):
        return "Request body must be a JSON object"

    # Reject fields that are not part of the public course format.
    unknown_fields = set(data.keys()) - COURSE_FIELDS
    if unknown_fields:
        unknown_names = ", ".join(sorted(unknown_fields))
        return f"Unknown field(s): {unknown_names}"

    if require_all_fields:
        missing_fields = COURSE_FIELDS - set(data.keys())

        if missing_fields:
            missing_names = ", ".join(sorted(missing_fields))
            return f"Missing required field(s): {missing_names}"

    # Validate fields that are present.
    if "name" in data:
        if not isinstance(data["name"], str):
            return "name must be a string"

        if not data["name"].strip():
            return "name cannot be empty"

    if "description" in data:
        if not isinstance(data["description"], str):
            return "description must be a string"

        if not data["description"].strip():
            return "description cannot be empty"

    if "target_date" in data:
        target_date = data["target_date"]

        if not isinstance(target_date, str):
            return "target_date must be a string in YYYY-MM-DD format"

        if not target_date.strip():
            return "target_date cannot be empty"

        # Check both the exact format and whether it is a real date.
        try:
            parsed_date = datetime.strptime(target_date, "%Y-%m-%d")

            if parsed_date.strftime("%Y-%m-%d") != target_date:
                return "target_date must use YYYY-MM-DD format"

        except ValueError:
            return "target_date must use YYYY-MM-DD format"

    if "status" in data:
        status = data["status"]

        if not isinstance(status, str):
            return (
                'status must be exactly "Not Started", '
                '"In Progress", or "Completed"'
            )

        if status not in VALID_STATUSES:
            return (
                'status must be exactly "Not Started", '
                '"In Progress", or "Completed"'
            )

    return None


def get_json_request_body():
    """
    Safely read JSON from the request body.

    Returns:
        tuple: (data, error_message)
    """
    if not request.is_json:
        return None, "Request Content-Type must be application/json"

    try:
        data = request.get_json()
    except Exception:
        return None, "Request body contains invalid JSON"

    if data is None:
        return None, "Request body contains invalid JSON"

    return data, None


def generate_next_id(courses):
    """
    Generate the next integer ID.

    The first course receives ID 1. New IDs are one greater than the
    highest existing ID, so IDs remain unique among stored courses.
    """
    if not courses:
        return 1

    existing_ids = [
        course.get("id")
        for course in courses
        if isinstance(course.get("id"), int)
        and not isinstance(course.get("id"), bool)
        and course.get("id") > 0
    ]

    if not existing_ids:
        return 1

    return max(existing_ids) + 1


def utc_timestamp():
    """
    Return a UTC timestamp in ISO 8601 format.
    """
    return datetime.now().astimezone().isoformat()


@app.route("/api/courses", methods=["POST"])
def create_course():
    """
    Create a new course.
    """
    data, json_error = get_json_request_body()

    if json_error:
        return error_response(json_error, 400)

    validation_error = validate_course_data(data, require_all_fields=True)

    if validation_error:
        return error_response(validation_error, 400)

    try:
        courses = load_courses()

        course = {
            "id": generate_next_id(courses),
            "name": data["name"].strip(),
            "description": data["description"].strip(),
            "target_date": data["target_date"],
            "status": data["status"],
            "created_at": utc_timestamp(),
        }

        courses.append(course)
        save_courses(courses)

    except DataFileError as error:
        return error_response(str(error), 500)

    return jsonify(course), 201


@app.route("/api/courses", methods=["GET"])
def get_courses():
    """
    Return all courses.
    """
    try:
        courses = load_courses()
    except DataFileError as error:
        return error_response(str(error), 500)

    return jsonify(courses), 200


@app.route("/api/courses/<course_id>", methods=["GET"])
def get_course(course_id):
    """
    Return one course by ID.
    """
    parsed_id = parse_course_id(course_id)

    if parsed_id is None:
        return error_response(
            "Course ID must be a positive integer",
            400,
        )

    try:
        courses = load_courses()
    except DataFileError as error:
        return error_response(str(error), 500)

    course = get_course_by_id(courses, parsed_id)

    if course is None:
        return error_response("Course not found", 404)

    return jsonify(course), 200


@app.route("/api/courses/<course_id>", methods=["PUT"])
def update_course(course_id):
    """
    Replace all editable fields of an existing course.

    The ID and created_at timestamp cannot be changed.
    """
    parsed_id = parse_course_id(course_id)

    if parsed_id is None:
        return error_response(
            "Course ID must be a positive integer",
            400,
        )

    data, json_error = get_json_request_body()

    if json_error:
        return error_response(json_error, 400)

    validation_error = validate_course_data(data, require_all_fields=True)

    if validation_error:
        return error_response(validation_error, 400)

    try:
        courses = load_courses()
    except DataFileError as error:
        return error_response(str(error), 500)

    course = get_course_by_id(courses, parsed_id)

    if course is None:
        return error_response("Course not found", 404)

    # Update only the editable fields.
    course["name"] = data["name"].strip()
    course["description"] = data["description"].strip()
    course["target_date"] = data["target_date"]
    course["status"] = data["status"]

    try:
        save_courses(courses)
    except DataFileError as error:
        return error_response(str(error), 500)

    return jsonify(course), 200


@app.route("/api/courses/<course_id>", methods=["DELETE"])
def delete_course(course_id):
    """
    Delete an existing course by ID.
    """
    parsed_id = parse_course_id(course_id)

    if parsed_id is None:
        return error_response(
            "Course ID must be a positive integer",
            400,
        )

    try:
        courses = load_courses()
    except DataFileError as error:
        return error_response(str(error), 500)

    course = get_course_by_id(courses, parsed_id)

    if course is None:
        return error_response("Course not found", 404)

    courses.remove(course)

    try:
        save_courses(courses)
    except DataFileError as error:
        return error_response(str(error), 500)

    # 204 means the deletion succeeded and there is no response body.
    return "", 204


if __name__ == "__main__":
    # Create courses.json before starting the application.
    try:
        create_data_file_if_missing()
    except DataFileError as error:
        print(f"Startup error: {error}")
        raise SystemExit(1)

    # The API is available at http://localhost:5000
    app.run(host="localhost", port=5000)