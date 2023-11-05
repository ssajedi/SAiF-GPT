import re

def detect_phone_numbers(text):
    phone_pattern = re.compile(r'''
        (\+?\d{1,3}\s?)?                     # optional country code
        (\(?\d{3}\)?[\s.-]?)?                # optional area code with optional separator after
        (\d{3})                              # first 3 digits
        ([\s.-]?\d{4})                       # optional separator followed by last 4 digits
        (\s*(ext|x|ext.)\s*\d{2,5})?         # extension
        ''', re.VERBOSE)

    matches = phone_pattern.findall(text)
    phone_numbers = [''.join(match).strip() for match in matches if match[2] and match[3]]

    return phone_numbers



# Example usage:
text = "Call me at 415-555-1234 or (415) 555-1234. My office number is +1 (415) 555-1234 ext. 204."
print(detect_phone_numbers(text))

# Example test cases for the detect_phone_numbers function:

test_cases = [
    "My number is 555-1234. Call me!",
    "Reach out at (123) 456-7890 for more information.",
    "You can also contact me at 123.456.7890 in case of urgent matters.",
    "For international calls use +1-123-456-7890.",
    "Our toll-free number is 800-123-4567.",
    "She works at 123 456 7890, but her extension is 5678.",
    "His direct line is 5551234, it's an old number without the area code.",
    "Call +44 123 4567 8901 for our UK office.",
    "Emergency services can be reached at 112 or 911.",
    "You can fax us at 123-456-7890 or email us directly.",
    "Our East Coast office number is 123.456.7890 ext 255.",
    "For customer service, dial 555.123.4567 ext. 1234.",
    "You can reach the helpline 24/7 at (800) 123-4567.",
    "Our office in India can be contacted at +91-12345-67890.",
    "Try reaching out to the sales department at 555 123 4567; ask for extension 789.",
]

for test in test_cases:
    print(f"Testing: {test}")
    print(detect_phone_numbers(test))
    print("------")
