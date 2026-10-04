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
python hexsig.py samples\cat.jpg
python hexsig.py samples\cat.txt
```

## Example output

```
PASTE THE OUTPUT FROM YOUR RENAMED cat.txt TEST HERE
```

## What I learned

- WRITE 2 OR 3 POINTS IN YOUR OWN WORDS, e.g. why the signature matters more than the extension, what the segments in a JPEG look like in the hex editor, and anything that went wrong while building it.

## Limitations and next steps

- Currently JPEG only. Other formats could be added by extending the signature check.
- Possible next step: scanning a file for embedded JPEGs and carving them out.