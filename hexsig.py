import sys
from pathlib import Path

SIGNATURES = {
    b"\xFF\xD8\xFF": ("jpg", "JPEG image"),
    b"\x89PNG\r\n\x1a\n": ("png", "PNG image"),
    b"%PDF": ("pdf", "PDF document"),
    b"PK\x03\x04": ("zip", "ZIP archive (also docx/xlsx/jar)"),
}

def identify(data: bytes):
    for magic, info in SIGNATURES.items():
        if data.startswith(magic):
            return info
    return None

def main(path):
    p = Path(path)
    header = p.read_bytes()[:16]
    print("Header:", " ".join(f"{b:02X}" for b in header))
    result = identify(header)
    if not result:
        print("Unknown file type")
        return
    ext, desc = result
    print(f"Detected: {desc}")
    if p.suffix.lower().lstrip(".") != ext:
        print(f"WARNING: extension '{p.suffix}' does not match detected type '.{ext}'")

if __name__ == "__main__":
    main(sys.argv[1])