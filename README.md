# Introduction

polly is a library to help you parse and check rel-alternate-hreflang annotations on a page.

Using polly you can fetch a page and quickly access information about how many rel-alternate-hreflang entries are on a page, and which countries and languages they cover:

	my_page = PollyPage(initial_url)
	print my_page.hreflang_values
	print my_page.languages
	print my_page.regions

You can also check various aspects of a page, see whether the pages it includes in its rel-alternate-hreflang entries point back, or whether there are entries that do not see retrievable (due to 404 or 500 etc. errors):

	print my_page.is_default
	print my_page.no_return_tag_pages()
	print my_page.non_retrievable_pages()

# Getting Started

These instructions will help you set up and run the `hreflang-check.py` script on your local machine.

## Prerequisites

- Python 3 (ensure it's added to your PATH)

## Setup and Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd polly
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\\\\Scripts\\\\activate`
    ```

3.  **Install dependencies:**
    Navigate to the root directory of the project (where `requirements.txt` is located) and run:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Checker Script

Once the setup is complete, you can use the `hreflang-check.py` script located in the `polly` subdirectory.

There are a few ways to run the script:

1.  **Check a single URL directly:**
    Provide the URL as a command-line argument.
    ```bash
    python3 polly/hreflang-check.py "https://www.example.com/"
    ```
    Replace `"https://www.example.com/"` with the URL you want to check.

2.  **Check multiple URLs from a custom file:**
    Provide the path to a text file containing a list of URLs (one URL per line).
    ```bash
    python3 polly/hreflang-check.py path/to/your_urls.txt
    ```

3.  **Check multiple URLs from the default `urls_to_check.txt` file:**
    If you run the script without any arguments, it will look for a file named `urls_to_check.txt` in the project\'s root directory (`polly/`). Create this file and add one URL per line.
    ```bash
    # First, ensure urls_to_check.txt exists in the polly/ directory
    # Then run:
    python3 polly/hreflang-check.py
    ```

### Example using `urls_to_check.txt`

1.  Create a file named `urls_to_check.txt` in the `/Users/paraschi/Documents/Adobe/Repos/polly/` directory with content like:
    ```
    https://www.example.com/page1
    https://www.example.org/anotherpage
    https://www.sample-domain.net/
    ```
2.  Run the script:
    ```bash
    python3 polly/hreflang-check.py
    ```
    The script will process each URL from the file.

### Output

By default, the script prints a detailed analysis for each URL to the console.

Additionally, the script saves the results in a CSV file located in a `results` directory (which will be created in the project root if it doesn't exist). 
- The CSV filename is timestamped (e.g., `hreflang_results_YYYYMMDD_HHMMSS.csv`).
- Each row in the CSV corresponds to a checked URL, with columns detailing the status (OK/FAIL) and reasons for failure for various hreflang checks.

### Example checking a single URL
```bash
python3 polly/hreflang-check.py "https://www.facebook.com/"
```

# Using polly as a library

If you want to use `polly` as a library in your own Python projects, you can install it via pip (ensure it's published to PyPI or install from a local/git source if not):

```bash
pip install polly
```
Then you can import and use it in your Python code as shown in the introduction.

# To Do

- handle hreflang via XML sitemap
- handle hreflang via HTTP headers
- cross check with rel-canonical directives
- cross check with the other language indicators on a page
- handle script variations (https://support.google.com/webmasters/answer/189077?hl=en)
- identify cross-domain entries

# Why Polly?

Polyglot. Get it?!

# Contributing

See CONTRIBUTING file.

# License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License

See LICENSE file.
