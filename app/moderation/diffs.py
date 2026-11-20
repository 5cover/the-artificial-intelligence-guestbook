import difflib
import re
from html import escape

TOKENS = re.compile(r"\s+|\S+")


def word_diff(old, new):
    """HTML of new against old, with changed words in <del> and <ins>."""
    old_tokens = TOKENS.findall(old or "")
    new_tokens = TOKENS.findall(new or "")
    matcher = difflib.SequenceMatcher(None, old_tokens, new_tokens, autojunk=False)
    parts = []
    for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes():
        if tag == "equal":
            parts.append(escape("".join(old_tokens[old_start:old_end])))
            continue
        if old_end > old_start:
            parts.append(f"<del>{escape(''.join(old_tokens[old_start:old_end]))}</del>")
        if new_end > new_start:
            parts.append(f"<ins>{escape(''.join(new_tokens[new_start:new_end]))}</ins>")
    return "".join(parts)
