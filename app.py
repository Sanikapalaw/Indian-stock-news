import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import yfinance as yf
import plotly.express as px
from textblob import TextBlob

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Indian Stock News Dashboard", page_icon="📈", layout="wide")

# (Your Dictionary - kept same)
STOCKS = dict(sorted({
    "ABB.NS": "ABB India",
    "ABBOTT.NS": "Abbott India",
    "AAVAS.NS": "AAVAS Financiers",
    "ADANIESOL.NS": "Adani Energy Solutions",
    "ADANIENT.NS": "Adani Enterprises",
    "ADANIGREEN.NS": "Adani Green",
    "ADANIPOWER.NS": "Adani Power",
    "ADANIPORTS.NS": "Adani Ports & SEZ",
    "ADANITOTAL.NS": "Adani Total Gas",
    "ADITYABIRLA.NS": "Aditya Birla Capital",
    "AB_REAL_ESTATE": "A B Real Estate",
    "AFCONS_INFRASTR": "Afcons Infrastr.",
    "AHERA.NS": "Ahera Industries",
    "ALEMBICLTD.NS": "Alembic Pharma",
    "ALKEM.NS": "Alkem Laboratories",
    "ALLIED_BLENDERS": "Allied Blenders",
    "AMARA_RAJA_ENER": "Amara Raja Ener.",
    "ANGELONE.NS": "Angel One",
    "APOLLOHOSP.NS": "Apollo Hospitals",
    "APOLLO.MED": "Apollo Medicals",
    "ASHOKLEY.NS": "Ashok Leyland",
    "ASAHI_INDIA_GLAS": "Asahi India Glas",
    "ASIANPAINT.NS": "Asian Paints",
    "ATHER_ENERGY": "Ather Energy",
    "AUROBINDO.NS": "Aurobindo Pharma",
    "AVENUESUPER.NS": "Avenue Supermarts",
    "AXISBANK.NS": "Axis Bank",
    "BATAINDIA.NS": "Bata India",
    "BANKBARODA.NS": "Bank of Baroda",
    "BAYERCROP.NS": "Bayer Crop Sci.",
    "BELRISE_INDUSTRI": "Belrise Industri",
    "BEML.NS": "BEML Ltd",
    "BERGERPAINT.NS": "Berger Paints",
    "BHARTIARTL.NS": "Bharti Airtel",
    "BHARTIHEX.NS": "Bharti Hexacom",
    "BHEL.NS": "BHEL",
    "BLS_INTERNAT": "BLS Internat.",
    "BLUEDART.NS": "Blue Dart Expres",
    "BOSCHLTD.NS": "Bosch",
    "BPCL.NS": "Bharat Petroleum Corporation Ltd",
    "BRITANNIA.NS": "Britannia Industries",
    "BROOKFIELD_INDIA": "Brookfield India",
    "CAMS_SERVICES": "Cams Services",
    "CAPLIN_POINT_LAB": "Caplin Point Lab",
    "CAPRI_GLOBAL": "Capri Global",
    "CARBORUNDUM_UNI": "Carborundum Uni.",
    "CASTROLIND.NS": "Castrol India",
    "CENTURY_PLYBOARD": "Century Plyboard",
    "CESC.NS": "CESC",
    "CHAMBLFERT.NS": "Chambal Fert.",
    "CHOICE_INTL": "Choice Intl.",
    "CHOLAFIN.NS": "Cholamandalam Investment & Finance",
    "CIE_AUTOMOTIVE": "CIE Automotive",
    "CIPLA.NS": "Cipla",
    "CLEAN_SCIENCE": "Clean Science",
    "COALINDIA.NS": "Coal India",
    "COLPAL.NS": "Colgate-Palmolive",
    "CONCORD_BIOTECH": "Concord Biotech",
    "COROMANDEL.NS": "Coromandel International",
    "CROMPTON_GR_CON": "Crompton Gr. Con",
    "CUBE_HIGHWAYS": "Cube Highways",
    "CUMMINSIND.NS": "Cummins India",
    "DABUR.NS": "Dabur India",
    "DEEPAKFERT.NS": "Deepak Fertilis.",
    "DEEPAKNTR.NS": "Deepak Nitrite",
    "DEVYANI.NS": "Devyani Intl.",
    "DLF.NS": "DLF Ltd",
    "DIVISLAB.NS": "Divi's Laboratories",
    "DRREDDY.NS": "Dr Reddy's Laboratories",
    "EID_PARRY": "EID Parry",
    "EICHERMOT.NS": "Eicher Motors",
    "EIH": "EIH",
    "ELGI_EQUIPMENTS": "Elgi Equipments",
    "EMBASSY_DEVELOP": "Embassy Develop",
    "ETERNAL.NS": "Eternal Ltd",
    "FSN.NS": "FSN E-Commerce (Nykaa)",
    "FORCE_MOTORS": "Force Motors",
    "FORTIS.NS": "Fortis Healthcare",
    "GAIL.NS": "GAIL (India)",
    "GABRIEL_INDIA": "Gabriel India",
    "GALLANTT_ISPAT_L": "Gallantt Ispat L",
    "GENINSUR.NS": "Gen Insur",
    "GODAWARI_POWER": "Godawari Power",
    "GODREJ_AGROVET": "Godrej Agrovet",
    "GODREJCP.NS": "Godrej Consumer Products",
    "GODREJPROP.NS": "Godrej Properties",
    "GRANULES.NS": "Granules India",
    "GMRINFRA.NS": "GMR Airports",
    "HAVELLS.NS": "Havells India",
    "HCLTECH.NS": "HCL Technologies",
    "HDFCBANK.NS": "HDFC Bank",
    "HDFCLIFE.NS": "HDFC Life Insurance",
    "HDFCAMC.NS": "HDFC Asset Management",
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
    "INDEGENE": "Indegene",
    "INFY.NS": "Infosys",
    "IOB.NS": "Indian Overseas Bank",
    "IOC.NS": "Indian Oil Corporation",
    "IRFC.NS": "IRFC",
    "JSWENERGY.NS": "JSW Energy",
    "JSWINFRA.NS": "JSW Infrastructure",
    "JSWSTEEL.NS": "JSW Steel",
    "JINDALSTAIN.NS": "Jindal Stainless",
    "JINDALSTEL.NS": "Jindal Steel",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "LT.NS": "Larsen & Toubro",
    "LUPIN.NS": "Lupin",
    "MAZDOCK.NS": "Mazagon Dock",
    "M&M.NS": "Mahindra & Mahindra",
    "MANKIND.NS": "Mankind Pharma",
    "MARICO.NS": "Marico",
    "MARUTI.NS": "Maruti Suzuki",
    "MAXHEALTH.NS": "Max Healthcare",
    "MRF.NS": "MRF Ltd",
    "MUTHOOTFIN.NS": "Muthoot Finance",
    "NMDC.NS": "NMDC Ltd",
    "NTPC.NS": "NTPC Limited",
    "NTPCGREEN.NS": "NTPC Green Energy",
    "NESTLEIND.NS": "Nestle India",
    "OIL.NS": "Oil India",
    "ONGC.NS": "Oil & Natural Gas Corporation",
    "ONE97.NS": "One 97 Communications (Paytm)",
    "PBFINTECH.NS": "PB Fintech (PolicyBazaar)",
    "PERSISTENT.NS": "Persistent Systems",
    "PIDILITIND.NS": "Pidilite Industries",
    "POWERFIN.NS": "Power Finance Corporation",
    "POWERGRID.NS": "Power Grid Corporation",
    "PRESTIGE.NS": "Prestige Estates",
    "RAILVIKAS.NS": "Rail Vikas Nigam",
    "RELIANCE.NS": "Reliance Industries",
    "RECLTD.NS": "REC Ltd",
    "SAMVARDHAN.NS": "Samvardhana Motherson",
    "SHREECEM.NS": "Shree Cement",
    "SHRIRAMFIN.NS": "Shriram Finance",
    "SBIN.NS": "State Bank of India",
    "SBILIFE.NS": "SBI Life Insurance",
    "SBICARD.NS": "SBI Cards",
    "SUNPHARMA.NS": "Sun Pharma Industries",
    "SUZLON.NS": "Suzlon Energy",
    "SWIGGY.NS": "Swiggy",
    "TATASTEEL.NS": "Tata Steel",
    "TATAPOWER.NS": "Tata Power Company",
    "TATAMOTORS.NS": "Tata Motors",
    "TCS.NS": "Tata Consultancy Services",
    "TECHM.NS": "Tech Mahindra",
    "TITAN.NS": "Titan Company",
    "TORNTPWR.NS": "Torn Power",
    "TORNTPHARM.NS": "Torrent Pharmaceuticals",
    "TUBEINV.NS": "Tube Investments",
    "TVSMOTOR.NS": "TVS Motor Company",
    "ULTRACEMCO.NS": "UltraTech Cement",
    "UNIONBANK.NS": "Union Bank of India",
    "UNOMINDA.NS": "Uno Minda",
    "VARUNBEV.NS": "Varun Beverages",
    "VEDANTA.NS": "Vedanta",
    "VODAFONEIDEA.NS": "Vodafone Idea",
    "WAAREE.NS": "Waaree Energies",
    "WIPRO.NS": "Wipro",
    "ZYDUSLIFE.NS": "Zydus Lifesciences",
}.items(), key=lambda x: x[0].upper()))

# --- 2. IMPROVED FETCH NEWS FUNCTION ---
@st.cache_data(ttl=600)
def fetch_news(company_name):
    """Fetch strict stock market news."""
    
    # OLD QUERY: company_name + " stock India"
    # NEW QUERY: company_name + " share price target buy sell result"
    # This forces Google to show financial news, not just general company news.
    query = f'{company_name} share price target buy sell results'
    query = query.replace(" ", "+")
    
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.findAll('item')

        articles = []
        # REMOVED: The code that skipped "Earnings" and "Results"
        # Now you will see Quarterly results!

        for item in items:
            title = item.title.text.strip()
            summary = item.description.text if item.description else ""
            summary_clean = BeautifulSoup(summary, "html.parser").get_text()
            published = item.pubDate.text if item.pubDate else None

            # Sentiment Analysis
            blob = TextBlob(summary_clean)
            sentiment_score = blob.sentiment.polarity

            articles.append({
                "title": title,
                "link": item.link.text,
                "summary": summary_clean.strip(),
                "published": published,
                "sentiment": sentiment_score
            })
            if len(articles) >= 15: break # Increased to 15 articles

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
    company_name = STOCKS[selected_ticker]

    # --- 1. PRICE & CHART SECTION ---
    # We use the Ticker (ABB.NS) for the Price
    is_valid_ticker = ".NS" in selected_ticker or ".BO" in selected_ticker
    
    if is_valid_ticker:
        with st.spinner(f"Fetching Price Chart for {selected_ticker}..."):
            stock_data = yf.download(selected_ticker, period="3mo", progress=False)
        
        if not stock_data.empty:
            # Metrics
            current_price = stock_data['Close'].iloc[-1]
            if isinstance(current_price, pd.Series): 
                 current_price = current_price.iloc[0]
            
            st.metric(label=f"{company_name} Price", value=f"₹{current_price:.2f}")
            
            # Chart
            st.subheader("Price Trend (3 Months)")
            fig = px.line(stock_data.reset_index(), x='Date', y='Close')
            st.plotly_chart(fig, use_container_width=True)

    # --- 2. NEWS SECTION ---
    st.header(f"📰 Market News for {company_name}")
    st.caption("Showing: Price targets, Buy/Sell calls, and Quarterly Results.")

    news_articles = fetch_news(company_name)

    if news_articles:
        for article in news_articles:
            # Sentiment Color
            score = article['sentiment']
            if score > 0.05:
                color = "green"
                emoji = "🟢"
            elif score < -0.05:
                color = "red"
                emoji = "🔴"
            else:
                color = "grey"
                emoji = "⚪"

            with st.expander(f"{emoji} {article['title']}"):
                st.markdown(f"**Sentiment Score:** :{color}[{score:.2f}]")
                st.write(article['summary'])
                st.markdown(f"[🔗 Read Full Article]({article['link']})")
                if article["published"]:
                    st.caption(f"Published: {article['published']}")

        # CSV download
        df = pd.DataFrame(news_articles)
        st.download_button("📥 Download News CSV", data=df.to_csv(index=False), file_name=f"{company_name}_news.csv")
    else:
        st.info(f"No recent news found for {company_name}.")

else:
    st.info("Select a stock from the sidebar to start.")
