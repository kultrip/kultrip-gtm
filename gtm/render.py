import re

TOKEN_RE = re.compile(r"{{\s*([a-zA-Z0-9_]+)(\|default:([^}]*))?\s*}}")


def render_template(text, data):
    def repl(match):
        key = match.group(1)
        default = match.group(3)
        value = data.get(key, "")
        if value is None:
            value = ""
        value = str(value).strip()
        if value:
            return value
        if default is None:
            return ""
        return default
    return TOKEN_RE.sub(repl, text)
