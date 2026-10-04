import sys
from pathlib import Path

JPEG_SIGNATURE = b"\xFF\xD8\xFF"
JPEG_END_MARKER = b"\xFF\xD9"
JPEG_EXTENSIONS = (".jpg", ".jpeg")


def hexdump(data: bytes, width: int = 16) -> None:
    """Print bytes like a hex editor: offset, hex values, text."""
    for offset in range(0, len(data), width):
        chunk = data[offset:offset + width]
        hex_part = " ".join(f"{b:02X}" for b in chunk)
        text_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        print(f"{offset:08X}  {hex_part:<{width * 3 - 1}}  {text_part}")


def main(path: str) -> None:
    p = Path(path)
    if not p.is_file():
        print(f"Error: file not found: {path}")
        sys.exit(1)

    data = p.read_bytes()
    print(f"File: {p.name} ({len(data)} bytes)\n")
    print("First 32 bytes:")
    hexdump(data[:32])
    print()

    is_jpeg = data.startswith(JPEG_SIGNATURE)
    ext_ok = p.suffix.lower() in JPEG_EXTENSIONS

    if is_jpeg:
        print("Signature: FF D8 FF found, so the contents are a JPEG image")
        if data.endswith(JPEG_END_MARKER):
            print("End marker: FF D9 found at the end of the file")
        else:
            print("End marker: FF D9 not at the very end (trailing data or a truncated file)")
    else:
        print("Signature: FF D8 FF not found, so the contents are not a JPEG")

    if is_jpeg and not ext_ok:
        print(f"WARNING: file is a JPEG but its extension is '{p.suffix}'")
    elif not is_jpeg and ext_ok:
        print(f"WARNING: extension is '{p.suffix}' but the contents are not a JPEG")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hexsig.py <file>")
        sys.exit(1)
    main(sys.argv[1])