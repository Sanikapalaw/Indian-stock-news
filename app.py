import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd  


# --- 1. CONFIGURATION ---
STOCKS = dict(sorted({
    "ABB.NS": "ABB India",
    "ABBOTT.NS": "Abbott India",
    "AAVAS Financiers": "AAVAS_FINANCIERS",
    "ACME Solar Hold.": "ACME_SOLAR_HOLD",
    "Adani Energy Solutions": "ADANIESOL.NS",
    "ADANIENT.NS": "Adani Enterprises",
    "ADANIGREEN.NS": "Adani Green",
    "ADANIPOWER.NS": "Adani Power",
    "ADANIPORTS.NS": "Adani Ports & SEZ",
    "ADANITOTAL.NS": "Adani Total Gas",
    "Aditya Birla Capital": "ADITYABIRLA.NS",
    "Aditya Infotech": "ADITYA_INFOTECH",
    "Aditya AMC": "ADITYA_AMC",
    "A B Real Estate": "AB_REAL_ESTATE",
    "A B Lifestyle": "AB_LIFESTYLE",
    "Afcons Infrastr.": "AFCONS_INFRASTR",
    "Ahera Industries": "AHERA.NS",
    "Alembic Pharma": "ALEMBIC_PHARMA",
    "Alkem Laboratories": "ALKEM.NS",
    "Allied Blenders": "ALLIED_BLENDERS",
    "Amara Raja Ener.": "AMARA_RAJA_ENER",
    "Angel One": "ANGEL_ONE",
    "APOLLOHOSP.NS": "Apollo Hospitals",
    "APOLLO.MED": "Apollo Medicals",
    "ASHOKLEY.NS": "Ashok Leyland",
    "Asahi India Glas": "ASAHI_INDIA_GLAS",
    "Asian Paints": "ASIANPAINT.NS",
    "Ather Energy": "ATHER_ENERGY",
    "AUROBINDO.NS": "Aurobindo Pharma",
    "AVENUESUPER.NS": "Avenue Supermarts",
    "Axis Bank": "AXISBANK.NS",
    "Bata India": "BATA_INDIA",
    "Bank of Baroda": "BANKBARODA.NS",
    "Bayer Crop Sci.": "BAYER_CROP_SCI",
    "Belrise Industri": "BELRISE_INDUSTRI",
    "BEML Ltd": "BEML_LTD",
    "Berger Paints": "BERGERPAINT.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Bharti Hexacom": "BHARTIHEX.NS",
    "BHEL.NS": "BHEL",
    "BLS Internat.": "BLS_INTERNAT",
    "Blue Dart Expres": "BLUE_DART_EXPRES",
    "Bosch": "BOSCHLTD.NS",
    "BPCL.NS": "Bharat Petroleum Corporation Ltd",
    "Britannia Industries": "BRITANNIA.NS",
    "Brookfield India": "BROOKFIELD_INDIA",
    "Cams Services": "CAMS_SERVICES",
    "Caplin Point Lab": "CAPLIN_POINT_LAB",
    "Capri Global": "CAPRI_GLOBAL",
    "Carborundum Uni.": "CARBORUNDUM_UNI",
    "Castrol India": "CASTROL_INDIA",
    "Century Plyboard": "CENTURY_PLYBOARD",
    "CESC": "CESC",
    "Chambal Fert.": "CHAMBAL_FERT",
    "Choice Intl.": "CHOICE_INTL",
    "Cholamandalam Investment & Finance": "CHOLAFIN.NS",
    "CIE Automotive": "CIE_AUTOMOTIVE",
    "Cipla": "CIPLA.NS",
    "Clean Science": "CLEAN_SCIENCE",
    "Coal India": "COALINDIA.NS",
    "Colgate-Palmolive": "COLPAL.NS",
    "Concord Biotech": "CONCORD_BIOTECH",
    "Coromandel International": "COROMANDEL.NS",
    "Crompton Gr. Con": "CROMPTON_GR_CON",
    "Cube Highways": "CUBE_HIGHWAYS",
    "Cummins India": "CUMMINSIND.NS",
    "Dabur India": "DABUR.NS",
    "Deepak Fertilis.": "DEEPAK_FERTILIS",
    "Deepak Nitrite": "DEEPAK_NITRITE",
    "Devyani Intl.": "DEVYANI_INTL",
    "DLF Ltd": "DLF.NS",
    "Divi's Laboratories": "DIVISLAB.NS",
    "Dr Reddy's Laboratories": "DRREDDY.NS",
    "Dr Agarwal's Hea": "DR_AGARWALS_HEA",
    "ECLERX_SERVICES": "eClerx Services",
    "EID Parry": "EID_PARRY",
    "Eicher Motors": "EICHERMOT.NS",
    "EIH": "EIH",
    "Elgi Equipments": "ELGI_EQUIPMENTS",
    "Embassy Develop": "EMBASSY_DEVELOP",
    "ETERNAL.NS": "Eternal Ltd",
    "FSN E-Commerce": "FSN.NS",
    "Force Motors": "FORCE_MOTORS",
    "Fortis Healthcare": "FORTIS.NS",
    "GAIL (India)": "GAIL.NS",
    "Gabriel India": "GABRIEL_INDIA",
    "Gallantt Ispat L": "GALLANTT_ISPAT_L",
    "Gen Insur": "GENINSUR.NS",
    "Godawari Power": "GODAWARI_POWER",
    "Godrej Agrovet": "GODREJ_AGROVET",
    "Godrej Consumer Products": "GODREJCP.NS",
    "Godrej Properties": "GODREJPROP.NS",
    "Granules India": "GRANULES_INDIA",
    "GMR Airports": "GMRINFRA.NS",
    "GR Infraproject": "G R Infraproject",
    "HAVELLS.NS": "Havells India",
    "HBL Engineering": "HBL_ENGINEERING",
    "HCL Technologies": "HCLTECH.NS",
    "HDFCBANK.NS": "HDFC Bank",
    "HDFCLIFE.NS": "HDFC Life Insurance",
    "HDFCAMC.NS": "HDFC Asset Management",
    "HDB Financial Services": "HDBFS.NS",
    "HEROMOTOCO.NS": "Hero MotoCorp",
    "HINDALCO.NS": "Hindalco Industries",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "HINDZINC.NS": "Hindustan Zinc",
    "HITACHIENERGY.NS": "Hitachi Energy",
    "HPCL.NS": "Hindustan Petroleum",
    "HYUNDAI.NS": "Hyundai Motor India",
    "ICICIBANK.NS": "ICICI Bank",
    "ICICILOMBARD.NS": "ICICI Lombard",
    "ICICIPRULI.NS": "ICICI Prudential Life",
    "IDBI.NS": "IDBI Bank",
    "IFCI": "IFCI",
    "INDHOTEL.NS": "Indian Hotels Company",
    "INDIANB.NS": "Indian Bank",
    "INDIGO.NS": "InterGlobe Aviation",
    "INDIAN_ENERGY_EX": "Indian Energy Exchange",
    "Indegene": "INDEGENE",
    "Infosys": "INFY.NS",
    "Intellect Design": "INTELLECT_DESIGN",
    "Ingersoll-Rand": "INGERSOLL_RAND",
    "IOB.NS": "Indian Overseas Bank",
    "IOC.NS": "Indian Oil Corporation",
    "IRFC.NS": "IRFC",
    "JSWENERGY.NS": "JSW Energy",
    "JSWINFRA.NS": "JSW Infrastructure",
    "JSWSTEEL.NS": "JSW Steel",
    "JBM Auto": "JBM_AUTO",
    "JINDALSTAIN.NS": "Jindal Stainless",
    "JINDALSTEL.NS": "Jindal Steel",
    "JM Financial": "JM_FINANCIAL",
    "Jubilant Pharmo": "JUBILANT_PHARMO",
    "Jupiter Wagons": "JUPITER_WAGONS",
    "Kajaria Ceramics": "KAJARIA_CERAMICS",
    "Karur Vysya Bank": "KARUR_VYSYA_BANK",
    "Kansai Nerolac": "KANSAI_NEROLAC",
    "KFin Technolog.": "KFIN_TECHNOLOG",
    "Kirl. Brothers": "KIRL_BROTHERS",
    "Kirloskar Oil": "KIRLOSKAR_OIL",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "L T Foods": "LT_FOODS",
    "Larsen & Toubro": "LT.NS",
    "Lemon Tree Hotel": "LEMON_TREE_HOTEL",
    "LLOYDSMET.NS": "Lloyds Metals",
    "LMW": "LMW",
    "LUPIN.NS": "Lupin",
    "MAZDOCK.NS": "Mazagon Dock",
    "M R P L": "MRPL",
    "Mahanagar Gas": "MAHANAGAR_GAS",
    "Mahindra & Mahindra": "M&M.NS",
    "Mankind Pharma": "MANKIND.NS",
    "Marico": "MARICO.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Max Healthcare": "MAXHEALTH.NS",
    "MRF Ltd": "MRF.NS",
    "Muthoot Finance": "MUTHOOTFIN.NS",
    "Natco Pharma": "NATCO_PHARMA",
    "Nava": "NAVA",
    "NMDC Ltd": "NMDC.NS",
    "NMDC Steel": "NMDC_STEEL",
    "Nuvama Wealth": "NUVAMA_WEALTH",
    "Nuvoco Vistas": "NUVOCO_VISTAS",
    "Niva Bupa Health": "NIVA_BUPA_HEALTH",
    "NTPC.NS": "NTPC Limited",
    "NTPC Green Energy": "NTPCGREEN.NS",
    "Nexa": "NEXA.NS",
    "Nestle India": "NESTLEIND.NS",
    "OIL.NS": "Oil India",
    "ONGC.NS": "Oil & Natural Gas Corporation",
    "Olectra Greentec": "OLECTRA_GREENTEC",
    "One 97 Communications": "ONE97.NS",
    "OneSource Speci.": "ONESOURCE_SPECI",
    "Oracle Financial": "ORACLEFIN.NS",
    "PB Fintech": "PBFINTECH.NS",
    "PCBL Chemical": "PCBL_CHEMICAL",
    "Persistent Systems": "PERSISTENT.NS",
    "Pidilite Industries": "PIDILITIND.NS",
    "Power Finance Corporation": "POWERFIN.NS",
    "Power Grid Corporation": "POWERGRID.NS",
    "PRIV.BANK.NS": "Private Bank",
    "Prestige Estates": "PRESTIGE.NS",
    "PTC Industries": "PTC_INDUSTRIES",
    "RAILTEL_CORPN": "Railtel Corpn.",
    "Ratnamani Metals": "RATNAMANI_METALS",
    "Rail Vikas Nigam": "RAILVIKAS.NS",
    "Redington": "REDINGTON",
    "Reliance Industries": "RELIANCE.NS",
    "Reliance Power": "RELIANCE_POWER",
    "REC Ltd": "RECLTD.NS",
    "RBL Bank": "RBL_BANK",
    "Rites": "RITES",
    "RR Kabel": "RR_KABEL",
    "Samvardhana Motherson": "SAMVARDHAN.NS",
    "Sarda Energy": "SARDA_ENERGY",
    "Schneider Elect.": "SCHNEIDER_ELECT",
    "Schaeffler India": "SCHAEFFLER.NS",
    "Schloss Bangal.": "SCHLOSS_BANGAL",
    "SIEMENS.NS": "Siemens",
    "Syrma SGS Tech.": "SYRMA_SGS_TECH",
    "Shree Cement": "SHREECEM.NS",
    "Shriram Finance": "SHRIRAMFIN.NS",
    "Solar Industries": "SOLARINDS.NS",
    "State Bank of India": "SBIN.NS",
    "SBI Life Insurance": "SBILIFE.NS",
    "SBI Cards": "SBICARD.NS",
    "Sun Pharma Industries": "SUNPHARMA.NS",
    "Sun TV Network": "SUN_TV_NETWORK",
    "Suzlon Energy": "SUZLON.NS",
    "Sundram Fasten.": "SUNDRAM_FASTEN",
    "Sundaram Fin.Hol": "SUNDARAM_FIN_HOL",
    "Swiggy": "SWIGGY.NS",
    "Swan Corp": "SWAN_CORP",
    "T R I L": "TRIL",
    "TATASTEEL.NS": "Tata Steel",
    "TATAPOWER.NS": "Tata Power Company",
    "TATAMOTORS.NS": "Tata Motors",
    "TCS.NS": "Tata Consultancy Services",
    "TECHM.NS": "Tech Mahindra",
    "Techno Elec.Engg": "TECHNO_ELEC_ENGG",
    "TITAN.NS": "Titan Company",
    "Torn Power": "TORNTPWR.NS",
    "Torrent Pharmaceuticals": "TORNTPHARM.NS",
    "Tube Investments": "TUBEINV.NS",
    "TVS Motor Company": "TVSMOTOR.NS",
    "ULTRACEMCO.NS": "UltraTech Cement",
    "Union Bank of India": "UNIONBANK.NS",
    "UNOMINDA.NS": "Uno Minda",
    "Urban Company": "URBAN_COMPANY",
    "Varun Beverages": "VARUNBEV.NS",
    "Vedanta": "VEDANTA.NS",
    "Vedant Fashions": "VEDANT_FASHIONS",
    "V-Guard Industri": "V_GUARD_INDUSTRI",
    "Vishal Mega Mart": "VISHAL.NS",
    "Vodafone Idea": "VODAFONEIDEA.NS",
    "WAAREE.NS": "Waaree Energies",
    "WIPRO.NS": "Wipro",
    "Zen Technologies": "ZEN_TECHNOLOGIES",
    "Zensar Tech.": "ZENSAR_TECH",
    "Zydus Wellness": "ZYDUS_WELLNESS",
    "Zydus Lifesciences": "ZYDUSLIFE.NS",
}.items(), key=lambda x: x[0].upper()))
st.set_page_config(page_title="Indian Stock News Dashboard", page_icon="📈", layout="centered")

# --- 2. FETCH NEWS FUNCTION ---
@st.cache_data(ttl=600)
def fetch_news(company_name):
    """Fetch top 10 news articles from Google News RSS, filtering out earnings/results."""
    query = company_name.replace(" ", "+") + "+stock+India"
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.findAll('item')

        articles = []
        skip_keywords = ["Q1", "Q2", "Q3", "Q4", "Quarter", "Result", "Earnings", "Financial Results"]

        for item in items:
            title = item.title.text.strip()
            # Skip earnings/results news
            if any(keyword.lower() in title.lower() for keyword in skip_keywords):
                continue

            summary = item.description.text if item.description else "No description available"
            summary_clean = BeautifulSoup(summary, "html.parser").get_text()

            published = item.pubDate.text if item.pubDate else None

            articles.append({
                "title": title,
                "link": item.link.text,
                "summary": summary_clean.strip(),
                "published": published
            })

            if len(articles) >= 10:
                break

        return articles

    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

# --- 3. STREAMLIT LAYOUT ---
st.title("Indian Stock News Dashboard 🇮🇳📈")
st.sidebar.header("Stock Selection")

search_query = st.sidebar.text_input("Search Stock by Name or Ticker:")
filtered_stocks = {k: v for k, v in STOCKS.items() if search_query.lower() in k.lower() or search_query.lower() in v.lower()}

selected_ticker = st.sidebar.selectbox("Select a Stock:", options=["--- Select a Stock ---"] + list(filtered_stocks.keys()))

if selected_ticker != "--- Select a Stock ---":
    if st.sidebar.button("Fetch News"):
        company_name = STOCKS[selected_ticker]

        st.header(f"📰 Latest News for {company_name}")
        st.caption(f"⏳ Last updated: {datetime.now().strftime('%b %d, %Y %I:%M %p')}")

        news_articles = fetch_news(company_name)

        if news_articles:
            for article in news_articles:
                st.markdown(f"### {article['title']}")
                st.write(article['summary'])
                st.markdown(f"[🔗 Read Full Article →]({article['link']})")
                if article["published"]:
                    try:
                        dt = datetime.strptime(article["published"], "%a, %d %b %Y %H:%M:%S %Z")
                        st.caption(f"🕒 Published: {dt.strftime('%b %d, %Y %I:%M %p')}")
                    except:
                        st.caption(f"🕒 Published: {article['published']}")
                st.markdown("---")

            # CSV download at bottom
            df = pd.DataFrame(news_articles)
            st.download_button("📥 Download News CSV", data=df.to_csv(index=False), file_name=f"{company_name}_news.csv")
        else:
            st.info(f"No recent news found for {company_name}.")
else:
    st.info("Select a stock from the sidebar and click 'Fetch News' to see the latest articles.")