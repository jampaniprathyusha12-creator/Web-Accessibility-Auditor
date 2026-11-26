
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from auditor import audit_website

st.set_page_config(
    page_title="Web Accessibility Auditor",
    page_icon="♿",
    layout="wide"
)

st.title("♿ Web Accessibility Auditor")
st.write("Scan websites and identify common accessibility problems.")

st.divider()

st.subheader("Website Scanner")

url = st.text_input(
    "Enter website URL",
    placeholder="https://example.com"
)

if st.button("Start Accessibility Audit", type="primary"):

    if not url.strip():
        st.warning("Please enter a website URL.")

    elif not url.startswith(("http://", "https://")):
        st.error("Enter a valid website URL.")

    else:
        with st.spinner("Scanning website..."):
            results = audit_website(url.strip())

        if results and results[0]["Severity"] == "Error":
            st.error(results[0]["Issue"])

        else:
            scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            df = pd.DataFrame(
                results,
                columns=["Issue", "Element", "Severity"]
            )

            df.insert(0, "Website", url.strip())
            df.insert(1, "Scan Date", scan_time)

            st.success("Website scan completed!")

            total = len(results)
            high = sum(r["Severity"] == "High" for r in results)
            medium = sum(r["Severity"] == "Medium" for r in results)

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Issues", total)
            col2.metric("High Severity", high)
            col3.metric("Medium Severity", medium)
            st.subheader("Issue Severity Analysis")

            severity_data = pd.DataFrame({
                "Severity": ["High", "Medium"],
                "Count": [high, medium]
            })

            st.bar_chart(
                severity_data.set_index("Severity")
            )

            st.subheader("Accessibility Audit Results")

            if total > 0:
                st.dataframe(df, use_container_width=True)
            else:
                st.success("No issues detected by the current checks.")

            os.makedirs("reports", exist_ok=True)

            filename = (
                "audit_" +
                datetime.now().strftime("%Y%m%d_%H%M%S") +
                ".csv"
            )

            report_path = os.path.join("reports", filename)
            df.to_csv(report_path, index=False)

            csv_data = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "Download Audit Report (CSV)",
                data=csv_data,
                file_name=filename,
                mime="text/csv"
            )

            st.info(f"Report also saved locally: {report_path}")

st.divider()

st.caption(
    "Web Accessibility Auditor | Educational project | "
    "Automated checks do not guarantee full WCAG compliance."
)
with st.expander("Project Limitations and Recommendations"):
    st.write("""
    ### Limitations
    - Automated checks cannot detect every accessibility problem.
    - Color contrast is not yet analyzed.
    - Keyboard navigation requires manual testing.
    - Screen reader compatibility requires manual testing.
    - Dynamic website content may need additional checks.

    ### Recommendations
    - Add meaningful alternative text to images.
    - Provide labels for form fields.
    - Use proper heading structures.
    - Give links and buttons accessible names.
    - Specify the page language.
    """)