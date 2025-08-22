
import pandas as pd
from data_prep import get_assumption

def project_financials(industry_df, assumptions_df, market, start_year=2021, horizon_years=5):
    d = industry_df[(industry_df["market"] == market) & (industry_df["year"] >= start_year)].copy()
    d = d.sort_values("year").head(horizon_years)

    revenue = d["target_som_billion_usd"] * 1000  # convert to million USD
    capex_initial = get_assumption(assumptions_df, "capex_initial_musd")
    fixed_costs = get_assumption(assumptions_df, "fixed_costs_annual_musd")
    var_pct = get_assumption(assumptions_df, "variable_cost_pct_revenue")
    tax_rate = get_assumption(assumptions_df, "tax_rate")
    discount_rate = get_assumption(assumptions_df, "discount_rate")

    df = pd.DataFrame({
        "year": d["year"].values,
        "revenue_musd": revenue.values,
    })
    df["cogs_musd"] = df["revenue_musd"] * var_pct
    df["gross_profit_musd"] = df["revenue_musd"] - df["cogs_musd"]
    df["opex_musd"] = fixed_costs
    df["ebit_musd"] = df["gross_profit_musd"] - df["opex_musd"]
    df["tax_musd"] = (df["ebit_musd"].clip(lower=0)) * tax_rate
    df["nopat_musd"] = df["ebit_musd"] - df["tax_musd"]
    df["fcf_musd"] = df["nopat_musd"]

    cash_flows = [-capex_initial] + df["fcf_musd"].tolist()

    npv = 0.0
    cumulative = 0.0
    payback_year = None
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate) ** t)
    for t, cf in enumerate(cash_flows):
        cumulative += cf
        if cumulative >= 0 and payback_year is None:
            payback_year = t
    return df, npv, payback_year
