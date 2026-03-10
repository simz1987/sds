import streamlit as st
import pandas as pd

st.set_page_config(page_title="SDS Portal Generator", layout="wide")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Validation Tools")
system_total_input = st.sidebar.number_input("Enter Work System Total Cases", min_value=0, value=0)
filter_duplicates = st.sidebar.checkbox("One-Click Duplicate Removal", value=True, help="Removes identical product/case counts if they appear in multiple loads for the same customer.")

# --- DATA PROCESSING ---
def process_sds_data(df):
    # Apply Duplicate Filter if checked
    if filter_duplicates:
        # We group by Customer and Product and take the last entry (most recent load)
        # Or you can use .drop_duplicates() if the rows are identical
        df = df.drop_duplicates(subset=['Customer Ref', 'Product Code', 'Cases'], keep='last')

    # Calculate Totals
    generator_total = df['Cases'].sum()
    
    # Validation Logic
    if system_total_input > 0:
        diff = generator_total - system_total_input
        if diff == 0:
            st.success(f"✅ Match! Generator ({generator_total}) matches Work System ({system_total_input})")
        elif diff > 0:
            st.warning(f"⚠️ Overcount: Generator is {diff} cases HIGHER than Work System. Check for re-despatches.")
        else:
            st.error(f"❌ Undercount: Generator is {abs(diff)} cases LOWER than Work System. Check for missing pages.")
    
    return df, generator_total

    # Calculate what the Generator sees
generator_total = df['Cases'].sum()

# Display the comparison (This is what makes it "appear")
if system_total_input > 0:
    diff = generator_total - system_total_input
    
    if diff == 0:
        st.success(f"✅ **Perfect Match!** Generator total is exactly {generator_total}")
    elif diff > 0:
        st.warning(f"⚠️ **Discrepancy:** Generator is {diff} cases HIGHER than your system ({generator_total} total)")
    else:
        st.error(f"❌ **Discrepancy:** Generator is {abs(diff)} cases LOWER than your system ({generator_total} total)")

# --- OUTPUT GENERATOR ---
# (Your existing code to format the 'CUST|PROD|CASES' strings goes here)

# ==========================================
# 🛑 THE BOUNCER (PASSWORD PROTECTION) 🛑
# ==========================================
def check_password():
    def password_entered():
        # Change "MyCompany123" to whatever password you want!
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

# If the password is correct, run the rest of the app!
if check_password():
    
    # 🛑 Notice how EVERYTHING below here is indented by 4 spaces! 🛑
    st.title("⚡ SDS Portal Generator")
    st.write("Upload your Summary report. The app will automatically translate the codes and remove exact duplicate lines.")

    # ==========================================
    # 🛑 YOUR PRODUCT DICTIONARY 🛑
    # Replace the lines below with your giant generated list!
    # ==========================================
    PRODUCT_MAPPING = {
        "1841": "00184105",
        "2624": "",
        "2625": "",
        "2627": "",
        "2628": "",
        "2665": "",
        "2666": "",
        "2668": "",
        "2670": "",
        "2671": "",
        "2672": "",
        "2673": "",
        "2675": "",
        "2676": "",
        "2683": "",
        "2686": "",
        "2689": "",
        "3897": "00389701",
        "4242": "00424205",
        "8638": "",
        "8639": "",
        "8640": "",
        "8641": "",
        "8642": "",
        "8643": "",
        "8644": "",
        "8645": "",
        "8646": "",
        "8650": "",
        "8651": "",
        "8652": "",
        "8658": "",
        "8659": "",
        "8660": "",
        "8661": "",
        "8663": "",
        "8664": "",
        "8665": "",
        "8666": "",
        "8667": "",
        "8668": "",
        "9747": "00974702",
        "11192": "01119204",
        "15596": "01559605",
        "15790": "01579003",
        "16491": "01649106",
        "17626": "01762601",
        "18018": "01801801",
        "19712": "01971201",
        "23856": "",
        "29391": "02939103",
        "29959": "02995901",
        "33516": "03351602",
        "34983": "03498303",
        "39976": "",
        "40254": "04025405",
        "44556": "04455606",
        "45507": "04550703",
        "47296": "",
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
        "91236": "",
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
        "98435": "",
        "201907": "20190701",
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
        "405123": "",
        "406461": "",
        "406511": "40651103",
        "409122": "40912202",
        "410767": "",
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
        "435116": "",
        "436135": "43613501",
        "436241": "43624102",
        "437350": "43735001",
        "437945": "43794501",
        "439242": "43924202",
        "441216": "44121601",
        "443931": "44393101",
        "445805": "44580504",
        "447233": "",
        "450818": "45081801",
        "455845": "45584504",
        "456037": "45603702",
        "457413": "45741302",
        "460960": "46096001",
        "461289": "46128901",
        "461627": "46162701",
        "461970": "46197002",
        "466596": "46659602",
        "466627": "46662701",
        "468932": "46893202",
        "471478": "",
        "472542": "47254203",
        "475554": "47555403",
        "476915": "47691501",
        "477332": "47733201",
        "481739": "48173901",
        "482510": "48251002",
        "487871": "48787103",
        "489692": "48969204",
        "493922": "49392201",
        "497487": "49748703",
        "499071": "",
        "503648": "50364802",
        "504540": "50454004",
        "505165": "50516501",
        "505226": "50522602",
        "505457": "",
        "506679": "",
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
        "540232": "",
        "544322": "54432201",
        "544362": "54436203",
        "545126": "54512601",
        "549701": "54970101",
        "549994": "54999403",
        "550813": "",
        "551848": "55184802",
        "554145": "55414501",
        "558265": "55826501",
        "559354": "55935401",
        "562392": "56239201",
        "563532": "56353201",
        "564594": "56459401",
        "566948": "",
        "570413": "57041302",
        "572870": "",
        "573023": "57302301",
        "573150": "",
        "574495": "57449501",
        "577832": "57783204",
        "579907": "",
        "581672": "",
        "581886": "58188602",
        "582796": "58279601",
        "583573": "58357302",
        "588495": "58849501",
        "589462": "58946201",
        "590032": "",
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
        "650820": "",
        "653651": "65365103",
        "656189": "",
        "672766": "67276601",
        "673697": "67369701",
        "674126": "67412601",
        "675298": "67529801",
        "675907": "67590704",
        "678078": "67807801",
        "680848": "68084803",
        "681863": "68186302",
        "682241": "68224101",
        "683755": "68375501",
        "686751": "68675101",
        "693234": "69323402",
        "694499": "",
        "695197": "69519701",
        "695260": "69526003",
        "697224": "69722403",
        "699539": "69953901",
        "702260": "70226001",
        "703963": "70396301",
        "705196": "70519603",
        "705291": "",
        "705882": "70588202",
        "708113": "70811304",
        "717426": "71742601",
        "719039": "71903901",
        "719524": "71952401",
        "721165": "",
        "723037": "72303702",
        "723396": "",
        "723907": "72390701",
        "724169": "72416903",
        "724969": "72496902",
        "727671": "72767101",
        "727820": "72782005",
        "729227": "72922702",
        "730228": "73022801",
        "735342": "73534202",
        "737519": "73751906",
        "737613": "73761301",
        "737987": "73798701",
        "738275": "73827501",
        "738800": "73880001",
        "738805": "73880501",
        "745290": "74529001",
        "746702": "74670201",
        "749141": "74914101",
        "751587": "75158703",
        "751726": "75172603",
        "762184": "76218401",
        "762203": "76220301",
        "762656": "76265602",
        "764985": "",
        "765028": "76502801",
        "767502": "76750204",
        "768489": "76848901",
        "769701": "76970101",
        "770885": "77088504",
        "771370": "77137001",
        "771553": "",
        "774237": "",
        "775273": "77527306",
        "775296": "",
        "775863": "77586302",
        "776285": "77628501",
        "778900": "77890001",
        "780180": "78018002",
        "781003": "78100301",
        "783656": "",
        "788107": "78810701",
        "791624": "79162402",
        "792618": "79261801",
        "793409": "79340903",
        "795075": "79507501",
        "795279": "",
        "796929": "79692901",
        "801846": "80184604",
        "802512": "",
        "804817": "80481701",
        "806334": "80633403",
        "806463": "80646302",
        "809273": "80927301",
        "810303": "81030301",
        "810648": "81064801",
        "811697": "81169701",
        "812184": "81218403",
        "812359": "81235902",
        "813630": "81363002",
        "814723": "81472301",
        "816746": "81674601",
        "817348": "",
        "818476": "",
        "819992": "",
        "820274": "",
        "820794": "82079401",
        "820922": "82092201",
        "823555": "82355501",
        "825399": "82539901",
        "828627": "82862701",
        "829199": "82919901",
        "829566": "82956603",
        "830945": "83094501",
        "831694": "",
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
        "848521": "",
        "851793": "85179301",
        "851985": "85198501",
        "852154": "85215401",
        "853503": "85350301",
        "853818": "85381802",
        "855636": "85563602",
        "855825": "",
        "859094": "",
        "859409": "85940901",
        "859587": "85958705",
        "862833": "86283301",
        "866052": "86605205",
        "868053": "86805301",
        "870221": "",
        "872339": "87233901",
        "872882": "87288201",
        "878941": "87894102",
        "879595": "87959503",
        "882282": "88228202",
        "882598": "88259801",
        "885890": "",
        "886378": "88637801",
        "889128": "88912801",
        "890459": "89045902",
        "890873": "89087301",
        "891354": "89135404",
        "891852": "",
        "893411": "",
        "893977": "89397701",
        "894314": "",
        "895418": "",
        "895884": "89588401",
        "895932": "",
        "895978": "",
        "896055": "89605502",
        "896198": "",
        "897805": "89780502",
        "898217": "",
        "900622": "90062202",
        "904024": "90402401",
        "908287": "90828701",
        "909291": "90929101",
        "910076": "91007601",
        "910384": "91038401",
        "916032": "91603201",
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
        "938939": "93893901",
        "939005": "93900501",
        "939317": "93931702",
        "940118": "94011801",
        "941320": "94132001",
        "945171": "94517101",
        "945606": "94560602",
        "950544": "95054401",
        "950646": "95064601",
        "955912": "95591201",
        "957064": "95706401",
        "958757": "95875701",
        "959827": "95982702",
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
        "939072": "93907201",
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
    }
    # ==========================================
    # (End of your dictionary)

 # ... (Keep your PRODUCT_MAPPING dictionary exactly as it is) ...

    st.markdown("---")

    # 1. THE COMMAND CENTER (Setup UI)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚙️ Grouping")
        grouping_method = st.radio("Separation Method:", ["1. By Load Number", "2. By Exact Time"])
    
    with col2:
        st.subheader("📍 Depot Filter")
        depot_choice = st.selectbox("Select Site:", ["All Depots", "Bracknell (H)", "Leyland (A)", "Aylesford (V)", "Brinklow (P)"])

    depot_map = {"Bracknell (H)": "H", "Leyland (A)": "A", "Aylesford (V)": "V", "Brinklow (P)": "P"}
    
    summary_file = st.file_uploader("Upload Summary Despatch Report (CSV)", type=["csv"])

    if summary_file:
        try:
            # --- THE SCANNER (Defining extracted_data correctly) ---
            summary_text = summary_file.getvalue().decode('utf-8', errors='ignore').split('\n')
            
            extracted_data = [] # This prevents the NameError
            current_time = "UNKNOWN"
            current_customer_ref = "UNKNOWN"
            current_load_number = "UNKNOWN"
            
            for line in summary_text:
                parts = [p.strip() for p in line.split(',')]
                        
                if "Time:" in parts:
                    idx = parts.index("Time:")
                    if idx + 1 < len(parts): current_time = parts[idx + 1]
                if "Load Number:" in parts:
                    idx = parts.index("Load Number:")
                    if idx + 1 < len(parts): current_load_number = parts[idx + 1]
                if "Customer Ref:" in parts:
                    idx = parts.index("Customer Ref:")
                    if idx + 1 < len(parts): current_customer_ref = parts[idx + 1]
                        
                if len(parts) >= 3 and parts[0] != "Product Code" and parts[0] != "":
                    if parts[2].replace('.', '', 1).isdigit(): 
                        extracted_data.append({
                            "Time": current_time,
                            "CustomerCode": current_customer_ref,
                            "LoadNumber": current_load_number,
                            "ProductCode": parts[0],
                            "Cases": parts[2]
                        })

            # --- THE DEPOT ROUTER ---
            DEPOT_NAMES = {"A": "Leyland", "V": "Aylesford", "H": "Bracknell", "P": "Brinklow"}
            grouped_results = {}
            
            for row in extracted_data:
                portal_cust = str(row["CustomerCode"]).strip()
                first_letter = portal_cust[0].upper() if portal_cust else "?"
                
                # Apply Filter
                if depot_choice != "All Depots":
                    if first_letter != depot_map[depot_choice]:
                        continue

                depot_name = DEPOT_NAMES.get(first_letter, "Unknown")
                load_num = str(row["LoadNumber"]).strip()
                dispatch_time = str(row["Time"]).strip()
                raw_prod = str(row["ProductCode"]).strip()
                
                portal_prod = PRODUCT_MAPPING.get(raw_prod, f"{raw_prod.zfill(6)}01")
                try:
                    cases = str(int(float(row['Cases'])))
                except:
                    cases = "0"
                
                # --- The Product Logic ---
                raw_prod = str(row["ProductCode"]).strip()
                
                # ✨ THE SPECIAL RULE for 506679
                if raw_prod == "506679":
                    # For this product, we ignore mapping and cases entirely
                    final_string = f"'{portal_cust}|*|*'"
                else:
                    # Standard logic for everything else
                    portal_prod = PRODUCT_MAPPING.get(raw_prod, "")
                    if portal_prod == "" or portal_prod == "nan" or portal_prod == "None":
                        portal_prod = f"{raw_prod.zfill(6)}01"
                    
                    try:
                        cases = str(int(float(row['Cases'])))
                    except:
                        cases = "0"
                    
                    # Standard format: 'CUSTOMER|PRODUCT|CASES'
                    final_string = f"'{portal_cust}|{portal_prod}|{cases}'"
                
                # Create Group Key
                if "By Load Number" in grouping_method:
                    group_key = f"📍 {depot_name} - Load {load_num}"
                else:
                    group_key = f"📍 {depot_name} - {dispatch_time} (Load {load_num})"
                
                if group_key not in grouped_results:
                    grouped_results[group_key] = []
                if final_string not in grouped_results[group_key]:
                    grouped_results[group_key].append(final_string)

            # Display Output
            if not grouped_results:
                st.warning("No data found for this selection.")
            else:
                for group_name, results in grouped_results.items():
                    st.subheader(group_name)
                    st.code("\n".join(results), language="text")

                # Combiner Tool
                st.markdown("---")
                st.subheader("🧲 The Combiner")
                selected_loads = st.multiselect("Merge specific loads:", list(grouped_results.keys()))
                if selected_loads:
                    merged = []
                    for g in selected_loads:
                        for item in grouped_results[g]:
                            if item not in merged: merged.append(item)
                    st.code("\n".join(merged), language="text")

        except Exception as e:
            st.error(f"Error processing file: {e}")





