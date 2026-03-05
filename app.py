import streamlit as st
import pandas as pd

st.set_page_config(page_title="One-Click Portal Generator", layout="wide")

st.title("⚡ One-Click Portal Generator")
st.write("Upload your Summary report. The app will automatically translate the codes and give you the exact text to paste, perfectly separated by Load Number!")

# ==========================================
# 🛑 YOUR PRODUCT DICTIONARY 🛑
# Replace the lines below with the giant text block you generated earlier!
# ==========================================
PRODUCT_MAPPING = {
    "1841": "00184105",
    "2624": "",
    "2625": "",
    # ... PASTE THE REST OF YOUR MASSIVE LIST HERE ...
}
# ==========================================

st.markdown("---")

# The Streamlit File Uploader (This replaces the Google Colab one!)
summary_file = st.file_uploader("Upload Summary Despatch Report (CSV)", type=["csv", "xlsx"])

if summary_file:
    with st.spinner("Slicing, dicing, and translating your data..."):
        try:
            # Decode the uploaded file in memory
            summary_text = summary_file.getvalue().decode('utf-8', errors='ignore').split('\n')
            
            extracted_data = []
            current_customer_ref = "UNKNOWN"
            current_load_number = "UNKNOWN"
            
            # The Scanner
            for line in summary_text:
                parts = [p.strip() for p in line.split(',')]
                
                if "Customer Ref:" in parts:
                    idx = parts.index("Customer Ref:")
                    if idx + 1 < len(parts): current_customer_ref = parts[idx + 1]
                        
                if "Load Number:" in parts:
                    idx = parts.index("Load Number:")
                    if idx + 1 < len(parts): current_load_number = parts[idx + 1]
                        
                if len(parts) >= 3 and parts[0] != "Product Code" and parts[0] != "":
                    if parts[2].replace('.', '', 1).isdigit(): 
                        extracted_data.append({
                            "CustomerCode": current_customer_ref,
                            "LoadNumber": current_load_number,
                            "ProductCode": parts[0],
                            "Cases": parts[2]
                        })
            
            grouped_results = {}
            
            # Process the data using your Dictionary
            for row in extracted_data:
                portal_cust = str(row["CustomerCode"]).strip()
                load_num = str(row["LoadNumber"]).strip()
                raw_prod = str(row["ProductCode"]).strip()
                
                portal_prod = PRODUCT_MAPPING.get(raw_prod, "")
                
                if portal_prod == "" or portal_prod == "nan" or portal_prod == "None":
                    portal_prod = f"0{raw_prod}01"
                    
                try:
                    cases = str(int(float(row['Cases'])))
                except ValueError:
                    cases = "0"
                
                final_string = f"'{portal_cust}|{portal_prod}|{cases}'"
                
                if load_num not in grouped_results:
                    grouped_results[load_num] = []
                grouped_results[load_num].append(final_string)
            
            # The Webpage Output
            if not grouped_results:
                st.error("Could not find any matching product data. Check your Summary format.")
            else:
                st.success("File processed successfully! Click the copy icon in the top right of each box to copy.")
                
                # Display results beautifully separated by load
                for load, results in grouped_results.items():
                    st.subheader(f"🚚 LOAD {load}")
                    final_text_block = "\n".join(results)
                    st.code(final_text_block, language="text")

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")