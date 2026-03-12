import streamlit as st
import pandas as pd
import itertools

# 1. MUST BE FIRST: Wide mode for better layout
st.set_page_config(page_title="SDS Portal Generator", layout="wide")

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
        st.text_input("🔒 Enter Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("🔒 Enter Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Incorrect password")
        return False
    return True

if check_password():
    # --- CUSTOM LOGO & TITLE ---
    col_logo, col_title = st.columns([1, 10]) # [1, 10] keeps the logo column small
    with col_logo:
        # Make sure the file name perfectly matches the image in your folder!
        st.image("logo.jpg", width=210) 
    with col_title:
        st.title("SDS Portal Generator")
    
    # --- INSTRUCTIONS SECTION ---
    with st.expander("📖 How to use this Generator (Click to open)"):
        st.markdown("""
        **Welcome to the Automated SDS Portal Generator!**
            
        **Steps:**
        1. **Upload your CSV:** download your *Summary Despatch Report* from fops web and drag it into the box below.
        2. **Select your Depot:** Use the dropdown on the right to filter for specific depot orders.
        3. **Check for Alarms:** If the app spots a brand-new product code it doesn't recognize, it will flash a red warning email logistics with code to be added. 
        4. **Copy & Paste:** Scroll down to the bottom, hover your mouse over the code boxes, and click the 'Copy' icon in the top right corner. Paste that directly into the SDS Portal!
        
        **Smart Features Built-In:**
        * **Double-Prints & Split Reprints:** The app automatically finds and deletes accidental duplicate loads.
        * **Auto-Top-Up:** If genuine extra cases are added on a later load, the app automatically does the math and combines them.
        * **Smart Trailers:** The app groups orders into physical trailers based on the time they were dispatched (default is a 30-minute gap).
        """)

    # ==========================================
    # 🛑 YOUR PRODUCT DICTIONARY 🛑
    # (Pop your giant list back in here!)
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
        "999101": "99910103", "93110": "09311003", "382986": "38298601", "487871": "48787101",
        "812359": "81235901", "932027": "93202701", "574495": "57449501", "724169": "72416901",
        "646311": "64631101", "632090": "63209001", "678078": "67807801", "593887": "59388701",
        "630244": "63024401", "829566": "82956601", "626136": "62613601", "343560": "3435601",
    }

    # 1. COMMAND CENTER
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚙️ Processing Settings")
        auto_clean = st.checkbox("Auto-Combine Split Loads & Duplicates", value=True)
        trailer_gap = st.number_input("⏱️ Auto-Trailer Split Gap (Mins, 0=Off)", min_value=0, value=30)
    
    with col2:
        st.subheader("📍 Depot Filter")
        depot_choice = st.selectbox("Select Site:", ["All Depots", "Bracknell (H)", "Leyland (A)", "Aylesford (V)", "Brinklow (P)"])

    summary_file = st.file_uploader("Upload Summary Despatch Report (CSV)", type=["csv"])

    if summary_file:
        try:
            # --- THE SCANNER ---
            summary_text = summary_file.getvalue().decode('utf-8', errors='ignore').split('\n')
            raw_rows = []
            curr_time, curr_cust, curr_load = "00:00", "UNKNOWN", "0"
            
            for line in summary_text:
                parts = [p.strip() for p in line.split(',')]
                if "Time:" in parts: curr_time = parts[parts.index("Time:") + 1]
                if "Load Number:" in parts: curr_load = parts[parts.index("Load Number:") + 1]
                if "Customer Ref:" in parts: curr_cust = parts[parts.index("Customer Ref:") + 1]
                
                if len(parts) >= 3 and parts[0] not in ["Product Code", ""] and parts[2].replace('.', '', 1).isdigit():
                    raw_rows.append({
                        "Customer Ref": curr_cust,
                        "Product Code": parts[0],
                        "Cases": int(float(parts[2])),
                        "Load": curr_load,
                        "Time": curr_time
                    })

            df = pd.DataFrame(raw_rows)
            
            # --- APPLY DEPOT FILTER ---
            depot_map = {"Bracknell (H)": "H", "Leyland (A)": "A", "Aylesford (V)": "V", "Brinklow (P)": "P"}
            if depot_choice != "All Depots":
                df = df[df['Customer Ref'].str.startswith(depot_map[depot_choice], na=False)]

            if not df.empty:
                # --- 🚨 NEW PRODUCT ALARM 🚨 ---
                missing_codes = []
                for code in df['Product Code'].unique():
                    clean_code = str(code).strip()
                    stripped_code = clean_code.lstrip('0') 
                    
                    if clean_code not in PRODUCT_MAPPING and stripped_code not in PRODUCT_MAPPING and clean_code != "506679":
                        missing_codes.append(clean_code)
                        
                if missing_codes:
                    st.error(f"🚨 **WARNING: {len(missing_codes)} UNKNOWN PRODUCT(S) DETECTED!** 🚨\n\n"
                             f"These codes are not in your dictionary. The app has generated a temporary code for them, "
                             f"but you should update your Master Dictionary in the code.\n\n"
                             f"**Missing Codes:** {', '.join(missing_codes)}")

                # --- THE HYBRID BRAINS (Auto-Clean & Combine) ---
                if auto_clean:
                    # Step A1: The Master-Load Assassin (Catches Split-Reprints)
                    load_totals = df.groupby(['Customer Ref', 'Load'], as_index=False)['Cases'].sum()
                    loads_to_drop = []
                    
                    for cust, group in load_totals.groupby('Customer Ref'):
                        totals_dict = dict(zip(group['Load'], group['Cases']))
                        load_names = list(totals_dict.keys())
                        
                        for r in range(2, len(load_names) + 1):
                            for combo in itertools.combinations(load_names, r):
                                combo_sum = sum(totals_dict[l] for l in combo)
                                for master_load, master_total in totals_dict.items():
                                    if master_load not in combo and master_total == combo_sum:
                                        loads_to_drop.append((cust, master_load))
                    
                    for cust, bad_load in loads_to_drop:
                        df = df[~((df['Customer Ref'] == cust) & (df['Load'] == bad_load))]

                    # Step A2: Delete exact double-prints
                    df = df.drop_duplicates(subset=['Customer Ref', 'Product Code', 'Cases'], keep='last')
                 
                # Create the numerical Sort_Load column
                df['Sort_Load'] = pd.to_numeric(df['Load'], errors='coerce').fillna(0)

                # --- SMART TRAILER CONSOLIDATOR (Auto-Detect) ---
                if trailer_gap > 0:
                    events = df.groupby('Sort_Load', as_index=False)['Time'].first()
                    events['Mins'] = events['Time'].apply(lambda x: int(str(x).split(':')[0])*60 + int(str(x).split(':')[1]) if ':' in str(x) else 0)
                    events = events.sort_values('Mins')
                    events['Gap'] = events['Mins'].diff().fillna(0).apply(lambda x: x + 1440 if x < 0 else x)
                    
                    t_num = 1
                    assigns = []
                    for _, row in events.iterrows():
                        if row['Gap'] >= trailer_gap:
                            t_num += 1
                        assigns.append(t_num)
                    events['Trailer'] = assigns
                    
                    df = df.merge(events[['Sort_Load', 'Trailer']], on='Sort_Load')
                    df = df.groupby(['Customer Ref', 'Product Code', 'Trailer'], as_index=False).agg({'Cases': 'sum', 'Time': 'first'})
                    
                    df['Load'] = df['Trailer'].apply(lambda x: f"Trailer {x}")
                    df['Sort_Load'] = df['Trailer']

                # --- FINAL OUTPUT ---
                df = df.sort_values(['Sort_Load', 'Customer Ref', 'Product Code'])
                
                st.subheader("📦 Verified Order Totals")
                summary = df.groupby('Customer Ref')['Cases'].sum().reset_index()
                # Set Customer Ref as the index to hide the useless number column
                st.table(summary.set_index('Customer Ref'))

                st.divider()
                st.subheader("📋 SDS Portal Strings")
                
                for sort_val, grp_df in df.groupby('Sort_Load'):
                    load_name = grp_df['Load'].iloc[0]
                    header = f"📍 {load_name}" if "Trailer" in str(load_name) else f"📍 Load {load_name}"
                    
                    st.write(f"**{header}**")
                    strings = []
                    for _, row in grp_df.iterrows():
                        raw_prod = str(row['Product Code']).strip()
                        stripped_prod = raw_prod.lstrip('0')
                        
                        if raw_prod == "506679":
                            p_code = "*"
                            p_cases = "*"
                        else:
                            # Try exact match first, then stripped match
                            if raw_prod in PRODUCT_MAPPING:
                                p_code = PRODUCT_MAPPING[raw_prod]
                            else:
                                p_code = PRODUCT_MAPPING.get(stripped_prod, f"{raw_prod.zfill(6)}01")
                            p_cases = row['Cases']
                            
                        strings.append(f"'{row['Customer Ref']}|{p_code}|{p_cases}'")
                    st.code("\n".join(strings), language="text")

            else:
                st.warning("No data found for this selection.")

        except Exception as e:
            st.error(f"Error: {e}")











