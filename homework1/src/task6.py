from pathlib import Path

def word_counter(path: str | Path) -> int:
 
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    return len(text.split())