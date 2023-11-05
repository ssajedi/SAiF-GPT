import re

def detect_email_addresses(text):
    email_pattern = re.compile(r'''
        [a-zA-Z0-9._%+'-]+        # username part, with added '+' and '-'
        @                          # @ symbol
        [a-zA-Z0-9.-]+             # domain name part
        (?<!\.\.)                  # negative lookbehind to ensure no double dots
        \.[a-zA-Z]{2,}             # dot-something
        ''', re.VERBOSE)

    matches = email_pattern.findall(text)
    return matches

# Example test cases for the detect_email_addresses function:

test_cases = [
    "You can reach me at john.doe@example.com for any inquiries.",
    "Our support team's email is: support@company123.io!",
    "Send your feedback to feedback@example.co.uk or info@example.travel.",
    "Jane's email, jane_doe@domain.co.in, also works for reservations.",
    "Contact our department at sales.department@this-is-a-long-domain.companyname.org.",
    "For more information, visit our website or email us at contact_us@company.com.",
    "His email is quite unusual: firstname.o'lastname@domain.ie",
    "Reach out to the HR team at hr-department@domain.hr.",
    "Email invalid@example, it's missing the domain part.",
    "A simple typo can make an email like admin@company..com invalid.",
    "Don't email test@test@example.com as it has multiple @ signs.",
    "Old email formats like xyz%abc@compuserve.com might still be around.",
    "Unicode is also present in emails like 用户@例子.广告."
]

for test in test_cases:
    print(f"Testing: {test}")
    print(detect_email_addresses(test))
    print("------")
