# 🇮🇹 Italian Portfolio Monte Carlo — Streamlit App

A web-based Monte Carlo simulation for modelling portfolio longevity net of
Italian taxes (deferred CGT model) with inflation-adjusted withdrawals.

---

## How to Deploy (Streamlit Community Cloud — Free, Shareable Link)

### Step 1: Create a GitHub account
Go to github.com and sign up if you don't have one.

### Step 2: Create a new repository
1. Click the "+" icon → "New repository"
2. Name it something like `italian-portfolio-mc`
3. Set it to **Public**
4. Click "Create repository"

### Step 3: Upload the files
Upload both files to the repository:
- `app.py`
- `requirements.txt`

You can drag and drop them directly into the GitHub web interface.

### Step 4: Deploy on Streamlit Cloud
1. Go to share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and set the main file to `app.py`
5. Click "Deploy"

Within 2–3 minutes you will have a public URL like:
`https://yourname-italian-portfolio-mc-app-xxxxx.streamlit.app`

Share this link with anyone — they can use the app in their browser
with no installation required.

---

## How to Run Locally (on your Mac)

If you want to run it on your own machine:

1. Install Python from python.org (if not already installed)
2. Open Terminal and run:

```bash
pip install streamlit numpy matplotlib pandas
streamlit run app.py
```

The app will open automatically in your browser at http://localhost:8501

---

## What the App Does

- **Sidebar controls**: adjust portfolio value, withdrawal, horizon,
  asset allocation, return assumptions, and Italian tax regime
- **Run Simulation button**: runs 10,000 Monte Carlo paths
- **4 charts**: fan chart, survival curve, terminal value distribution,
  withdrawal sensitivity
- **Year-by-year table**: median, 10th/90th percentile, and survival
  rate for every year
- **Scenario comparison**: quick side-by-side of 6 preset scenarios

## Tax Model

The app implements a deferred CGT model (Level 1 + 2):
- **Level 1**: Only dividend/coupon income is taxed annually (26% equities,
  12.5% BTPs). Price appreciation is deferred until disposal.
- **Level 2**: On each withdrawal, CGT is only applied to the gain portion
  of units sold, calculated against a tracked cost basis.

---

*For illustrative purposes only. Not financial advice.*
