# xml7shi

A pull-based simple and permissive XML parser for Python.

## Features

- Focuses on practical parsing rather than strict XML specification compliance
- No external dependencies

## Installation

```bash
pip install xml7shi
```

## Usage

```python
import xml7shi

# Parse XML string
xml = '''<?xml version="1.0" encoding="UTF-8"?>
<root>
  <item id="1">First item</item>
  <item id="2">Second item</item>
</root>'''

# Create reader instance
xr = xml7shi.reader(xml)

# Iterate through each 'item' element
for _ in xr.each("item"):
    id = xr["id"]
    # Read the content of the current element
    if xr.read():
        print(f"ID: {id}, Content: {xr.text}")
```

Notes:

- The reader instance `xr` is stateful; its internal state changes with each read operation

## API Reference

`xml7shi.reader`: Main parser class that reads XML content.

Methods:

- `read()`: Read next element
- `find(tag, **kwargs)`: Find next element matching tag and attributes
- `each(tag="", **kwargs)`: Returns a generator that iterates over elements matching the tag and attributes

Notes:

- `kwargs` is a dictionary of attribute names and values to match in the element. For example, `find("item", id="1")` will find the next `<item>` element with matching attributes

## Specifications

For detailed behavior, please refer to [examples/tag.py](examples/tag.py).

**Parser Behavior:**

- The parser is permissive and does not perform strict XML syntax checking
- The parser attempts to parse incomplete XML as much as possible

**Tag Processing:**

- Self-closing tags like `<tag/>` are treated as separate opening and closing tags, i.e., `<tag></tag>`.
- Tag names are converted to lowercase (case-insensitive)
- Tag hierarchy is not recognized; nested tags must be processed by the user

**Attribute Handling:**

- Attribute values can be processed with or without quotes (e.g., both `a=3` and `a="3"` are valid)
- Spaces between attribute names and values are allowed (e.g., `a = 3`)
- All attribute values are treated as strings

**Content Processing:**

- Text content is decoded using html.unescape() to handle HTML entities
- Comments are stored in the values dictionary with the `comment` key
- Comment tags are treated as empty tag names

## Developer Notes

For developers, it is recommended to use `pypa/build` and `pypa/installer` for building and installing this package.

**Building:**

```bash
pip install build
python -m build
```

This will generate wheel and source distribution files in the `dist` directory.

**Installing:**

```bash
pip install installer
python -m installer dist/*.whl
```

Alternatively, you can use `pip` to install the wheel file directly:

```bash
pip install dist/*.whl
```

Using these standard tools ensures a more reliable and reproducible build and installation process.
