
# Market Entry Strategy Dashboard (Bain-style)

This project showcases a hypothesis-driven market entry case with a runnable Streamlit dashboard and CSV data. It’s designed to mirror a consulting-style workflow: **Problem → Hypotheses → Analyses → Recommendation**.

## 📦 What’s Inside
```
market_entry_dashboard/
├── data/
│   ├── economic.csv
│   ├── industry.csv
│   ├── competitors.csv
│   ├── company_assumptions.csv
│   └── risks.csv
├── data_prep.py
├── model.py
├── streamlit_app.py
└── README.md
```

## 🧠 Hypotheses (Bain-style)
- **H1: Market attractiveness:** Market GDP & industry TAM are large and growing.
- **H2: Competitive dynamics:** Competition is fragmented with accessible positioning gaps.
- **H3: Financial feasibility:** Entry yields positive NPV and fast payback under base-case assumptions.

## 📂 Datasets (CSV)
- `economic.csv`: GDP, inflation, unemployment for candidate markets (2019–2024).
- `industry.csv`: TAM/SAM/target SOM for **Consumer Electronics** by market (2019–2024).
- `competitors.csv`: Top-5 competitors with market share, price index, differentiation (1–5).
- `company_assumptions.csv`: CAPEX, fixed costs, variable costs %, tax & discount rates.
- `risks.csv`: Likelihood and impact (1–5 scale) for a simple risk matrix.

## ⚙️ How the Code Fits Together
- `data_prep.py`
  - `load_data()`: Reads CSVs.
  - `compute_cagr()`: Utility to compute CAGR across years.
- `model.py`
  - `project_financials(...)`: Builds a simple P&L and FCF projection; returns table, NPV, payback.
- `streamlit_app.py`
  - Interactive dashboard with 4 sections: **Market Attractiveness**, **Competitive Landscape**, **Financial Feasibility**, **GTM & Risks**.

## 🚀 Run Locally
1) (Recommended) Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```
2) Install dependencies
```bash
pip install streamlit pandas numpy matplotlib
```
3) Launch the app
```bash
cd market_entry_dashboard
streamlit run streamlit_app.py
```
4) Open the Streamlit URL printed in your terminal.

## 🧪 Customize & Extend
- Change markets, years, or industries by editing the CSVs in `data/`.
- Tweak `company_assumptions.csv` to run alternate scenarios (e.g., discount rate, costs).
- Add a new page for **scenario analysis** (best/base/worst case).
- Add real data (World Bank, OECD, Statista) by replacing the mock CSVs.

## 📝 Executive-Style Output
Use the **Executive Summary** section inside the app as a template for your slide deck. Export charts directly from the app or reproduce them in PowerPoint/Canva with the same logic.
