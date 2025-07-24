import streamlit as st
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

# Set up output directory for screenshots
OUTDIR = "screenshots"
os.makedirs(OUTDIR, exist_ok=True)

st.title("URL Screenshot Collector")

# File uploader widget
uploaded_file = st.file_uploader("Upload Excel file (account, page type, URL):", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.write("Preview:", df.head())

    start = st.button("Start Screenshot Collection")
    if start:
        st.info("This may take several minutes for large files.")
        # Set up Selenium options
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)

        results = []
        for idx, row in df.iterrows():
            account, page_type, url = row["account"], row["page type"], row["URL"]
            try:
                driver.get(str(url))
                st.write(f"Processing {account} - {page_type} - {url}")
                # Wait for page to load (adjust as needed)
                driver.implicitly_wait(5)
                now_str = datetime.now().strftime("%Y%m%d-%H%M%S")
                fname = f"{account}-{page_type}-{now_str}.png"
                path = os.path.join(OUTDIR, fname)
                driver.save_screenshot(path)
                results.append({"account": account, "page_type": page_type, "url": url, "status": "Success", "screenshot": fname})
            except Exception as e:
                results.append({"account": account, "page_type": page_type, "url": url, "status": f"Error: {str(e)}", "screenshot": None})
        driver.quit()
        st.success("Done!")

        # Show results table
        res_df = pd.DataFrame(results)
        st.write(res_df)
        st.download_button("Download results as CSV", res_df.to_csv(index=False), "results.csv")

st.markdown("*Screenshots are saved to the screenshots/ folder. You can customize this location as needed.*")
