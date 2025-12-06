import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import yfinance as yf
import plotly.express as px
from textblob import TextBlob

# --- 1. CONFIGURATION & LAYOUT ---
st.set_page_config(page_title="Indian Stock News Dashboard", page_icon="📈", layout="wide")

# (Keeping your original Dictionary)
STOCKS = dict(sorted({
    "ABB.NS": "ABB India",
    "ABBOTT.NS": "Abbott India",
    "AAVAS.NS": "AAVAS Financiers", # Updated to valid ticker
    "ADANIESOL.NS": "Adani Energy Solutions",
    "ADANIENT.NS": "Adani Enterprises",
    "ADANIGREEN.NS": "Adani Green",
    "ADANIPOWER.NS": "Adani Power",
    "ADANIPORTS.NS": "Adani Ports & SEZ",
    "ADANITOTAL.NS": "Adani Total Gas",
    "ADITYABIRLA.NS": "Aditya Birla Capital",
    "AB_REAL_ESTATE": "A B Real Estate", # Note: This key might not work in yfinance if not a ticker
    "AFCONS_INFRASTR": "Afcons Infrastr.",
    "ALEMBICLTD.NS": "Alembic Pharma", # Updated to valid ticker
    "ALKEM.NS": "Alkem Laboratories",
    "ALLIED_BLENDERS": "Allied Blenders",
    "ANGELONE.NS": "Angel One",
    "APOLLOHOSP.NS": "Apollo Hospitals",
    "APOLLO.MED": "Apollo Medicals",
    "ASHOKLEY.NS": "Ashok Leyland",
    "ASIANPAINT.NS": "Asian Paints",
    "AUROBINDO.NS": "Aurobindo Pharma",
    "AVENUESUPER.NS": "Avenue Supermarts",
    "AXISBANK.NS": "Axis Bank",
    "BANKBARODA.NS": "Bank of Baroda",
    "BAYERCROP.NS": "Bayer Crop Sci.",
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
    "CAMS.NS": "Cams Services",
    "CAPLIPOINT.NS": "Caplin Point Lab",
    "CASTROLIND.NS": "Castrol India",
    "CESC.NS": "CESC",
    "CHAMBLFERT.NS": "Chambal Fert.",
    "CHOLAFIN.NS": "Cholamandalam Investment & Finance",
    "CIPLA.NS": "Cipla",
    "COALINDIA.NS": "Coal India",
    "COLPAL.NS": "Colgate-Palmolive",
    "COROMANDEL.NS": "Coromandel International",
    "CUMMINSIND.NS": "Cummins India",
    "DABUR.NS": "Dabur India",
    "DEEPAKFERT.NS": "Deepak Fertilis.",
    "DEEPAKNTR.NS": "Deepak Nitrite",
    "DEVYANI.NS": "Devyani Intl.",
    "DLF.NS": "DLF Ltd",
    "DIVISLAB.NS": "Divi's Laboratories",
    "DRREDDY.NS": "Dr Reddy's Laboratories",
    "EICHERMOT.NS": "Eicher Motors",
    "FSN.NS": "FSN E-Commerce (Nykaa)",
    "FORTIS.NS": "Fortis Healthcare",
    "GAIL.NS": "GAIL (India)",
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
    "HPCL.NS": "Hindustan Petroleum",
    "ICICIBANK.NS": "ICICI Bank",
    "ICICILOMBARD.NS": "ICICI Lombard",
    "ICICIPRULI.NS": "ICICI Prudential Life",
    "IDBI.NS": "IDBI Bank",
    "INDHOTEL.NS": "Indian Hotels Company",
    "INDIANB.NS": "Indian Bank",
    "INDIGO.NS": "InterGlobe Aviation",
    "INFY.NS": "Infosys",
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


# --- 2. FETCH NEWS FUNCTION ---
@st.cache_data(ttl=600)
def fetch_news(company_name):
    """Fetch top 10 news articles from Google News RSS."""
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
            if any(keyword.lower() in title.lower() for keyword in skip_keywords):
                continue

            summary = item.description.text if item.description else "No description available"
            summary_clean = BeautifulSoup(summary, "html.parser").get_text()
            published = item.pubDate.text if item.pubDate else None

            # --- NEW: Sentiment Analysis ---
            blob = TextBlob(summary_clean)
            sentiment_score = blob.sentiment.polarity

            articles.append({
                "title": title,
                "link": item.link.text,
                "summary": summary_clean.strip(),
                "published": published,
                "sentiment": sentiment_score
            })

            if len(articles) >= 10:
                break

        return articles

    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []

# --- 3. MAIN APP ---
st.title("Indian Stock News Dashboard 🇮🇳📈")

# Sidebar
st.sidebar.header("Stock Selection")
search_query = st.sidebar.text_input("Search Stock by Name or Ticker:")
filtered_stocks = {k: v for k, v in STOCKS.items() if search_query.lower() in k.lower() or search_query.lower() in v.lower()}
selected_ticker = st.sidebar.selectbox("Select a Stock:", options=["--- Select a Stock ---"] + list(filtered_stocks.keys()))

# --- 4. INTERACTIVE LOGIC ---
if selected_ticker != "--- Select a Stock ---":
    company_name = STOCKS[selected_ticker]
    
    # --- A. FETCH STOCK PRICE (yfinance) ---
    # We attempt to fetch price if the key looks like a ticker (e.g., ends in .NS)
    # If your dictionary key is just a name (e.g. "Aditya Infotech"), yfinance will fail gracefully.
    stock_data = pd.DataFrame() 
    with st.spinner(f"Analyzing {company_name}..."):
        try:
            # Get 3 months of data
            stock_data = yf.download(selected_ticker, period="3mo", progress=False)
        except Exception:
            pass # Ignore if ticker is invalid

        # Fetch News
        news_articles = fetch_news(company_name)

    # --- B. DISPLAY METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    
    # Price Metric
    if not stock_data.empty:
        try:
            current_price = float(stock_data['Close'].iloc[-1])
            prev_price = float(stock_data['Close'].iloc[-2])
            price_change = current_price - prev_price
            col1.metric("Current Price", f"₹{current_price:,.2f}", f"{price_change:.2f}")
        except:
            col1.metric("Price", "N/A")
    else:
        col1.metric("Price", "No Data")

    # Sentiment Metrics
    if news_articles:
        pos_news = sum(1 for a in news_articles if a['sentiment'] > 0.05)
        neg_news = sum(1 for a in news_articles if a['sentiment'] < -0.05)
        col2.metric("Total Articles", len(news_articles))
        col3.metric("Positive News", f"{pos_news} 🟢")
        col4.metric("Negative News", f"{neg_news} 🔴")
    
    st.markdown("---")

    # --- C. PRICE CHART (Plotly) ---
    if not stock_data.empty:
        st.subheader(f"Price Trend: {company_name}")
        # Reset index so 'Date' is a column accessible to Plotly
        chart_data = stock_data.reset_index()
        fig = px.line(chart_data, x='Date', y='Close', title=f'{selected_ticker} - 3 Month Performance')
        fig.update_layout(xaxis_title="Date", yaxis_title="Price (INR)", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    
    # --- D. NEWS LIST (With Expanders) ---
    st.subheader(f"📰 Latest News Analysis")
    st.caption(f"Last updated: {datetime.now().strftime('%b %d, %Y %I:%M %p')}")

    if news_articles:
        for article in news_articles:
            # Determine Color based on sentiment
            score = article['sentiment']
            if score > 0.05:
                sentiment_label = "🟢 Bullish"
                color = "green"
            elif score < -0.05:
                sentiment_label = "🔴 Bearish"
                color = "red"
            else:
                sentiment_label = "⚪ Neutral"
                color = "grey"

            # Expander for interactivity
            with st.expander(f"{sentiment_label} | {article['title']}"):
                st.markdown(f"**Source:** Google News | **Sentiment Score:** :{color}[{score:.2f}]")
                st.write(article['summary'])
                st.markdown(f"[🔗 Read Full Article]({article['link']})")
                if article["published"]:
                     st.caption(f"Published: {article['published']}")

        # CSV Download
        df_news = pd.DataFrame(news_articles)
        st.download_button("📥 Download News CSV", data=df_news.to_csv(index=False), file_name=f"{company_name}_news.csv")

    else:
        st.info(f"No recent news found for {company_name} (Earnings reports filtered out).")

else:
    st.info("Select a stock from the sidebar to view the dashboard.")
