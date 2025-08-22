
import pandas as pd

def load_data(base_path="data"):
    economic = pd.read_csv(f"{base_path}/economic.csv")
    industry = pd.read_csv(f"{base_path}/industry.csv")
    competitors = pd.read_csv(f"{base_path}/competitors.csv")
    assumptions = pd.read_csv(f"{base_path}/company_assumptions.csv")
    risks = pd.read_csv(f"{base_path}/risks.csv")
    return economic, industry, competitors, assumptions, risks

def compute_cagr(df, value_col, group_cols, start_year, end_year):
    out = []
    for keys, grp in df.groupby(group_cols):
        g = grp.set_index("year").sort_index()
        if start_year in g.index and end_year in g.index:
            v0 = g.loc[start_year, value_col]
            v1 = g.loc[end_year, value_col]
            n = end_year - start_year
            cagr = (v1 / v0) ** (1/n) - 1 if v0 > 0 else float("nan")
            rec = dict(zip(group_cols, keys if isinstance(keys, tuple) else (keys,)))
            rec.update({f"{value_col}_cagr": cagr})
            out.append(rec)
    return pd.DataFrame(out)

def get_assumption(assumptions_df, name):
    row = assumptions_df[assumptions_df["parameter"] == name]
    return float(row["value"].iloc[0]) if not row.empty else None
