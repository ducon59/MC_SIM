import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Patch
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Italian Portfolio Monte Carlo",
    page_icon="🇮🇹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS styling ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@300;400;500;600&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* Main background */
  .stApp { background-color: #f0f4f8; }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background-color: #1a2332;
  }
  section[data-testid="stSidebar"] * {
    color: #e8edf2 !important;
  }
  section[data-testid="stSidebar"] input {
    color: #1a2332 !important;
    background-color: #ffffff !important;
}

section[data-testid="stSidebar"] input::placeholder {
    color: #6b7c93 !important;
}
  section[data-testid="stSidebar"] .stSlider label,
  section[data-testid="stSidebar"] .stNumberInput label,
  section[data-testid="stSidebar"] .stSelectbox label {
    color: #b8c8d8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
  }
  section[data-testid="stSidebar"] hr {
    border-color: #2e4a6b !important;
  }
  section[data-testid="stSidebar"] h3 {
    color: #b8963e !important;
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.0rem !important;
    margin-top: 1.2rem !important;
  }

  /* Metric cards */
  div[data-testid="metric-container"] {
    background: white;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    border-left: 4px solid #b8963e;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
  }
  div[data-testid="metric-container"] label {
    color: #6b7c93 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
  }
  div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #1a2332 !important;
    font-size: 1.6rem !important;
    font-weight: 600 !important;
  }
  div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
    font-size: 0.82rem !important;
  }

  /* Section headers */
  .section-header {
    font-family: 'DM Serif Display', serif;
    color: #1a2332;
    font-size: 1.4rem;
    margin-top: 2rem;
    margin-bottom: 0.2rem;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid #b8963e;
  }

  /* Page title */
  .page-title {
    font-family: 'DM Serif Display', serif;
    color: #1a2332;
    font-size: 2.4rem;
    font-weight: 400;
    letter-spacing: -0.01em;
  }
  .page-subtitle {
    color: #6b7c93;
    font-size: 0.95rem;
    margin-top: -0.5rem;
    margin-bottom: 1.5rem;
  }

  /* Info / warning boxes */
  .info-box {
    background: #ffffff;
    border-left: 4px solid #2aab96;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
    color: #1a2332;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  }
  .warn-box {
    background: #fff9f0;
    border-left: 4px solid #d4903a;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
    color: #1a2332;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  }

  /* Table styling */
  .dataframe { font-size: 0.85rem !important; }

  /* Run button */
  div[data-testid="stButton"] button {
    background: #b8963e !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 2px 8px rgba(184,150,62,0.3) !important;
  }
  div[data-testid="stButton"] button:hover {
    background: #9a7d32 !important;
    box-shadow: 0 4px 12px rgba(184,150,62,0.4) !important;
  }

  /* Hide Streamlit branding */
  #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Colour palette ────────────────────────────────────────────────────────────
C_GOLD  = "#b8963e"
C_BLUE  = "#3a7ebf"
C_TEAL  = "#2aab96"
C_RED   = "#c94f4f"
C_AMBER = "#d4903a"
C_BG    = "#f0f4f8"
C_PANEL = "#ffffff"
C_DARK  = "#1a2332"
C_DIM   = "#6b7c93"
C_GRID  = "#dde4ed"

plt.rcParams.update({
    "font.family":        "serif",
    "font.serif":         ["DejaVu Serif"],
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.spines.left":   False,
    "axes.spines.bottom": False,
    "axes.grid":          True,
    "grid.color":         C_GRID,
    "grid.linewidth":     0.6,
    "axes.facecolor":     C_PANEL,
    "figure.facecolor":   C_BG,
    "xtick.color":        C_DIM,
    "ytick.color":        C_DIM,
    "xtick.labelsize":    9,
    "ytick.labelsize":    9,
    "axes.labelcolor":    C_DIM,
    "text.color":         C_DARK,
})

# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR — INPUTS
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🇮🇹 Monte Carlo\n### Portfolio Settings")

    portfolio = st.number_input(
        "Initial Portfolio (€)",
        min_value=100_000, max_value=50_000_000,
        value=1_000_000, step=100_000,
        format="%d"
    )
    withdrawal = st.number_input(
        "Annual Withdrawal — Real (€)",
        min_value=10_000, max_value=1_000_000,
        value=100_000, step=5_000,
        format="%d"
    )
    years = st.slider("Projection Horizon (years)", 10, 50, 30)
    simulations = st.select_slider(
        "Simulations",
        options=[1_000, 2_000, 5_000, 10_000, 25_000, 50_000],
        value=10_000
    )

    st.markdown("---")
    st.markdown("### Macro Assumptions")
    inflation = st.slider("Inflation Rate (%)", 0.0, 8.0, 2.5, 0.5, format="%.1f%%") / 100
    ivafe     = st.slider("IVAFE Wealth Tax (%)", 0.0, 0.5, 0.2, 0.1, format="%.1f%%") / 100

    st.markdown("---")
    st.markdown("### Asset Allocation")
    st.caption("Allocations must sum to 100%")

    eq_alloc  = st.slider("Global Equities",     0, 100, 95, 1, format="%d%%")
    btp_alloc = st.slider("EU Govt Bonds (BTP)", 0, 100,  3, 1, format="%d%%")
    cash_alloc = 100 - eq_alloc - btp_alloc

    alloc_sum = eq_alloc + btp_alloc + cash_alloc
    if cash_alloc < 0:
        st.error(f"Allocation exceeds 100% — reduce Equities or Bonds.")
        cash_alloc = 0
    else:
        st.info(f"Cash / Deposits: **{cash_alloc}%** (auto-calculated)")

    st.markdown("---")
    st.markdown("### Return Assumptions")
    eq_return   = st.slider("Equity Gross Return (%)",    1.0, 15.0, 7.0, 0.5, format="%.1f%%") / 100
    eq_vol      = st.slider("Equity Volatility σ (%)",  5.0, 40.0, 16.0, 0.5, format="%.1f%%") / 100
    eq_income   = st.slider("Equity Income / Dividend Yield (%)", 0.0, 5.0, 1.5, 0.5, format="%.1f%%") / 100
    btp_return  = st.slider("BTP Gross Return (%)",   1.0, 10.0, 3.5, 0.5, format="%.1f%%") / 100
    cash_return = st.slider("Cash Return (%)",        0.0,  8.0, 2.5, 0.5, format="%.1f%%") / 100

    st.markdown("---")
    st.markdown("### Tax Regime")
    tax_regime = st.selectbox(
        "Active Tax Regime",
        ["Standard Italian (26%)", "Flat Tax (€200K lump sum)", "7% Retiree Regime"]
    )
    if tax_regime == "Flat Tax (€200K lump sum)":
        flat_tax_amount = st.number_input("Annual Flat Tax (€)", value=200_000, step=10_000)
    else:
        flat_tax_amount = 0

    st.markdown("---")
    run_button = st.button("▶  Run Simulation")

# ════════════════════════════════════════════════════════════════════════════
# MAIN PANEL — HEADER
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="page-title">Italian Portfolio Monte Carlo</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-subtitle">Deferred CGT model &nbsp;·&nbsp; Inflation-adjusted withdrawals &nbsp;·&nbsp; Italian tax treatment</p>',
    unsafe_allow_html=True
)

# ── Validate allocation ───────────────────────────────────────────────────────
if cash_alloc < 0:
    st.error("Asset allocation exceeds 100%. Please adjust the sliders in the sidebar.")
    st.stop()

# ════════════════════════════════════════════════════════════════════════════
# DERIVED PARAMETERS
# ════════════════════════════════════════════════════════════════════════════
eq_a    = eq_alloc   / 100
btp_a   = btp_alloc  / 100
cash_a  = cash_alloc / 100

# Tax rates by asset
eq_tax   = 0.26
btp_tax  = 0.125
cash_tax = 0.26

# Level 1: split income vs price return
eq_price   = eq_return - eq_income
btp_income = btp_return   # all coupon
cash_income = cash_return  # all interest

# Weighted portfolio params
mu_gross  = eq_a * eq_return + btp_a * btp_return + cash_a * cash_return
sigma     = eq_a * eq_vol + btp_a * 0.05 + cash_a * 0.005

# Effective net return (Level 1 — income taxed annually, price deferred)
eq_net_annual   = eq_income * (1 - eq_tax) + eq_price
btp_net_annual  = btp_income * (1 - btp_tax)
cash_net_annual = cash_income * (1 - cash_tax)
mu_net = (eq_a * eq_net_annual + btp_a * btp_net_annual + cash_a * cash_net_annual) - ivafe

# Flat tax regime override
if tax_regime == "Flat Tax (€200K lump sum)":
    flat_tax_drag = flat_tax_amount / portfolio
    mu_net = mu_gross - flat_tax_drag - ivafe
elif tax_regime == "7% Retiree Regime":
    mu_net = mu_gross * (1 - 0.07) - ivafe

withdrawal_rate = withdrawal / portfolio
perpetuity_rate = withdrawal / portfolio
surplus = mu_net - perpetuity_rate

# Annual income tax drag (for Level 2 disposal calc)
portfolio_income_tax = (eq_a * eq_income * eq_tax +
                        btp_a * btp_income * btp_tax +
                        cash_a * cash_income * cash_tax)
weighted_cgt = eq_a * eq_tax + btp_a * btp_tax + cash_a * cash_tax

# ════════════════════════════════════════════════════════════════════════════
# ASSUMPTION SUMMARY CARDS (always visible)
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-header">Portfolio Parameters</p>', unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Portfolio",        f"€{portfolio/1e6:.2f}M")
c2.metric("Annual Withdrawal", f"€{withdrawal:,.0f}")
c3.metric("Withdrawal Rate",   f"{withdrawal_rate:.2%}")
c4.metric("Gross Return (μ)",  f"{mu_gross:.2%}")
c5.metric("Net Return (μ)",    f"{mu_net:.2%}",
          delta=f"{surplus:+.2%} vs required",
          delta_color="normal")
c6.metric("Volatility (σ)",    f"{sigma:.2%}")

# Sustainability callout
if surplus > 0.01:
    st.markdown(f'<div class="info-box">✅  <strong>Portfolio appears self-sustaining</strong> in the median scenario. Net return ({mu_net:.2%}) exceeds the perpetuity rate ({perpetuity_rate:.2%}) by {surplus:.2%}. The portfolio should grow in real terms over time on average.</div>', unsafe_allow_html=True)
elif surplus > -0.01:
    st.markdown(f'<div class="warn-box">⚠️  <strong>Near the sustainability threshold.</strong> Net return ({mu_net:.2%}) is close to the perpetuity rate ({perpetuity_rate:.2%}). Small changes in return assumptions or withdrawal could tip this either way.</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="warn-box">⚠️  <strong>Drawing down capital</strong> in the median scenario. Net return ({mu_net:.2%}) is below the perpetuity rate ({perpetuity_rate:.2%}) by {abs(surplus):.2%}. The simulation will show how long the portfolio is likely to last.</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# RUN SIMULATION
# ════════════════════════════════════════════════════════════════════════════
# Build a signature of all inputs — if anything changes, clear stale results
sim_signature = (portfolio, withdrawal, years, simulations, inflation, ivafe,
                 eq_alloc, btp_alloc, eq_return, eq_vol, eq_income,
                 btp_return, cash_return, tax_regime)
if "sim_signature" not in st.session_state or st.session_state["sim_signature"] != sim_signature:
    st.session_state.pop("sim_results", None)
    st.session_state["sim_signature"] = sim_signature

if run_button or "sim_results" not in st.session_state:

    with st.spinner(f"Running {simulations:,} simulations..."):

        np.random.seed(None)
        paths      = np.zeros((simulations, years + 1))
        paths[:, 0] = portfolio
        cost_basis  = np.full(simulations, float(portfolio))

        for yr in range(1, years + 1):
            prev         = paths[:, yr - 1]
            shocks       = np.random.normal(mu_gross, sigma, simulations)
            gross_value  = prev * (1 + shocks)

            inc_tax      = prev * portfolio_income_tax
            real_wd      = withdrawal * (1 + inflation) ** yr
            cash_needed  = real_wd + inc_tax + prev * ivafe

            gain_ratio   = np.maximum(0, (gross_value - cost_basis) / np.maximum(gross_value, 1))
            d_factor     = np.maximum(1 - gain_ratio * weighted_cgt, 0.5)
            total_out    = cash_needed / d_factor
            sold_frac    = np.minimum(total_out / np.maximum(gross_value, 1), 1.0)

            cost_basis   = cost_basis * (1 - sold_frac)
            paths[:, yr] = np.maximum(0, gross_value - total_out)
            cost_basis   = np.where(paths[:, yr] <= 0, 0, cost_basis)

        # Statistics
        final_values  = paths[:, -1]
        survived      = final_values > 0
        survival_rate = survived.mean()

        depletion_years = []
        for path in paths[~survived]:
            dy = np.argmax(path == 0)
            depletion_years.append(dy)

        pct_10 = np.percentile(paths, 10,  axis=0)
        pct_25 = np.percentile(paths, 25,  axis=0)
        pct_50 = np.percentile(paths, 50,  axis=0)
        pct_75 = np.percentile(paths, 75,  axis=0)
        pct_90 = np.percentile(paths, 90,  axis=0)

        deflator    = np.array([(1 + inflation) ** yr for yr in range(years + 1)])
        pct_50_real = pct_50 / deflator

        st.session_state["sim_results"] = {
            "paths": paths, "final_values": final_values,
            "survived": survived, "survival_rate": survival_rate,
            "depletion_years": depletion_years,
            "pct_10": pct_10, "pct_25": pct_25, "pct_50": pct_50,
            "pct_75": pct_75, "pct_90": pct_90, "pct_50_real": pct_50_real,
        }

# ── Pull results from session state ──────────────────────────────────────────
r = st.session_state["sim_results"]
paths         = r["paths"]
final_values  = r["final_values"]
survived      = r["survived"]
survival_rate = r["survival_rate"]
depletion_years = r["depletion_years"]
pct_10, pct_25, pct_50, pct_75, pct_90 = r["pct_10"], r["pct_25"], r["pct_50"], r["pct_75"], r["pct_90"]
pct_50_real   = r["pct_50_real"]
depleted_count = (~survived).sum()
# Derive years_axis from stored paths shape to avoid mismatch
# if the years slider changes before re-running the simulation
years_axis     = np.arange(paths.shape[1])
years          = paths.shape[1] - 1   # keep years consistent with stored results

# ════════════════════════════════════════════════════════════════════════════
# RESULTS METRICS
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-header">Simulation Results</p>', unsafe_allow_html=True)

r1, r2, r3, r4, r5 = st.columns(5)
surv_color = "normal" if survival_rate >= 0.8 else "inverse"
r1.metric(f"{years}-Year Survival Rate", f"{survival_rate:.1%}",
          delta="Above 80% threshold" if survival_rate >= 0.8 else "Below 80% threshold",
          delta_color=surv_color)
r2.metric("Median Terminal Value",  f"€{np.median(final_values)/1e6:.2f}M")
r3.metric("10th Pct Terminal",      f"€{np.percentile(final_values,10)/1e6:.2f}M")
r4.metric("90th Pct Terminal",      f"€{np.percentile(final_values,90)/1e6:.2f}M")
r5.metric("Paths Depleted",
          f"{depleted_count:,} / {len(paths):,}",
          delta=f"Avg year {np.mean(depletion_years):.0f}" if depletion_years else "None depleted",
          delta_color="inverse" if depleted_count > 0 else "normal")

# ════════════════════════════════════════════════════════════════════════════
# CHARTS
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-header">Charts</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

# ── Chart 1: Fan Chart ──────────────────────────────────────────────────────
with col1:
    fig, ax = plt.subplots(figsize=(7, 4.5), facecolor=C_BG)
    ax.set_facecolor(C_PANEL)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.tick_params(length=0)

    sample_idx = np.random.choice(len(paths), min(100, len(paths)), replace=False)
    for idx in sample_idx:
        ax.plot(years_axis, paths[idx] / 1e6, color=C_BLUE, alpha=0.04, lw=0.6)

    ax.fill_between(years_axis, pct_10/1e6, pct_90/1e6, color=C_BLUE, alpha=0.08)
    ax.fill_between(years_axis, pct_25/1e6, pct_75/1e6, color=C_BLUE, alpha=0.18)
    ax.plot(years_axis, pct_50/1e6,      color=C_GOLD, lw=2.2, zorder=5, label="Median")
    ax.plot(years_axis, pct_50_real/1e6, color=C_TEAL, lw=1.4, ls=(0,(4,3)), zorder=4, label="Median (real)")
    ax.axhline(portfolio/1e6, color=C_DIM, lw=0.7, ls=":", alpha=0.5)

    try:
        ax.text(years * 0.6, pct_90[-1]/1e6 * 1.02, "90th", color=C_BLUE, fontsize=7.5, alpha=0.8)
        ax.text(years * 0.6, pct_50[-1]/1e6 * 1.06, "Median", color=C_GOLD, fontsize=7.5)
        ax.text(years * 0.6, pct_10[-1]/1e6 * 0.78, "10th", color=C_BLUE, fontsize=7.5, alpha=0.8)
    except Exception:
        pass

    ax.set_title("Portfolio Outcomes", color=C_DARK, fontsize=11,
                 fontfamily="DejaVu Serif", pad=10, loc="left", fontweight="bold")
    ax.set_xlabel("Year")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:.1f}M"))
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Chart 2: Survival Curve ─────────────────────────────────────────────────
with col2:
    fig, ax = plt.subplots(figsize=(7, 4.5), facecolor=C_BG)
    ax.set_facecolor(C_PANEL)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.tick_params(length=0)

    survival_by_year = (paths > 0).mean(axis=0) * 100
    ax.fill_between(years_axis, survival_by_year, alpha=0.1, color=C_TEAL)
    ax.plot(years_axis, survival_by_year, color=C_TEAL, lw=2.2, zorder=5)

    for threshold, col in [(80, C_AMBER), (50, C_RED)]:
        ax.axhline(threshold, color=col, lw=0.9, ls="--", alpha=0.7)
        ax.text(years + 0.3, threshold, f"{threshold}%", color=col, fontsize=7.5, va="center")

    final_surv = survival_by_year[-1]
    ax.annotate(f"{final_surv:.0f}% survive\nyear {years}",
                xy=(years, final_surv),
                xytext=(years * 0.6, min(final_surv + 14, 100)),
                color=C_TEAL, fontsize=8.5,
                arrowprops=dict(arrowstyle="-", color=C_TEAL, lw=0.8, alpha=0.5))

    ax.set_title("Survival Rate Over Time", color=C_DARK, fontsize=11,
                 fontfamily="DejaVu Serif", pad=10, loc="left", fontweight="bold")
    ax.set_ylim(0, 108)
    ax.set_xlabel("Year")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

col3, col4 = st.columns(2)

# ── Chart 3: Terminal Value Distribution ────────────────────────────────────
with col3:
    fig, ax = plt.subplots(figsize=(7, 4.5), facecolor=C_BG)
    ax.set_facecolor(C_PANEL)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.tick_params(length=0)

    survived_vals = final_values[survived] / 1e6
    if len(survived_vals) > 0:
        n, bins, patches = ax.hist(survived_vals, bins=55, edgecolor="none", color=C_BLUE, alpha=0.75)
        norm_vals = (bins[:-1] - bins[:-1].min()) / (bins[:-1].max() - bins[:-1].min() + 1e-9)
        for patch, nv in zip(patches, norm_vals):
            patch.set_facecolor(plt.cm.Blues(0.3 + nv * 0.6))
            patch.set_alpha(0.85)

        med_val = np.median(survived_vals)
        ax.axvline(med_val, color=C_GOLD, lw=1.8, zorder=6)
        ax.axvline(portfolio/1e6, color=C_DIM, lw=1.0, ls=":", alpha=0.6)
        ylim_top = ax.get_ylim()[1]
        ax.text(med_val + 0.05, ylim_top * 0.88,
                f"Median\n€{med_val:.2f}M", color=C_GOLD, fontsize=8)

    if depleted_count > 0:
        ax.text(0.03, 0.95, f"[!]  {depleted_count:,} paths depleted ({depleted_count/len(paths):.1%})",
                transform=ax.transAxes, color=C_RED, fontsize=8)

    ax.set_title(f"Terminal Value (Year {years})", color=C_DARK, fontsize=11,
                 fontfamily="DejaVu Serif", pad=10, loc="left", fontweight="bold")
    ax.set_xlabel("Terminal Value")
    ax.set_ylabel("Simulations")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:.1f}M"))
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ── Chart 4: Withdrawal Sensitivity ─────────────────────────────────────────
with col4:
    with st.spinner("Calculating sensitivity..."):
        wds = np.arange(50_000, 200_001, 10_000)
        s_rates = []
        for wd in wds:
            p  = np.zeros((2000, years + 1)); p[:, 0] = portfolio
            cb = np.full(2000, float(portfolio))
            for yr in range(1, years + 1):
                pv = p[:, yr-1]
                sh = np.random.normal(mu_gross, sigma, 2000)
                gv = pv * (1 + sh)
                it = pv * portfolio_income_tax
                rw = wd * (1 + inflation) ** yr
                cn = rw + it + pv * ivafe
                gr = np.maximum(0, (gv - cb) / np.maximum(gv, 1))
                df = np.maximum(1 - gr * weighted_cgt, 0.5)
                to = cn / df
                sf = np.minimum(to / np.maximum(gv, 1), 1.0)
                cb = cb * (1 - sf)
                p[:, yr] = np.maximum(0, gv - to)
                cb = np.where(p[:, yr] <= 0, 0, cb)
            s_rates.append((p[:, -1] > 0).mean() * 100)

    s_rates    = np.array(s_rates)
    bar_colors = np.where(s_rates >= 80, C_TEAL, np.where(s_rates >= 50, C_AMBER, C_RED))

    fig, ax = plt.subplots(figsize=(7, 4.5), facecolor=C_BG)
    ax.set_facecolor(C_PANEL)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.tick_params(length=0)

    ax.bar(wds / 1000, s_rates, width=7.5, color=bar_colors, alpha=0.85,
           edgecolor=C_BG, linewidth=0.5)
    ax.axvline(withdrawal / 1000, color=C_GOLD, lw=1.6, ls="--", zorder=6)
    ax.text(withdrawal/1000 + 2, s_rates.max() * 0.96,
            f"Current\n€{withdrawal/1000:.0f}K",
            color=C_GOLD, fontsize=7.5)
    ax.axhline(80, color=C_AMBER, lw=0.8, ls=":", alpha=0.6)

    legend_elements = [
        Patch(facecolor=C_TEAL,  label=">=80%  safe",    alpha=0.85),
        Patch(facecolor=C_AMBER, label="50-80% caution",  alpha=0.85),
        Patch(facecolor=C_RED,   label="<50%  at risk",  alpha=0.85),
    ]
    ax.legend(handles=legend_elements, fontsize=7.5, frameon=False, labelcolor=C_DIM, loc="lower left")
    ax.set_title("Survival by Withdrawal Amount", color=C_DARK, fontsize=11,
                 fontfamily="DejaVu Serif", pad=10, loc="left", fontweight="bold")
    ax.set_xlabel("Annual Withdrawal (€K)")
    ax.set_ylim(0, 108)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

# ════════════════════════════════════════════════════════════════════════════
# YEAR-BY-YEAR DATA TABLE
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-header">Year-by-Year Summary</p>', unsafe_allow_html=True)

table_data = []
for yr in range(years + 1):
    nominal_wd = withdrawal * (1 + inflation) ** yr if yr > 0 else 0
    table_data.append({
        "Year":              yr,
        "Median Portfolio":  f"€{pct_50[yr]/1e6:.2f}M",
        "10th Percentile":   f"€{pct_10[yr]/1e6:.2f}M",
        "90th Percentile":   f"€{pct_90[yr]/1e6:.2f}M",
        "Median (Real €)":   f"€{pct_50_real[yr]/1e6:.2f}M",
        "Nominal Withdrawal":f"€{nominal_wd:,.0f}" if yr > 0 else "—",
        "% Paths Surviving": f"{(paths[:, yr] > 0).mean():.1%}",
    })

df = pd.DataFrame(table_data)
st.dataframe(df, use_container_width=True, hide_index=True,
             column_config={
                 "Year":               st.column_config.NumberColumn(width="small"),
                 "Median Portfolio":   st.column_config.TextColumn(width="medium"),
                 "10th Percentile":    st.column_config.TextColumn(width="medium"),
                 "90th Percentile":    st.column_config.TextColumn(width="medium"),
                 "Median (Real €)":    st.column_config.TextColumn(width="medium"),
                 "Nominal Withdrawal": st.column_config.TextColumn(width="medium"),
                 "% Paths Surviving":  st.column_config.TextColumn(width="medium"),
             })

# ════════════════════════════════════════════════════════════════════════════
# SCENARIO COMPARISON
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-header">Quick Scenario Comparison</p>', unsafe_allow_html=True)
st.caption("Compare how different withdrawal levels and return assumptions affect sustainability.")

scenarios = [
    ("Conservative returns (5%)",  0.050, withdrawal, sigma),
    ("Base case (current model)",  mu_gross, withdrawal, sigma),
    ("Optimistic returns (8.5%)",  0.085, withdrawal, sigma),
    ("Lower withdrawal (€75K)",    mu_gross, 75_000,   sigma),
    ("Higher withdrawal (€125K)",  mu_gross, 125_000,  sigma),
    ("Higher volatility (σ 22%)",  mu_gross, withdrawal, 0.22),
]

scen_rows = []
for name, g_ret, wd, vol in scenarios:
    wr = wd / portfolio
    # Estimate net return for scenario
    net_est = g_ret * (1 - weighted_cgt) - ivafe
    sust = "✅ Sustainable" if net_est > wr else "⚠️ Drawing down"
    scen_rows.append({
        "Scenario":        name,
        "Gross Return":    f"{g_ret:.1%}",
        "Withdrawal":      f"€{wd:,.0f}",
        "Withdrawal Rate": f"{wr:.2%}",
        "Est. Net Return": f"{net_est:.2%}",
        "Median Outlook":  sust,
    })

st.dataframe(pd.DataFrame(scen_rows), use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    f"<small style='color:{C_DIM}'>Model: Deferred CGT (Level 1 + 2) &nbsp;·&nbsp; "
    f"Gross μ: {mu_gross:.2%} &nbsp;·&nbsp; "
    f"Net μ: {mu_net:.2%} &nbsp;·&nbsp; "
    f"σ: {sigma:.2%} &nbsp;·&nbsp; "
    f"IVAFE: {ivafe:.1%} &nbsp;·&nbsp; "
    f"Tax regime: {tax_regime} &nbsp;·&nbsp; "
    f"<em>For illustrative purposes only. Not financial advice.</em></small>",
    unsafe_allow_html=True
)
