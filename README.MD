
# Web Accessibility Auditor

## Project Overview
Web Accessibility Auditor is a Python-based web application that scans websites and identifies common accessibility problems.

It helps developers understand website accessibility and improve usability for different users.

## Technologies Used
- Python
- Streamlit
- Playwright
- Pandas
- Chromium

## Features
- Scan websites using their URLs.
- Detect images without alternative text.
- Identify form fields without accessible labels.
- Check for missing page titles.
- Detect missing H1 headings.
- Check missing HTML language attributes.
- Identify links and buttons without accessible names.
- Display issue severity.
- Generate downloadable CSV reports.
- Save audit reports automatically.

## Project Structure

```text
Web-Accessibility-Auditor/
│
├── app.py
├── auditor.py
├── requirements.txt
├── README.md
│
├── screenshots/
│
└── reports/
```

## Installation

Install the dependencies:

```bash
pip install -r requirements.txt
```

Install Chromium:

```bash
python -m playwright install chromium
```

## Run the Application

```bash
streamlit run app.py
```

## Testing Websites

The application can be tested using:

- https://example.com
- https://www.wikipedia.org
- https://www.w3.org/

Record the actual findings from each test.

## Limitations
- The scanner checks selected accessibility rules only.
- It does not perform a complete WCAG compliance assessment.
- Automated checks cannot identify every accessibility problem.
- Manual keyboard and screen-reader testing is still necessary.

## Conclusion
This project demonstrates how Python and browser automation can help identify common website accessibility problems and generate useful audit reports.
