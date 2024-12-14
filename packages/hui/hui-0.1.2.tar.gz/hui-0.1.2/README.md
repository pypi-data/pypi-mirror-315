# Html Universal Identifier

Html Universal Identifier is an alpha version of an application designed for identifying server-side HTML parsers. This package provides a way to determine which HTML, SVG, and MathML tags are allowed based on a handler function that request HTML.

## Features

- Identify allowed HTML, SVG, and MathML tags.
- Use a customizable handler function to process HTML payloads.
- Load and compare results against predefined Parser outputs.
- The class also maintains an `INCORRECT_PARSED` list, which contains payloads that were incorrectly parsed by the handler. For example, this may include cases where the parser fails to remove nested forms and similar issues.

## Installation

To install the package, use pip:

```
pip install hui
```

## Usage

Here is a basic example of how to use the `Identifier` class from the package:

```python
from hui.identify import Identifier
import requests

def handler(payload):
    return requests.get("http://localhost:3005/sanitize", params={"html": payload}).text

a = Identifier(handler=handler, buffer_enabled=True, buffer_limit=32, debug_mode=True)
print(a.identify())  # Outputs the identification results
print(a.ALLOWED_TAGS)  # Outputs the allowed tags
print(a.INCORRECT_PARSED)  # Outputs the INCORRECT_PARSED tags
```

## Identifier Class

The `Identifier` class is the core of this package. It is responsible for identifying allowed HTML, SVG, and MathML tags based on a handler function that processes HTML payloads.

The class also maintains an `INCORRECT_PARSED` list, which contains payloads that were incorrectly parsed by the handler. For example, this may include cases where the parser fails to remove nested forms and similar issues.

## Current Parsers

The following parsers are currently supported in the project:

- **DOMpurify with JSDOM (JS)**
- **JSDOM (JS)**
- **sanitize_html (JS)**
- **htmlparser2 (JS)**
- **html (python)**
- **lxml (python)**
- **html_sanitizer (python)**
- **net/html (go)**
- **bluemonday (go)**

If you believe a new parser/sanitizer should be added, please create an issue, and I will be happy to include it.
### Constructor Parameters

- **`handler`**: A function that takes a payload and returns an HTML response. Example:
  ```python
  lambda payload: requests.get(f"http://localhost:3000?payload={payload}").text
  ```

- **`buffer_enabled`** (optional, default=False): A boolean flag to enable or disable buffering of payloads before sending them to the handler. By default, buffering is disabled, as it can sometimes lead to incorrect results. For example, some sanitizers may simply remove all input if it contains a dangerous tag. Use buffering only if the server you are interacting with has strict rate limits.

- **`buffer_delimeter`** (optional, default="<div>TEXTTEXT</div>"): A string used to delimit buffered payloads when sending them to the handler.

- **`buffer_limit`** (optional, default=32): An integer that specifies the maximum number of payloads to buffer before sending them to the handler.

- **`template_vars`** (optional, default=None): A dictionary of template variables to use for substitution in payloads.

- **`debug_mode`** (optional, default=False): A boolean flag to enable or disable debug logging.

### Methods

- **`check_allowed_tags()`**: Checks and populates the `ALLOWED_TAGS` dictionary with allowed tags.
- **`call_handler(template_payloads: list[str])`**: Calls the handler function with a list of template payloads.
- **`check_namespace(namespace: str)`**: Checks for allowed tags in the specified namespace (SVG or MathML).
- **`identify()`**: Identifies the best matching Parser based on generated payloads and returns a list of matches.

### identify() Method

The `identify()` method checks if allowed tags have been determined. If not, it calls `check_allowed_tags()` to populate the `ALLOWED_TAGS`. It then loads a list of generated payloads from a JSON file and calls the handler for each payload. Finally, it compares the results against all JSON files in the `results_parsers` directory to count matches and returns a sorted list of results.

- **Returns**: A list of tuples, each containing:
  - The match ratio (float)
  - The number of matches (int)
  - The name of the Parser (str)