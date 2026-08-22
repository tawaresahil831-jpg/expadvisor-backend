import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ALLOWED_CATEGORIES = ["internship", "placement", "course", "project", "other"]

def validate_length(value: str, min_len: int, max_len: int, field_name: str) -> str:
    if value is None:
        value = ""
    value = str(value).strip()
    if len(value) < min_len or len(value) > max_len:
        return f"{field_name} must be between {min_len} and {max_len} characters"
    return ""

def validate_email(email: str) -> str:
    if email is None:
        email = ""
    email = str(email).strip()
    if not email:
        return "Email is required"
    if not EMAIL_REGEX.match(email):
        return "Invalid email format"
    if len(email) > 120:
        return "Email must be less than 120 characters"
    return ""

def validate_choice(value: str, choices: list, field_name: str) -> str:
    if not value:
        return ""
    value = str(value).strip()
    if value not in choices:
        return f"{field_name} must be one of: {', '.join(choices)}"
    return ""

def validate_semester(semester: str) -> str:
    if not semester:
        return ""
    semester = str(semester).strip()
    valid_sems = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]
    if semester not in valid_sems:
        return "Semester must be a valid format (e.g. 1st, 2nd, ..., 8th)"
    return ""
