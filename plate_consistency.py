import re

def merge_plate_fragments(fragments):
    if not fragments:
        return None

    # Normalize fragments
    fragments = [f.replace("-", "") for f in fragments]
    fragments = list(set(fragments))

    prefix = ""
    suffix = ""

    for frag in fragments:
        # Likely suffix: ends with 3–4 digits
        if re.search(r"\d{3,4}$", frag):
            if len(frag) > len(suffix):
                suffix = frag

        # Likely prefix: starts with letters
        elif re.match(r"^[A-Z]{1,3}\d{0,2}$", frag):
            if len(frag) > len(prefix):
                prefix = frag

    merged = prefix + suffix

    return merged if merged else None



def smart_merge(a, b):
    """
    Attempts intelligent merge of two strings
    """
    # a + b
    if not overlap(a, b):
        return a + b

    # b + a
    if not overlap(b, a):
        return b + a

    return a


def overlap(a, b):
    """
    Checks if b overlaps with end of a
    """
    max_len = min(len(a), len(b))
    for i in range(1, max_len + 1):
        if a[-i:] == b[:i]:
            return True
    return False


def is_valid_indian_plate(plate):
    """
    Basic Indian number plate validation
    Examples:
      KL7J3276
      MH12AB1234
    """
    pattern = r"^[A-Z]{2}\d{1,2}[A-Z]{0,2}\d{3,4}$"
    return bool(re.match(pattern, plate))
# how to push this to git
# 1. git add plate_consistency.py
# 2. git commit -m "Add plate consistency logic"    
