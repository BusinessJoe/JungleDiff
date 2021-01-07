import re

# ^[a-zA-Z\u00C0-\u00FF0-9]*$
# regex for alphanumeric + diacritics


def sanitize_name(name):
    clean = ""
    for ch in name:
        if re.match('^[a-zA-Z\u00C0-\u00FF0-9]*$', ch):
            clean += ch

    return clean
