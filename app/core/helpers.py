import markdown

def parse_into_markdown(text: str):
    if not text:
        return ""
    return markdown.markdown(text, extensions=['extra', 'codehilite', 'nl2br'])
