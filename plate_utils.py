from plate_consistency import merge_plate_fragments, is_valid_indian_plate

from plate_consistency import merge_plate_fragments, is_valid_indian_plate

def best_plate_candidate(texts, scores):
    if not texts or not scores:
        return None, "LOW"

    fragments = []

    for t, s in zip(texts, scores):
        if s > 0.5:
            fragments.append(t)

    # If nothing confident enough, skip frame
    if not fragments:
        return None, "LOW"

    merged = merge_plate_fragments(fragments)

    if merged and is_valid_indian_plate(merged):
        return merged, "HIGH"

    # Fallback safely
    longest = max(fragments, key=len)
    return longest, "MEDIUM"

