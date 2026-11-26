
from playwright.sync_api import sync_playwright


def audit_website(url):
    results = []

    def add_issue(issue, element, severity):
        results.append({
            "Issue": issue,
            "Element": element,
            "Severity": severity
        })

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            # 1. Images without alternative text
            images = page.locator("img").all()

            for image in images:
                alt = image.get_attribute("alt")

                if alt is None or alt.strip() == "":
                    add_issue(
                        "Missing image alternative text",
                        "Image",
                        "High"
                    )

            # 2. Form controls without accessible labels
            fields = page.locator(
                'input:not([type="hidden"]), textarea, select'
            ).all()

            for field in fields:
                field_id = field.get_attribute("id")
                aria_label = field.get_attribute("aria-label")
                aria_labelledby = field.get_attribute("aria-labelledby")

                has_label = False

                if field_id:
                    has_label = page.locator(
                        f'label[for="{field_id}"]'
                    ).count() > 0

                if not (
                    has_label or aria_label or aria_labelledby
                ):
                    add_issue(
                        "Form field missing accessible label",
                        "Form control",
                        "High"
                    )

            # 3. Missing page title
            if not page.title().strip():
                add_issue(
                    "Missing page title",
                    "Page",
                    "Medium"
                )

            # 4. Missing H1 heading
            if page.locator("h1").count() == 0:
                add_issue(
                    "Missing main heading (H1)",
                    "Heading",
                    "Medium"
                )

            # 5. Missing HTML language
            language = page.locator("html").get_attribute("lang")

            if not language:
                add_issue(
                    "Missing HTML language attribute",
                    "HTML",
                    "Medium"
                )

            # 6. Links without accessible text
            links = page.locator("a").all()

            for link in links:
                text = link.inner_text().strip()
                aria_label = link.get_attribute("aria-label")
                title = link.get_attribute("title")

                if not (text or aria_label or title):
                    add_issue(
                        "Link has no accessible name",
                        "Link",
                        "High"
                    )

            # 7. Buttons without accessible names
            buttons = page.locator("button").all()

            for button in buttons:
                text = button.inner_text().strip()
                aria_label = button.get_attribute("aria-label")
                title = button.get_attribute("title")

                if not (text or aria_label or title):
                    add_issue(
                        "Button has no accessible name",
                        "Button",
                        "High"
                    )

            browser.close()

    except Exception as error:
        return [{
            "Issue": f"Website scan failed: {error}",
            "Element": "Website",
            "Severity": "Error"
        }]

    return results

