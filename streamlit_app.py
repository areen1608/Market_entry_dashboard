
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_prep import load_data, compute_cagr
from model import project_financials

st.set_page_config(page_title="Market Entry Strategy Dashboard", layout="wide")

st.title("Market Entry Strategy Dashboard")
st.caption("A Bain-style, hypothesis-driven project using mock CSV data.")

economic, industry, competitors, assumptions, risks = load_data()

# Sidebar controls
markets = sorted(economic["market"].unique())
years = sorted(economic["year"].unique())
industry_name = industry["industry"].iloc[0]

st.sidebar.header("Controls")
market = st.sidebar.selectbox("Select Market", markets, index=0)
start_year = st.sidebar.selectbox("Start Year", years, index=max(0, len(years)-5))
end_year = st.sidebar.selectbox("End Year", years, index=len(years)-1)

st.sidebar.markdown("---")
st.sidebar.subheader("Hypotheses")
st.sidebar.write("H1: Market is attractive (growth & size).")
st.sidebar.write("H2: Fragmented competition allows entry.")
st.sidebar.write("H3: Financials yield positive NPV & fast payback.")

# ----- Section 1: Market Attractiveness -----
st.header("1) Market Attractiveness")

col1, col2 = st.columns(2)
with col1:
    st.subheader("GDP Trend")
    eg = economic[(economic["market"] == market) & (economic["year"].between(start_year, end_year))]
    fig1, ax1 = plt.subplots()
    ax1.plot(eg["year"], eg["gdp_trillions_usd"])
    ax1.set_xlabel("Year")
    ax1.set_ylabel("GDP (Trillions USD)")
    ax1.set_title(f"{market} GDP Trend")
    st.pyplot(fig1)

with col2:
    st.subheader(f"{industry_name}: TAM & SAM")
    ig = industry[(industry["market"] == market) & (industry["year"].between(start_year, end_year))]
    fig2, ax2 = plt.subplots()
    ax2.plot(ig["year"], ig["tam_billion_usd"], label="TAM")
    ax2.plot(ig["year"], ig["sam_billion_usd"], label="SAM")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Market Size (Billion USD)")
    ax2.set_title(f"{market} {industry_name} TAM vs SAM")
    ax2.legend()
    st.pyplot(fig2)

cagr_df = compute_cagr(industry, "tam_billion_usd", ["market"], years[0], years[-1])
st.write("**CAGR by Market (TAM)**")
st.dataframe(cagr_df.round(3))

# ----- Section 2: Competitive Landscape -----
st.header("2) Competitive Landscape")

cc = competitors[competitors["market"] == market].copy()
left, right = st.columns([1,1])
with left:
    st.subheader("Competitor Shares & Pricing")
    st.dataframe(cc[["competitor","market_share_pct","price_index_vs_avg","differentiation_score"]].sort_values("market_share_pct", ascending=False))

with right:
    st.subheader("Simple Heatmap: Differentiation vs Price Index")
    fig3, ax3 = plt.subplots()
    ax3.scatter(cc["price_index_vs_avg"], cc["differentiation_score"])
    for _, row in cc.iterrows():
        ax3.annotate(row["competitor"], (row["price_index_vs_avg"], row["differentiation_score"]))
    ax3.set_xlabel("Price Index vs Market Avg (~1.0 is average)")
    ax3.set_ylabel("Differentiation (1-5)")
    ax3.set_title(f"{market}: Positioning Map")
    st.pyplot(fig3)

# ----- Section 3: Financial Feasibility -----
st.header("3) Financial Feasibility")

proj_df, npv, payback_year = project_financials(industry, assumptions, market, start_year=max(years[0], years[-1]-4), horizon_years=5)
st.subheader("Projected P&L & Cash Flows (Million USD)")
st.dataframe(proj_df.round(2))

fig4, ax4 = plt.subplots()
ax4.plot(proj_df["year"], proj_df["fcf_musd"])
ax4.set_xlabel("Year")
ax4.set_ylabel("Free Cash Flow (MUSD)")
ax4.set_title(f"{market}: Free Cash Flow Projection")
st.pyplot(fig4)

st.metric("NPV (MUSD, discounted)", f"{npv:,.1f}")
st.metric("Payback (years from start)", "N/A" if payback_year is None else int(payback_year))

# ----- Section 4: Go-to-Market Strategy & Risks -----
st.header("4) Go-to-Market Strategy & Risks")
gtm_mode = st.selectbox("Preferred Entry Mode", ["Greenfield (Organic)", "Joint Venture", "Acquisition"], index=1)
st.write("**Rationale Template:**")
st.write(
    "- If the market is **fast-growing** and **fragmented**, a **JV** can speed access while sharing risk.\n"
    "- If there is a clear acquisition target with synergy, consider **Acquisition**.\n"
    "- If barriers are low and capabilities are strong, **Organic** entry may maximize control and margin."
)

st.subheader("Risk Matrix (Likelihood x Impact)")
risk_df = risks.copy()
risk_df["score"] = risk_df["likelihood"] * risk_df["impact"]
st.dataframe(risk_df.sort_values("score", ascending=False))

fig5, ax5 = plt.subplots()
ax5.scatter(risk_df["likelihood"], risk_df["impact"], s=risk_df["score"]*20)
for _, r in risk_df.iterrows():
    ax5.annotate(r["risk"], (r["likelihood"], r["impact"]))
ax5.set_xlabel("Likelihood (1-5)")
ax5.set_ylabel("Impact (1-5)")
ax5.set_title("Risk Bubble Chart")
st.pyplot(fig5)

# ----- Executive Summary Snippet -----
st.header("Executive Summary (Auto-Generated Template)")
st.write(
    f"- **H1 (Market Attractiveness):** {market}'s {industry_name} TAM CAGR and GDP trend suggest attractiveness relative to peers.\n"
    f"- **H2 (Competition):** Positioning shows varying price/differentiation; potential white spaces exist.\n"
    f"- **H3 (Financials):** Projected NPV = {npv:,.1f} MUSD; payback = {'N/A' if payback_year is None else int(payback_year)} years.\n"
    f"- **Recommended Entry Mode:** {gtm_mode} (based on control, speed, and risk share)."
)

st.caption("Adjust assumptions in data/company_assumptions.csv to test scenarios.")
