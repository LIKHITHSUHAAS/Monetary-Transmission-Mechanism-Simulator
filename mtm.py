import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="MTM Simulator", layout="wide")
st.title("📊 Monetary Transmission Mechanism (MTM) Simulator")

# ---------- Helper Function ----------
def show_bar_chart(labels, values, title):
    fig, ax = plt.subplots()
    ax.barh(labels, values, color='skyblue')
    ax.set_title(title)
    for i, val in enumerate(values):
        ax.text(val + 0.5, i, f"{val:.2f}", va='center')
    st.pyplot(fig)

# ---------- MTM Channel Functions ----------

def interest_rate_channel(repo_rate):
    lending_rate = 8.0 + 0.6 * (repo_rate - 5.0)
    loan_demand = max(0, 200 - 10 * lending_rate)
    investment = loan_demand * 0.7
    gdp_growth = 2.5 + 0.03 * investment
    return ["Lending Rate", "Loan Demand", "Investment", "GDP Growth"], [lending_rate, loan_demand, investment, gdp_growth]

def credit_channel(crr):
    credit_supply = 1000 - (crr - 4.0) * 40
    private_investment = credit_supply * 0.65
    sme_loans = credit_supply * 0.25
    job_creation = sme_loans * 10
    gdp_growth = 2.0 + 0.025 * private_investment
    return ["Credit Supply", "Private Investment", "SME Loans", "Jobs Created", "GDP Growth"], [credit_supply, private_investment, sme_loans, job_creation, gdp_growth]

def asset_price_channel(interest_rate):
    stock_index = 60000 - 1000 * (interest_rate - 6.0)
    real_estate_index = 120 - 2.5 * (interest_rate - 6.0)
    wealth_index = stock_index * 0.5 + real_estate_index * 1.5
    confidence = 70 + 0.01 * wealth_index
    consumption = 150 + 0.5 * confidence
    gdp_growth = 2.5 + 0.02 * consumption
    return ["Stock Index", "Real Estate", "Confidence", "Consumption", "GDP Growth"], [stock_index, real_estate_index, confidence, consumption, gdp_growth]

def exchange_rate_channel(repo_rate):
    exchange_rate = 80 + 0.8 * (repo_rate - 5.0)
    exports = 250 - 1.5 * (exchange_rate - 80)
    imports = 300 + 1.8 * (exchange_rate - 80)
    net_exports = exports - imports
    inflation = 4 + 0.02 * max(0, -net_exports)
    gdp = 2.5 + 0.015 * exports
    return ["Exchange Rate", "Exports", "Imports", "Net Exports", "Inflation", "GDP Growth"], [exchange_rate, exports, imports, net_exports, inflation, gdp]

def expectations_channel(exp_infl):
    wage_growth = 5 + 0.3 * exp_infl
    cost_infl = 3 + 0.5 * exp_infl
    consumption = 200 - 4 * exp_infl
    investment = 180 - 3.5 * exp_infl
    gdp_growth = 1.5 + 0.015 * consumption + 0.02 * investment - 0.1 * exp_infl
    return ["Wage Growth", "Cost Inflation", "Consumption", "Investment", "GDP Growth"], [wage_growth, cost_infl, consumption, investment, gdp_growth]

# ---------- TABS ----------
tabs = st.tabs([
    "📉 Interest Rate",
    "🏦 Credit",
    "🏠 Asset Price",
    "💱 Exchange Rate",
    "🔮 Expectations"
])

with tabs[0]:
    st.subheader("Interest Rate Channel")
    repo = st.slider("Repo Rate (%)", 2.0, 10.0, 5.0, step=0.25)
    labels, values = interest_rate_channel(repo)
    show_bar_chart(labels, values, "Impact of Repo Rate")

with tabs[1]:
    st.subheader("Credit Channel")
    crr = st.slider("CRR (%)", 3.0, 6.0, 4.0, step=0.1)
    labels, values = credit_channel(crr)
    show_bar_chart(labels, values, "Impact of CRR on Credit")

with tabs[2]:
    st.subheader("Asset Price Channel")
    ir = st.slider("Interest Rate (%)", 3.0, 10.0, 6.0, step=0.25)
    labels, values = asset_price_channel(ir)
    show_bar_chart(labels, values, "Impact of Asset Prices")

with tabs[3]:
    st.subheader("Exchange Rate Channel")
    repo2 = st.slider("Repo Rate (%)", 2.0, 10.0, 5.0, step=0.25, key="repo_exchange")
    labels, values = exchange_rate_channel(repo2)
    show_bar_chart(labels, values, "Impact on Exchange Rate and Trade")

with tabs[4]:
    st.subheader("Expectations Channel")
    expected_infl = st.slider("Expected Inflation (%)", 1.0, 10.0, 4.0, step=0.25, key="expected_inflation")
    labels, values = expectations_channel(expected_infl)
    show_bar_chart(labels, values, "Impact of Inflation Expectations")