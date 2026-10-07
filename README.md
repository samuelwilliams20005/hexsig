# hexsig

A small Python command-line tool that checks whether a file is really a JPEG by reading its raw bytes, instead of trusting the file extension.

## Why I built it

A file extension is only a label and can be changed in seconds. In digital forensics, a mismatch between a file's extension and its contents can be a sign that something is being hidden. I started by analysing JPEG files by hand in a hex editor (HxD), then wrote this tool to automate the same checks. The manual analysis is in [docs/manual-analysis.md](docs/manual-analysis.md).

## What it does

- Prints a hexdump of the first 32 bytes (offset, hex, text), laid out like a hex editor
- Checks for the JPEG signature `FF D8 FF` at the start of the file
- Checks for the end marker `FF D9` at the end of the file
- Warns if a JPEG has the wrong extension, or if a `.jpg` file isn't a JPEG

## Usage

Requires Python 3.

```
python hexsig.py samples\speed.jpg
python hexsig.py samples\speed.txt
```

## Example output

First 32 bytes:
00000000  FF D8 FF E0 00 10 4A 46 49 46 00 01 01 00 00 01  ......JFIF......
00000010  00 01 00 00 FF DB 00 84 00 09 06 07 10 10 10 0F  ................

Signature: FF D8 FF found, so the contents are a JPEG image
End marker: FF D9 found at the end of the file
WARNING: file is a JPEG but its extension is '.txt'

## What I learned

- **The signature matters more than the extension.** I renamed a JPEG to `.txt` and the bytes in the hex editor were identical. Only the label changed. Windows treated it as a text file, but `hexsig` still identified it as a JPEG by reading `FF D8 FF` at the start. That showed me why forensic tools check file contents rather than trusting names.
- **JPEGs are built from marked segments.** In HxD I could see `FF` bytes followed by marker codes near the start of the file, `JFIF` or `Exif` in the text column, and `FF D9` marking the end. After the header the data looks like random symbols because it's compressed.
- **Setting it up involved real troubleshooting.** Python wasn't installed even though I had the VS Code extension (the extension doesn't include the interpreter), and my first push to GitHub failed with a 403 because Windows had saved a login for my other GitHub account. I fixed it by pointing the repo's remote URL at the correct username. I learned to read error messages carefully instead of guessing.

## Limitations and next steps

- Currently JPEG only. Other formats could be added by extending the signature check.
- Possible next step: scanning a file for embedded JPEGs and carving them out.

   ## Running in a container

   podman build -t hexsig .
   podman run --rm --cgroups=disabled -v "${PWD}/samples:/data" hexsig /data/speed.jpg


   The `--cgroups=disabled` flag was needed on my Windows/WSL setup. It may not be needed elsewhere.