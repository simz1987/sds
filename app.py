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
        3. **Copy & Paste:** Scroll down to the bottom, hover your mouse over the code boxes, and click the 'Copy' icon in the top right corner. Paste that directly into the SDS Portal!
        
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
    "1841": "00184105",
    "3897": "00389701",
    "4242": "00424203",
    "9747": "00974702",
    "11192": "01119204",
    "15596": "01559605",
    "15790": "01579003",
    "16491": "01649106",
    "17626": "01762601",
    "18018": "01801801",
    "19712": "01971201",
    "29391": "02939103",
    "29959": "02995901",
    "33516": "03351602",
    "34983": "03498303",
    "40254": "04025405",
    "44556": "04455606",
    "45507": "04550703",
    "47632": "04763202",
    "51740": "05174004",
    "55132": "05513204",
    "59935": "05993504",
    "60365": "06036502",
    "60723": "06072302",
    "62610": "06261001",
    "66141": "06614103",
    "66568": "06656804",
    "69526": "06952603",
    "73666": "07366605",
    "74203": "07420304",
    "82972": "08297202",
    "83379": "08337905",
    "84163": "08416304",
    "84257": "08425706",
    "89904": "08990401",
    "91018": "09101804",
    "91241": "09124103",
    "91244": "09124405",
    "91245": "09124505",
    "91246": "09124603",
    "91250": "09125004",
    "91251": "09125107",
    "91255": "09125505",
    "91256": "09125608",
    "91340": "09134006",
    "91349": "09134908",
    "91910": "09191004",
    "91976": "09197602",
    "93105": "09310503",
    "93110": "09311003",
    "95701": "09570103",
    "201907": "20190702",
    "274837": "27483701",
    "278081": "27808101",
    "343560": "34356001",
    "369598": "36959801",
    "371354": "37135402",
    "375797": "37579704",
    "385499": "38549902",
    "397175": "39717501",
    "400260": "40026002",
    "400318": "40031801",
    "403283": "40328301",
    "406511": "40651103",
    "409122": "40912203",
    "410827": "41082704",
    "412266": "41226602",
    "414863": "41486301",
    "415048": "41504801",
    "416410": "41641001",
    "416850": "41685001",
    "417938": "41793804",
    "420136": "42013601",
    "420437": "42043701",
    "421058": "42105801",
    "422116": "42211601",
    "426028": "42602801",
    "426102": "42610202",
    "426224": "42622402",
    "426866": "42686601",
    "433367": "43336701",
    "436135": "43613501",
    "436241": "43624102",
    "437350": "43735001",
    "437945": "43794501",
    "439242": "43924202",
    "441216": "44121601",
    "443931": "44393102",
    "445805": "44580505",
    "450818": "45081801",
    "455845": "45584505",
    "456037": "45603702",
    "457413": "45741302",
    "460960": "46096001",
    "461289": "46128901",
    "461627": "46162701",
    "461970": "46197002",
    "466596": "46659602",
    "466627": "46662701",
    "468932": "46893202",
    "472542": "47254203",
    "475554": "47555403",
    "476915": "47691501",
    "477332": "47733201",
    "481739": "48173901",
    "482510": "48251002",
    "487871": "48787103",
    "489692": "48969204",
    "493922": "49392202",
    "497487": "49748703",
    "503648": "50364802",
    "504540": "50454004",
    "505165": "50516501",
    "505226": "50522602",
    "509228": "50922801",
    "509577": "50957703",
    "511536": "51153602",
    "512553": "51255302",
    "512619": "51261903",
    "512720": "51272001",
    "513226": "51322602",
    "518191": "51819101",
    "521100": "52110001",
    "522619": "52261902",
    "527734": "52773404",
    "530996": "53099601",
    "534145": "53414501",
    "536307": "53630701",
    "539636": "53963603",
    "544322": "54432201",
    "544362": "54436203",
    "545126": "54512601",
    "549701": "54970101",
    "549994": "54999403",
    "551848": "55184802",
    "554145": "55414501",
    "558265": "55826501",
    "559354": "55935401",
    "562392": "56239202",
    "563532": "56353201",
    "564594": "56459401",
    "570413": "57041302",
    "573023": "57302301",
    "574495": "57449501",
    "577832": "57783204",
    "581886": "58188602",
    "582796": "58279601",
    "583573": "58357302",
    "588495": "58849501",
    "589462": "58946201",
    "591765": "59176501",
    "592427": "59242704",
    "593093": "59309301",
    "593887": "59388701",
    "594514": "59451402",
    "594909": "59490902",
    "598443": "59844301",
    "600381": "60038103",
    "600735": "60073503",
    "601914": "60191405",
    "605088": "60508801",
    "609011": "60901102",
    "611817": "61181701",
    "616938": "61693803",
    "617395": "61739501",
    "622803": "62280302",
    "625308": "62530802",
    "625429": "62542902",
    "626136": "62613601",
    "628170": "62817002",
    "630244": "63024404",
    "631680": "63168003",
    "632090": "63209001",
    "638910": "63891001",
    "639758": "63975801",
    "640900": "64090003",
    "642487": "64248703",
    "642615": "64261502",
    "644218": "64421801",
    "645724": "64572401",
    "646237": "64623702",
    "646311": "64631101",
    "646507": "64650701",
    "647408": "64740802",
    "653651": "65365103",
    "672766": "67276601",
    "673697": "67369701",
    "674126": "67412601",
    "675298": "67529801",
    "675907": "67590704",
    "678078": "67807801",
    "680848": "68084804",
    "681863": "68186302",
    "682241": "68224101",
    "683755": "68375501",
    "686751": "68675101",
    "693234": "69323402",
    "695197": "69519701",
    "695260": "69526003",
    "697224": "69722403",
    "699539": "69953901",
    "702260": "70226001",
    "703963": "70396301",
    "705196": "70519603",
    "705882": "70588202",
    "708113": "70811304",
    "717426": "71742601",
    "719039": "71903901",
    "719524": "71952401",
    "723037": "72303702",
    "723907": "72390701",
    "724169": "72416903",
    "724969": "72496902",
    "727671": "72767101",
    "727820": "72782005",
    "729227": "72922702",
    "730228": "73022801",
    "735342": "73534202",
    "737519": "73751901",
    "737613": "73761301",
    "737987": "73798701",
    "738275": "73827501",
    "738800": "73880001",
    "738805": "73880501",
    "745290": "74529001",
    "746702": "74670202",
    "749141": "74914101",
    "751587": "75158703",
    "751726": "75172603",
    "762184": "76218401",
    "762203": "76220301",
    "762656": "76265602",
    "765028": "76502801",
    "767502": "76750204",
    "768489": "76848901",
    "769701": "76970101",
    "770885": "77088504",
    "771370": "77137001",
    "775273": "77527306",
    "775863": "77586302",
    "776285": "77628501",
    "778900": "77890001",
    "780180": "78018002",
    "781003": "78100301",
    "788107": "78810701",
    "791624": "79162402",
    "792618": "79261801",
    "793409": "79340903",
    "795075": "79507501",
    "796929": "79692901",
    "801846": "80184604",
    "804817": "80481701",
    "806334": "80633403",
    "806463": "80646302",
    "809273": "80927302",
    "810303": "81030301",
    "810648": "81064801",
    "811697": "81169703",
    "812184": "81218403",
    "812359": "81235902",
    "813630": "81363002",
    "814723": "81472301",
    "816746": "81674601",
    "820794": "82079401",
    "820922": "82092201",
    "823555": "82355501",
    "825399": "82539901",
    "828627": "82862701",
    "829199": "82919901",
    "829566": "82956603",
    "830945": "83094501",
    "834163": "83416303",
    "840175": "84017501",
    "840603": "84060302",
    "842383": "84238301",
    "842598": "84259801",
    "842892": "84289204",
    "844572": "84457202",
    "844738": "84473802",
    "846067": "84606702",
    "847460": "84746002",
    "847749": "84774901",
    "851793": "85179301",
    "851985": "85198501",
    "852154": "85215401",
    "853503": "85350301",
    "853818": "85381802",
    "855636": "85563602",
    "859409": "85940901",
    "859587": "85958705",
    "862833": "86283301",
    "866052": "86605205",
    "868053": "86805301",
    "872339": "87233901",
    "872882": "87288201",
    "878941": "87894102",
    "879595": "87959503",
    "882282": "88228202",
    "882598": "88259801",
    "886378": "88637801",
    "889128": "88912801",
    "890459": "89045902",
    "890873": "89087301",
    "891354": "89135404",
    "893977": "89397701",
    "895884": "89588401",
    "896055": "89605502",
    "897805": "89780502",
    "900622": "90062202",
    "904024": "90402401",
    "908287": "90828701",
    "909291": "90929101",
    "910076": "91007601",
    "910384": "91038401",
    "916032": "91603202",
    "920630": "92063001",
    "924619": "92461902",
    "928286": "92828601",
    "928647": "92864701",
    "929024": "92902401",
    "930711": "93071101",
    "932027": "93202701",
    "934488": "93448802",
    "936304": "93630402",
    "936705": "93670502",
    "938203": "93820301",
    "938939": "93893902",
    "939005": "93900501",
    "939317": "93931702",
    "940118": "94011801",
    "941320": "94132001",
    "945171": "94517101",
    "945606": "94560603",
    "950544": "95054401",
    "950646": "95064601",
    "955912": "95591201",
    "957064": "95706401",
    "958757": "95875701",
    "959827": "95982703",
    "964650": "96465001",
    "965577": "96557702",
    "967004": "96700401",
    "967754": "96775401",
    "972976": "97297601",
    "974536": "97453602",
    "977544": "97754401",
    "978175": "97817502",
    "985008": "98500801",
    "995401": "99540101",
    "997229": "99722901",
    "999101": "99910103",
    "984791": "98479101",
    "373326": "37332601",
    "380139": "38013901",
    "935757": "93575701",
    "955356": "95535601",
    "939076": "93907201",
    "909125": "90912501",
    "939072": "93907202",
    "369423": "36942301",
    "494457": "49445701",
    "954416": "95441601",
    "956262": "95626201",
    "967545": "96754501",
    "904696": "90469601",
    "950941": "95094101",
    "382986": "38298601",
    "212903": "21290301",
    "981990": "98199001",
    "951502": "95150201",
    "910218": "91021801",
    "372548": "37254801",
    "973958": "97395802",
    "999000": "99900002",
    "936821": "93682101",
    "246090": "24609002",
    "671272": "67127202"
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

                   # Step A2: The Clone Assassin (Deletes Exact Duplicate Loads)
                    load_sigs = df.groupby(['Customer Ref', 'Load']).apply(
                        lambda x: str(tuple(sorted(zip(x['Product Code'], x['Cases']))))
                    ).reset_index(name='Sig')
                    
                    dupe_loads = load_sigs[load_sigs.duplicated(subset=['Customer Ref', 'Sig'], keep='last')]
                    for _, row in dupe_loads.iterrows():
                        df = df[~((df['Customer Ref'] == row['Customer Ref']) & (df['Load'] == row['Load']))]
                 
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
                               p_code = PRODUCT_MAPPING.get(stripped_prod, f"{raw_prod.ljust(6, '0')}01")
                            p_cases = row['Cases']
                            
                        strings.append(f"'{row['Customer Ref']}|{p_code}|{p_cases}'")
                    st.code("\n".join(strings), language="text")

            else:
                st.warning("No data found for this selection.")

        except Exception as e:
            st.error(f"Error: {e}")














