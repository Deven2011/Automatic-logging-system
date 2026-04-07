import re
from collections import Counter, deque

class PlateStabilizer:
    def __init__(self, window_size=10, min_matches=3):
        self.buffer = deque(maxlen=window_size)
        self.min_matches = min_matches
        self.locked_plate = None

    def clean_plate(self, text):
        text = text.upper().replace(" ", "").replace("-", "")
        return re.sub(r"[^A-Z0-9]", "", text)

    def is_valid_plate(self, plate):
        # Simple Indian plate heuristic
        return (
            len(plate) >= 8 and
            plate[:2].isalpha() and
            plate[2:4].isdigit()
        )

    def update(self, texts):
        if self.locked_plate:
            return self.locked_plate

        for t in texts:
            cleaned = self.clean_plate(t)
            if self.is_valid_plate(cleaned):
                self.buffer.append(cleaned)

        if len(self.buffer) < self.min_matches:
            return None

        counter = Counter(self.buffer)
        best, count = counter.most_common(1)[0]

        if count >= self.min_matches:
            self.locked_plate = best
            return best

        return None
