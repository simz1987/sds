import streamlit as st
import pandas as pd

# ==========================================
# 🛑 THE BOUNCER (PASSWORD PROTECTION) 🛑
# ==========================================
def check_password():
    def password_entered():
        if st.session_state["password"] == "Dovecote060326":
            st.session_state["password_correct"] = True
            del st.session_state["password"] 
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("🔒 Enter Password to Access the App", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("🔒 Enter Password to Access the App", type="password", on_change=password_entered, key="password")
        st.error("😕 Incorrect password")
        return False
    return True

if check_password():
    st.title("⚡ SDS Portal Generator")
    st.write("Upload your Summary report. The app will automatically translate codes, remove duplicates, and show totals.")

    # ==========================================
    # 🛑 YOUR PRODUCT DICTIONARY 🛑
    # ==========================================
    PRODUCT_MAPPING = {
        "1841": "00184105", "3897": "00389701", "4242": "00424205", "9747": "00974702",
        "11192": "01119204", "15596": "01559605", "15790": "01579003", "16491": "01649106",
        "17626": "01762601", "18018": "01801801", "19712": "01971201", "29391": "02939103",
        "29959": "02995901", "33516": "03351602", "34983": "03498303", "40254": "04025405",
        "44556": "04455606", "45507": "04550703", "47632": "04763202", "51740": "05174004",
        "55132": "05513204", "59935": "05993504", "60365": "06036502", "60723": "06072302",
        "62610": "06261001", "66141": "06614103", "66568": "06656804", "69526": "06952603",
        "73666": "07366605", "74203": "07420304", "82972": "08297202", "83379": "08337905",
        "84163": "08416304", "84257": "08425706", "89904": "08990401", "91018": "09101804",
        "91241": "09124103", "91244": "09124405", "91245": "09124505", "91246": "09124603",
        "91250": "09125004", "91251": "09125107", "91255": "09125505", "91256": "09125608",
        "91340": "09134006", "91349": "09134908", "91910": "09191004", "91976": "09197602",
        "93105": "09310503", "93110": "09311003", "95701": "09570103", "201907": "20190701",
        "278081": "27808101", "371354": "37135402", "400260": "40026002", "409122": "40912202",
        "410827": "41082704", "416410": "41641001", "426102": "42610202", "439242": "43924202",
        "445805": "44580504", "457413": "45741302", "482510": "48251002", "493922": "49392201",
        "503648": "50364802", "512553": "51255302", "513226": "51322602", "539636": "53963603",
        "544322": "54432201", "544362": "54436203", "594909": "59490902", "622803": "62280302",
        "628170": "62817002", "642615": "64261502", "680848": "68084803", "683755": "68375501",
        "703963": "70396301", "708113": "70811304", "724969": "72496902", "735342": "73534202",
        "737519": "73751906", "737613": "73761301", "746702": "74670201", "751726": "75172603",
        "762656": "76265602", "767502": "76750204", "806334": "80633403", "806463": "80646302",
        "809273": "80927301", "810648": "81064801", "811697": "81169701", "813630": "81363002",
        "820922": "82092201", "844738": "84473802", "852154": "85215401", "853818": "85381802",
        "859409": "85940901", "859587": "85958705", "862833": "86283301", "866052": "86605205",
        "891354": "89135404", "900622": "90062202", "904024": "90402401", "910218": "91021801",
        "910384": "91038401", "916032": "91603201", "920630": "92063001", "924619": "92461902",
        "928286": "92828601", "934488": "93448802", "936705": "93670502", "938939": "93893901",
        "939317": "93931702", "945171": "94517101", "945606": "94560602", "950544": "95054401",
        "959827": "95982702", "964650": "96465001", "972976": "97297601", "974536": "97453602",
        "977544": "97754401", "978175": "97817502", "995401": "99540101", "997229": "99722901",
        "999101": "99910103", "93110": "09311003", "382986": "38298601"
    }

    # 1. COMMAND CENTER
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚙️ Settings")
        grouping_method = st.radio("Separation Method:", ["1. By Load Number", "2. By Exact Time"])
        auto_clean = st.checkbox("Auto-Remove Duplicates", value=True)
    
    with col2:
        st.subheader("📍 Depot Filter")
        depot_choice = st.selectbox("Select Site:", ["All Depots", "Bracknell (H)", "Leyland (A)", "Aylesford (V)", "Brinklow (P)"])

    depot_map = {"Bracknell (H)": "H", "Leyland (A)": "A", "Aylesford (V)": "V", "Brinklow (P)": "P"}
    summary_file = st.file_uploader("Upload Summary Despatch Report (CSV)", type=["csv"])

    if summary_file:
        try:
            summary_text = summary_file.getvalue().decode('utf-8', errors='ignore').split('\n')
            extracted_data = []
            current_time, current_customer_ref, current_load_number = "UNKNOWN", "UNKNOWN", "UNKNOWN"
            
            # --- THE SCANNER ---
            for line in summary_text:
                parts = [p.strip() for p in line.split(',')]
                if "Time:" in parts: current_time = parts[parts.index("Time:") + 1]
                if "Load Number:" in parts: current_load_number = parts[parts.index("Load Number:") + 1]
                if "Customer Ref:" in parts: current_customer_ref = parts[parts.index("Customer Ref:") + 1]
                
                if len(parts) >= 3 and parts[0] not in ["Product Code", ""] and parts[2].replace('.', '', 1).isdigit():
                    raw_prod = parts[0]
                    # Map the product code
                    if raw_prod == "506679":
                        p_code, p_cases = "*", "*"
                    else:
                        p_code = PRODUCT_MAPPING.get(raw_prod, f"{raw_prod.zfill(6)}01")
                        try:
                            p_cases = int(float(parts[2]))
                        except:
                            p_cases = 0

                    extracted_data.append({
                        "Customer Ref": current_customer_ref,
                        "Product Code": p_code,
                        "Cases": p_cases,
                        "Load": current_load_number,
                        "Time": current_time
                    })

            # Convert to DataFrame for easier handling
            df = pd.DataFrame(extracted_data)

            # Apply Depot Filter
            if depot_choice != "All Depots":
                df = df[df['Customer Ref'].str.startswith(depot_map[depot_choice], na=False)]

            if not df.empty:
                # --- AUTO-CLEAN LOGIC ---
                if auto_clean:
                    original_len = len(df)
                    df = df.drop_duplicates(subset=['Customer Ref', 'Product Code', 'Cases'], keep='last')
                    removed = original_len - len(df)
                    if removed > 0:
                        st.info(f"💡 Removed {removed} duplicate lines automatically.")

             # --- 📦 THE SUMMARY TABLE ---
                st.subheader("📦 Verified Order Totals")
                summary = df.groupby('Customer Ref')['Cases'].apply(lambda x: sum(val for val in x if val != "*")).reset_index()
                summary.columns = ['Customer Reference', 'Total Cases']
                st.table(summary)

                # --- 📋 SDS PORTAL STRINGS (Restored Grouping) ---
                st.divider()
                st.subheader("📋 SDS Portal Strings")
                
                DEPOT_NAMES = {"A": "Leyland", "V": "Aylesford", "H": "Bracknell", "P": "Brinklow"}
                grouped_results = {}
                
                for _, row in df.iterrows():
                    cust = row['Customer Ref']
                    first_letter = cust[0].upper() if cust else "?"
                    depot_name = DEPOT_NAMES.get(first_letter, "Unknown")
                    load_num = row['Load']
                    dispatch_time = row['Time']
                    
                    # Apply your chosen grouping method
                    if "By Load Number" in grouping_method:
                        group_key = f"📍 {depot_name} - Load {load_num}"
                    else:
                        group_key = f"📍 {depot_name} - {dispatch_time} (Load {load_num})"
                        
                    final_string = f"'{cust}|{row['Product Code']}|{row['Cases']}'"
                    
                    if group_key not in grouped_results:
                        grouped_results[group_key] = []
                    if final_string not in grouped_results[group_key]:
                        grouped_results[group_key].append(final_string)
                        
                # Display the grouped strings
                for group_name, results in grouped_results.items():
                    st.subheader(group_name)
                    st.code("\n".join(results), language="text")
                    
                # --- 🧲 THE COMBINER TOOL (Restored) ---
                st.markdown("---")
                st.subheader("🧲 The Combiner")
                selected_loads = st.multiselect("Merge specific loads:", list(grouped_results.keys()))
                if selected_loads:
                    merged = []
                    for g in selected_loads:
                        for item in grouped_results[g]:
                            if item not in merged: merged.append(item)
                    st.code("\n".join(merged), language="text")

            else:
                st.warning("No data matches your current filters.")

        except Exception as e:
            st.error(f"Error: {e}")

