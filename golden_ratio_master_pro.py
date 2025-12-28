import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json

# ═══════════════════════════════════════════════════════════════════════════════
# 💎 GOLDEN RATIO MASTER PRO v2.0
# Advanced 5-Split Position Calculator with Full Symbol Support
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Golden Ratio Master Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────────
# CUSTOM STYLING - Dark Trading Terminal Aesthetic
# ─────────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;600&display=swap');
    
    :root {
        --bg-primary: #0a0e17;
        --bg-secondary: #111827;
        --bg-card: #1a1f2e;
        --accent-gold: #f59e0b;
        --accent-cyan: #06b6d4;
        --profit-green: #10b981;
        --loss-red: #ef4444;
        --text-primary: #f1f5f9;
        --text-muted: #64748b;
        --border-subtle: #1e293b;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    }
    
    .main-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, var(--accent-gold), var(--accent-cyan));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        letter-spacing: -1px;
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        color: var(--text-muted);
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: var(--accent-gold);
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.1);
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .metric-value.profit { color: var(--profit-green); }
    .metric-value.loss { color: var(--loss-red); }
    .metric-value.gold { color: var(--accent-gold); }
    .metric-value.cyan { color: var(--accent-cyan); }
    
    .position-row {
        background: var(--bg-card);
        border-left: 4px solid var(--accent-gold);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .scenario-positive {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.1), transparent);
        border-left: 3px solid var(--profit-green);
    }
    
    .scenario-negative {
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.1), transparent);
        border-left: 3px solid var(--loss-red);
    }
    
    .copy-box {
        background: #000;
        border: 1px solid var(--accent-cyan);
        border-radius: 8px;
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: var(--accent-cyan);
    }
    
    .warning-box {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid var(--accent-gold);
        border-radius: 8px;
        padding: 1rem;
        color: var(--accent-gold);
        font-family: 'Inter', sans-serif;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--bg-card);
        border-radius: 8px;
        color: var(--text-muted);
        font-family: 'Inter', sans-serif;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, var(--accent-gold), var(--accent-cyan));
        color: var(--bg-primary);
    }
    
    div[data-testid="stSidebar"] {
        background: var(--bg-secondary);
    }
    
    .fibonacci-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--accent-gold), #d97706);
        color: var(--bg-primary);
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────────
# SYMBOL CONFIGURATION - Comprehensive Market Data
# ─────────────────────────────────────────────────────────────────────────────────
SYMBOL_CONFIG = {
    # Major Forex Pairs
    "EURUSD": {"pip_value": 10.0, "pip_mult": 10000, "digits": 5, "category": "Forex Major", "base_currency": "EUR"},
    "GBPUSD": {"pip_value": 10.0, "pip_mult": 10000, "digits": 5, "category": "Forex Major", "base_currency": "GBP"},
    "USDCHF": {"pip_value": 10.0, "pip_mult": 10000, "digits": 5, "category": "Forex Major", "base_currency": "USD"},
    "USDJPY": {"pip_value": 6.70, "pip_mult": 100, "digits": 3, "category": "Forex Major", "base_currency": "USD"},
    "USDCAD": {"pip_value": 7.15, "pip_mult": 10000, "digits": 5, "category": "Forex Major", "base_currency": "USD"},
    "AUDUSD": {"pip_value": 10.0, "pip_mult": 10000, "digits": 5, "category": "Forex Major", "base_currency": "AUD"},
    "NZDUSD": {"pip_value": 10.0, "pip_mult": 10000, "digits": 5, "category": "Forex Major", "base_currency": "NZD"},
    
    # Forex Crosses
    "EURGBP": {"pip_value": 12.50, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "EUR"},
    "EURJPY": {"pip_value": 6.70, "pip_mult": 100, "digits": 3, "category": "Forex Cross", "base_currency": "EUR"},
    "GBPJPY": {"pip_value": 6.70, "pip_mult": 100, "digits": 3, "category": "Forex Cross", "base_currency": "GBP"},
    "GBPAUD": {"pip_value": 6.50, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "GBP"},
    "EURAUD": {"pip_value": 6.50, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "EUR"},
    "EURCHF": {"pip_value": 10.0, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "EUR"},
    "GBPCHF": {"pip_value": 10.0, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "GBP"},
    "AUDCAD": {"pip_value": 7.15, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "AUD"},
    "AUDNZD": {"pip_value": 5.80, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "AUD"},
    "NZDCAD": {"pip_value": 7.15, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "NZD"},
    "CADJPY": {"pip_value": 6.70, "pip_mult": 100, "digits": 3, "category": "Forex Cross", "base_currency": "CAD"},
    "AUDJPY": {"pip_value": 6.70, "pip_mult": 100, "digits": 3, "category": "Forex Cross", "base_currency": "AUD"},
    "NZDJPY": {"pip_value": 6.70, "pip_mult": 100, "digits": 3, "category": "Forex Cross", "base_currency": "NZD"},
    "CHFJPY": {"pip_value": 6.70, "pip_mult": 100, "digits": 3, "category": "Forex Cross", "base_currency": "CHF"},
    "CADCHF": {"pip_value": 10.0, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "CAD"},
    "AUDCHF": {"pip_value": 10.0, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "AUD"},
    "NZDCHF": {"pip_value": 10.0, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "NZD"},
    "EURNZD": {"pip_value": 5.80, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "EUR"},
    "GBPNZD": {"pip_value": 5.80, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "GBP"},
    "EURCAD": {"pip_value": 7.15, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "EUR"},
    "GBPCAD": {"pip_value": 7.15, "pip_mult": 10000, "digits": 5, "category": "Forex Cross", "base_currency": "GBP"},
    
    # Commodities
    "XAUUSD": {"pip_value": 10.0, "pip_mult": 10, "digits": 2, "category": "Commodity", "base_currency": "XAU"},
    "XAGUSD": {"pip_value": 50.0, "pip_mult": 100, "digits": 3, "category": "Commodity", "base_currency": "XAG"},
    "XTIUSD": {"pip_value": 10.0, "pip_mult": 100, "digits": 2, "category": "Commodity", "base_currency": "OIL"},
    
    # Index CFDs
    "US100": {"pip_value": 1.0, "pip_mult": 1, "digits": 1, "category": "Index CFD", "base_currency": "NQ", "type": "cfd"},
    "US500": {"pip_value": 1.0, "pip_mult": 1, "digits": 1, "category": "Index CFD", "base_currency": "SPX", "type": "cfd"},
    "US30": {"pip_value": 1.0, "pip_mult": 1, "digits": 1, "category": "Index CFD", "base_currency": "DJI", "type": "cfd"},
    "GER40": {"pip_value": 1.0, "pip_mult": 1, "digits": 1, "category": "Index CFD", "base_currency": "DAX", "type": "cfd"},
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FUTURES - Tick Size & Tick Value Based
    # point_value = tick_value / tick_size (value per 1.0 point move per contract)
    # ═══════════════════════════════════════════════════════════════════════════
    
    # E-mini & Micro Nasdaq
    "NQ": {"tick_size": 0.25, "tick_value": 5.00, "point_value": 20.0, "digits": 2, "category": "Futures", "base_currency": "NQ", "type": "futures"},
    "MNQ": {"tick_size": 0.25, "tick_value": 0.50, "point_value": 2.0, "digits": 2, "category": "Futures", "base_currency": "MNQ", "type": "futures"},
    
    # E-mini & Micro S&P 500
    "ES": {"tick_size": 0.25, "tick_value": 12.50, "point_value": 50.0, "digits": 2, "category": "Futures", "base_currency": "ES", "type": "futures"},
    "MES": {"tick_size": 0.25, "tick_value": 1.25, "point_value": 5.0, "digits": 2, "category": "Futures", "base_currency": "MES", "type": "futures"},
    
    # E-mini & Micro Dow
    "YM": {"tick_size": 1.0, "tick_value": 5.00, "point_value": 5.0, "digits": 0, "category": "Futures", "base_currency": "YM", "type": "futures"},
    "MYM": {"tick_size": 1.0, "tick_value": 0.50, "point_value": 0.5, "digits": 0, "category": "Futures", "base_currency": "MYM", "type": "futures"},
    
    # E-mini & Micro Russell 2000
    "RTY": {"tick_size": 0.10, "tick_value": 5.00, "point_value": 50.0, "digits": 2, "category": "Futures", "base_currency": "RTY", "type": "futures"},
    "M2K": {"tick_size": 0.10, "tick_value": 0.50, "point_value": 5.0, "digits": 2, "category": "Futures", "base_currency": "M2K", "type": "futures"},
    
    # Gold & Micro Gold Futures
    "GC": {"tick_size": 0.10, "tick_value": 10.00, "point_value": 100.0, "digits": 2, "category": "Futures", "base_currency": "GC", "type": "futures"},
    "MGC": {"tick_size": 0.10, "tick_value": 1.00, "point_value": 10.0, "digits": 2, "category": "Futures", "base_currency": "MGC", "type": "futures"},
    
    # Crude Oil & Micro Crude
    "CL": {"tick_size": 0.01, "tick_value": 10.00, "point_value": 1000.0, "digits": 2, "category": "Futures", "base_currency": "CL", "type": "futures"},
    "MCL": {"tick_size": 0.01, "tick_value": 1.00, "point_value": 100.0, "digits": 2, "category": "Futures", "base_currency": "MCL", "type": "futures"},
    
    # Euro FX Futures
    "6E": {"tick_size": 0.00005, "tick_value": 6.25, "point_value": 125000.0, "digits": 5, "category": "Futures", "base_currency": "6E", "type": "futures"},
    "M6E": {"tick_size": 0.0001, "tick_value": 1.25, "point_value": 12500.0, "digits": 5, "category": "Futures", "base_currency": "M6E", "type": "futures"},
    
    # Crypto
    "BTCUSD": {"pip_value": 1.0, "pip_mult": 1, "digits": 1, "category": "Crypto", "base_currency": "BTC", "type": "cfd"},
    "ETHUSD": {"pip_value": 1.0, "pip_mult": 10, "digits": 2, "category": "Crypto", "base_currency": "ETH", "type": "cfd"},
}

# Fibonacci Constants
GOLDEN_DECAY = [1.0, 0.618, 0.382, 0.236, 0.146]
FIBONACCI_WEIGHTS = [13, 8, 5, 3, 2]  # Sum = 31
WEIGHT_SUM = sum(FIBONACCI_WEIGHTS)

# ─────────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────────

def get_symbol_config(symbol: str) -> dict:
    """Get configuration for a symbol with fallback defaults."""
    return SYMBOL_CONFIG.get(symbol, {
        "pip_value": 10.0,
        "pip_mult": 10000,
        "digits": 5,
        "category": "Unknown",
        "base_currency": "???",
        "type": "forex"
    })


def validate_futures_minimum(df: pd.DataFrame, config: dict, account: float, risk_pct: float, sl_dist_max: float) -> dict:
    """
    Validate that all futures positions meet minimum 1 contract requirement.
    Returns dict with 'valid', 'message', and 'min_risk_pct' needed.
    """
    if config.get("type") != "futures":
        return {"valid": True, "message": "", "min_risk_pct": 0}
    
    point_value = config["point_value"]
    
    # Check if any position is below 1 contract
    size_col = 'Contracts' if 'Contracts' in df.columns else 'Lots'
    min_contracts = df[size_col].min()
    
    if min_contracts < 1:
        # Calculate minimum risk needed for smallest position (P5) to have 1 contract
        # P5 has weight 2/31 and decay 0.146
        p5_weight = FIBONACCI_WEIGHTS[4] / WEIGHT_SUM  # 2/31
        p5_decay = GOLDEN_DECAY[4]  # 0.146
        p5_sl_dist = sl_dist_max * p5_decay
        
        # For 1 contract: risk_needed = 1 * points * point_value
        p5_risk_needed = 1 * p5_sl_dist * point_value
        
        # Total risk needed = p5_risk / p5_weight
        total_risk_needed = p5_risk_needed / p5_weight
        
        # Convert to percentage
        min_risk_pct = (total_risk_needed / account) * 100
        
        return {
            "valid": False,
            "message": f"⚠️ 5-Split nicht möglich! Minimum 1 Kontrakt pro Position erforderlich.",
            "min_risk_pct": min_risk_pct,
            "min_risk_usd": total_risk_needed,
            "current_min_contracts": min_contracts
        }
    
    return {"valid": True, "message": "", "min_risk_pct": 0}


def calculate_futures_min_system(entry: float, sl_max: float, tp: float, symbol: str, multiplier: int = 1) -> pd.DataFrame:
    """
    Calculate futures positions with exactly 'multiplier' contracts per position.
    Returns detailed DataFrame with ticks, points, prices, and amounts.
    """
    config = get_symbol_config(symbol)
    
    tp_dist = abs(entry - tp)
    sl_dist_max = abs(entry - sl_max)
    is_short = entry > tp
    
    tick_size = config["tick_size"]
    tick_value = config["tick_value"]
    point_value = config["point_value"]
    
    data = []
    for i in range(5):
        contracts = multiplier  # Same for all positions in min system
        
        # SL distance with Golden Ratio decay
        pos_sl_dist = sl_dist_max * GOLDEN_DECAY[i]
        
        # Calculate SL price
        if is_short:
            pos_sl_price = entry + pos_sl_dist
        else:
            pos_sl_price = entry - pos_sl_dist
        
        # Calculate ticks and points
        sl_points = pos_sl_dist
        sl_ticks = pos_sl_dist / tick_size
        tp_points = tp_dist
        tp_ticks = tp_dist / tick_size
        
        # Calculate risk and profit in USD
        risk_usd = contracts * sl_points * point_value
        profit_usd = contracts * tp_points * point_value
        
        # RR ratio
        rr = tp_dist / pos_sl_dist if pos_sl_dist > 0 else 0
        
        data.append({
            "Position": f"P{i+1}",
            "Contracts": contracts,
            "Decay": f"{GOLDEN_DECAY[i]*100:.1f}%",
            "SL_Price": pos_sl_price,
            "SL_Points": sl_points,
            "SL_Ticks": sl_ticks,
            "TP_Price": tp,
            "TP_Points": tp_points,
            "TP_Ticks": tp_ticks,
            "Risk_USD": risk_usd,
            "Profit_USD": profit_usd,
            "RR": rr,
            "Unit": "Kontrakte"
        })
    
    return pd.DataFrame(data)


def validate_inputs(entry: float, sl: float, tp: float) -> tuple[bool, str]:
    """Validate trading inputs and return (is_valid, error_message)."""
    if entry == sl:
        return False, "⚠️ Entry und SL dürfen nicht identisch sein!"
    if entry == tp:
        return False, "⚠️ Entry und TP dürfen nicht identisch sein!"
    
    is_short = entry > tp
    if is_short and sl < entry:
        return False, "⚠️ Bei SHORT muss SL über Entry liegen!"
    if not is_short and sl > entry:
        return False, "⚠️ Bei LONG muss SL unter Entry liegen!"
    
    return True, ""


def calculate_positions(account: float, risk_pct: float, entry: float, sl_max: float, tp: float, symbol: str) -> pd.DataFrame:
    """Calculate all 5 positions with Golden Ratio decay."""
    config = get_symbol_config(symbol)
    total_risk = account * (risk_pct / 100)
    
    tp_dist = abs(entry - tp)
    sl_dist_max = abs(entry - sl_max)
    is_short = entry > tp
    
    # Determine calculation method based on instrument type
    is_futures = config.get("type") == "futures"
    
    data = []
    for i in range(5):
        # Risk allocation based on Fibonacci weights
        pos_risk = (FIBONACCI_WEIGHTS[i] / WEIGHT_SUM) * total_risk
        
        # SL distance with Golden Ratio decay
        pos_sl_dist = sl_dist_max * GOLDEN_DECAY[i]
        
        # Calculate SL price
        if is_short:
            pos_sl_price = entry + pos_sl_dist
        else:
            pos_sl_price = entry - pos_sl_dist
        
        # Calculate position size based on instrument type
        if is_futures:
            # Futures: Contracts = Risk / (Points * Point Value)
            point_value = config["point_value"]
            points = pos_sl_dist
            pos_size = pos_risk / (points * point_value) if points > 0 else 0
            unit_label = "Kontrakte"
        else:
            # Forex/CFD: Lots = Risk / (Pips * Pip Value / 10)
            pip_value = config["pip_value"]
            pip_mult = config["pip_mult"]
            pips = pos_sl_dist * pip_mult
            pos_size = pos_risk / (pips * (pip_value / 10)) if pips > 0 else 0
            points = pips  # For display consistency
            unit_label = "Lots"
        
        # Calculate RR and potential profit
        rr = tp_dist / pos_sl_dist if pos_sl_dist > 0 else 0
        profit = pos_risk * rr
        
        data.append({
            "Position": f"P{i+1}",
            "Weight": f"{FIBONACCI_WEIGHTS[i]}/{WEIGHT_SUM}",
            "Decay": f"{GOLDEN_DECAY[i]*100:.1f}%",
            "SL_Price": pos_sl_price,
            "SL_Pips": points,
            "Risk_USD": pos_risk,
            "Lots": pos_size,
            "RR": rr,
            "Profit_USD": profit,
            "Unit": unit_label
        })
    
    return pd.DataFrame(data)


def calculate_single_entry(account: float, risk_pct: float, entry: float, sl: float, tp: float, symbol: str) -> dict:
    """Calculate single entry position for comparison."""
    config = get_symbol_config(symbol)
    total_risk = account * (risk_pct / 100)
    
    sl_dist = abs(entry - sl)
    tp_dist = abs(entry - tp)
    
    is_futures = config.get("type") == "futures"
    
    if is_futures:
        # Futures: Contracts = Risk / (Points * Point Value)
        point_value = config["point_value"]
        points = sl_dist
        size = total_risk / (points * point_value) if points > 0 else 0
        unit_label = "Kontrakte"
    else:
        # Forex/CFD
        pips = sl_dist * config["pip_mult"]
        size = total_risk / (pips * (config["pip_value"] / 10)) if pips > 0 else 0
        points = pips
        unit_label = "Lots"
    
    rr = tp_dist / sl_dist if sl_dist > 0 else 0
    profit = total_risk * rr
    
    return {
        "size": size,
        "risk": total_risk,
        "rr": rr,
        "profit": profit,
        "sl_points": points,
        "unit": unit_label
    }


def calculate_scenarios(df: pd.DataFrame, total_risk: float) -> list[dict]:
    """
    Calculate all possible outcome scenarios.
    
    Logic: All positions share same Entry and TP. SLs vary from tight (P5) to wide (P1).
    When price moves against you, tighter SLs get hit first: P5 → P4 → P3 → P2 → P1
    
    Scenarios:
    - 0 SL hit = All 5 reach TP = Max Profit
    - 1 SL hit = P5 stopped out, P1-P4 reach TP
    - 2 SL hit = P5+P4 stopped out, P1-P3 reach TP
    - ...
    - 5 SL hit = All stopped out = Max Loss
    """
    scenarios = []
    
    # Reverse order: P5 (index 4) gets hit first, P1 (index 0) gets hit last
    for sl_hits in range(6):
        if sl_hits == 0:
            # Best case: All positions reach TP
            net = df['Profit_USD'].sum()
            desc = "Alle im TP ✨"
            status = "profit"
        elif sl_hits == 5:
            # Worst case: All positions stopped out
            net = -total_risk
            desc = "Alle SL getroffen"
            status = "loss"
        else:
            # Partial: Some SLs hit (from P5 backwards), rest reach TP
            # SLs hit: last 'sl_hits' positions (P5, P4, P3...)
            # TPs reached: first (5 - sl_hits) positions (P1, P2, P3...)
            
            positions_stopped = df.iloc[5-sl_hits:]['Risk_USD'].sum()  # P5, P4, etc. stopped
            positions_won = df.iloc[:5-sl_hits]['Profit_USD'].sum()     # P1, P2, etc. won
            
            net = positions_won - positions_stopped
            desc = f"{sl_hits}x SL getroffen"
            status = "profit" if net > 0 else "loss" if net < 0 else "breakeven"
        
        scenarios.append({
            "sl_hits": sl_hits,
            "description": desc,
            "net": net,
            "status": status
        })
    
    return scenarios


def find_breakeven_point(scenarios: list[dict]) -> int:
    """Find maximum SL hits that still allow break-even or profit."""
    # Start from most SL hits and find where we're still >= 0
    for s in reversed(scenarios):
        if s["net"] >= 0:
            return s["sl_hits"]
    return 0  # Only profitable if no SLs hit


def generate_mt5_orders(df: pd.DataFrame, entry: float, tp: float, symbol: str) -> str:
    """Generate copy-paste ready order strings."""
    config = get_symbol_config(symbol)
    digits = config["digits"]
    unit_label = df.iloc[0].get('Unit', 'Lots') if 'Unit' in df.columns else 'Lots'
    size_col = 'Contracts' if 'Contracts' in df.columns else 'Lots'
    
    lines = [f"// {symbol} - Golden Ratio 5-Split Orders", f"// Entry: {entry:.{digits}f} | TP: {tp:.{digits}f}", ""]
    
    for _, row in df.iterrows():
        size_val = row[size_col]
        lines.append(f"{row['Position']}: {size_val:.0f} {unit_label} | SL: {row['SL_Price']:.{digits}f} | Risk: ${row['Risk_USD']:.2f}")
    
    lines.append("")
    lines.append(f"// Total {unit_label}: {df[size_col].sum():.0f}")
    lines.append(f"// Total Risk: ${df['Risk_USD'].sum():.2f}")
    
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────────
# VISUALIZATION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────────

def create_sl_ladder_chart(entry: float, sl_max: float, tp: float, df: pd.DataFrame, symbol: str):
    """Create visual SL ladder chart with Plotly."""
    config = get_symbol_config(symbol)
    is_short = entry > tp
    
    fig = go.Figure()
    
    # TP Zone
    fig.add_hline(y=tp, line_color="#10b981", line_width=3, line_dash="solid",
                  annotation_text=f"TP: {tp:.{config['digits']}f}", annotation_position="right")
    
    # Entry Line
    fig.add_hline(y=entry, line_color="#f59e0b", line_width=2, line_dash="dash",
                  annotation_text=f"Entry: {entry:.{config['digits']}f}", annotation_position="right")
    
    # SL Levels for each position
    colors = ["#ef4444", "#f97316", "#eab308", "#84cc16", "#22c55e"]
    for i, row in df.iterrows():
        fig.add_hline(y=row['SL_Price'], line_color=colors[i], line_width=1.5, line_dash="dot",
                      annotation_text=f"SL {row['Position']}: {row['SL_Price']:.{config['digits']}f}",
                      annotation_position="left")
    
    # Styling
    y_min = min(tp, sl_max) - abs(entry - tp) * 0.1
    y_max = max(tp, sl_max) + abs(entry - tp) * 0.1
    
    fig.update_layout(
        title=dict(text=f"📊 SL-Leiter Visualisierung ({symbol})", font=dict(color="#f1f5f9")),
        yaxis=dict(
            title="Preis",
            range=[y_min, y_max],
            gridcolor="#1e293b",
            color="#f1f5f9"
        ),
        xaxis=dict(visible=False),
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,31,46,0.8)",
        font=dict(family="JetBrains Mono", color="#f1f5f9"),
        margin=dict(l=20, r=150, t=50, b=20)
    )
    
    return fig


def create_risk_distribution_chart(df: pd.DataFrame):
    """Create pie chart showing risk distribution."""
    fig = go.Figure(data=[go.Pie(
        labels=df['Position'],
        values=df['Risk_USD'],
        hole=0.5,
        marker_colors=['#f59e0b', '#d97706', '#b45309', '#92400e', '#78350f'],
        textinfo='label+percent',
        textfont=dict(family="JetBrains Mono", size=12),
        hovertemplate="<b>%{label}</b><br>Risk: $%{value:.2f}<br>Anteil: %{percent}<extra></extra>"
    )])
    
    fig.update_layout(
        title=dict(text="💰 Risiko-Verteilung", font=dict(color="#f1f5f9")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono", color="#f1f5f9"),
        height=300,
        showlegend=False,
        annotations=[dict(text="Risk", x=0.5, y=0.5, font_size=16, showarrow=False, font_color="#f59e0b")]
    )
    
    return fig


def create_scenario_chart(scenarios: list[dict]):
    """Create bar chart for scenario analysis."""
    fig = go.Figure()
    
    colors = ["#10b981" if s['net'] > 0 else "#ef4444" if s['net'] < 0 else "#64748b" for s in scenarios]
    
    fig.add_trace(go.Bar(
        x=[s['description'] for s in scenarios],
        y=[s['net'] for s in scenarios],
        marker_color=colors,
        text=[f"${s['net']:+.2f}" for s in scenarios],
        textposition='outside',
        textfont=dict(family="JetBrains Mono", size=11)
    ))
    
    fig.add_hline(y=0, line_color="#64748b", line_width=1)
    
    fig.update_layout(
        title=dict(text="📈 Szenario-Analyse (0 SL = Best Case → 5 SL = Worst Case)", font=dict(color="#f1f5f9")),
        yaxis=dict(title="Netto P/L ($)", gridcolor="#1e293b", color="#f1f5f9", zerolinecolor="#64748b"),
        xaxis=dict(color="#f1f5f9", title="Anzahl SLs getroffen"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(26,31,46,0.8)",
        font=dict(family="JetBrains Mono", color="#f1f5f9"),
        height=350,
        margin=dict(l=20, r=20, t=50, b=80)
    )
    
    return fig


# ─────────────────────────────────────────────────────────────────────────────────
# MAIN APPLICATION
# ─────────────────────────────────────────────────────────────────────────────────

# Header
st.markdown('<h1 class="main-header">💎 GOLDEN RATIO MASTER PRO</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced 5-Split Position Calculator | Fibonacci-Based Risk Management</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR - Input Configuration
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ Trade Setup")
    
    # Account Settings
    st.markdown("**Konto**")
    account = st.number_input("Kontostand ($)", value=10000.0, min_value=100.0, step=100.0, format="%.2f")
    risk_pct = st.number_input("Risiko (%)", value=1.00, min_value=0.01, max_value=10.00, step=0.01, format="%.2f")
    
    st.divider()
    
    # Symbol Selection with Categories
    st.markdown("**Symbol**")
    categories = sorted(set(c["category"] for c in SYMBOL_CONFIG.values()))
    selected_category = st.selectbox("Kategorie", categories, index=0)
    
    filtered_symbols = [s for s, c in SYMBOL_CONFIG.items() if c["category"] == selected_category]
    symbol = st.selectbox("Instrument", filtered_symbols, index=0)
    
    config = get_symbol_config(symbol)
    
    # Show relevant info based on instrument type
    if config.get("type") == "futures":
        st.caption(f"📊 Tick: {config['tick_size']} = ${config['tick_value']} | Punkt = ${config['point_value']}")
        
        st.divider()
        
        # Futures-specific controls
        st.markdown("**Futures Modus**")
        futures_mode = st.radio(
            "Position Sizing",
            ["Kleinst-System (1 Kontrakt)", "Risk-basiert"],
            index=0,
            help="Kleinst-System: Immer 1 Kontrakt pro Position. Risk-basiert: Berechnet aus Risiko %"
        )
        
        if futures_mode == "Kleinst-System (1 Kontrakt)":
            multiplier = st.number_input("Multiplikator", value=1, min_value=1, max_value=100, step=1)
            st.caption(f"→ {multiplier * 5} Kontrakte total ({multiplier} pro Position)")
        else:
            multiplier = 1
    else:
        futures_mode = "Risk-basiert"
        multiplier = 1
        st.caption(f"📊 Pip-Wert: ${config['pip_value']} | Mult: {config['pip_mult']}")
    
    st.divider()
    
    # Price Levels
    st.markdown("**Preis-Level**")
    digits = config["digits"]
    
    # Default values based on symbol type
    if config.get("type") == "futures":
        if symbol in ["NQ", "MNQ"]:
            default_entry, default_sl, default_tp = 21500.00, 21550.00, 21350.00
        elif symbol in ["ES", "MES"]:
            default_entry, default_sl, default_tp = 6000.00, 6020.00, 5950.00
        elif symbol in ["YM", "MYM"]:
            default_entry, default_sl, default_tp = 43000.0, 43100.0, 42800.0
        elif symbol in ["GC", "MGC"]:
            default_entry, default_sl, default_tp = 2650.00, 2660.00, 2620.00
        elif symbol in ["CL", "MCL"]:
            default_entry, default_sl, default_tp = 72.50, 73.00, 71.00
        else:
            default_entry, default_sl, default_tp = 100.00, 101.00, 98.00
    elif config["category"] == "Index CFD":
        default_entry, default_sl, default_tp = 21500.0, 21550.0, 21350.0
    elif symbol == "XAUUSD":
        default_entry, default_sl, default_tp = 2650.00, 2658.00, 2620.00
    else:
        default_entry, default_sl, default_tp = 1.08500, 1.08600, 1.08000
    
    entry = st.number_input("Entry", value=default_entry, format=f"%.{digits}f", step=10**(-digits))
    sl_max = st.number_input("Max SL (P1)", value=default_sl, format=f"%.{digits}f", step=10**(-digits))
    tp = st.number_input("Take Profit", value=default_tp, format=f"%.{digits}f", step=10**(-digits))
    
    # Trade Direction Indicator
    is_short = entry > tp
    direction_color = "#ef4444" if is_short else "#10b981"
    direction_text = "🔻 SHORT" if is_short else "🔺 LONG"
    st.markdown(f'<div style="text-align:center; padding:0.5rem; background:{direction_color}22; border-radius:8px; color:{direction_color}; font-weight:bold;">{direction_text}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

# Validation
is_valid, error_msg = validate_inputs(entry, sl_max, tp)

if not is_valid:
    st.error(error_msg)
    st.stop()

# Calculate everything
is_futures_min_mode = config.get("type") == "futures" and futures_mode == "Kleinst-System (1 Kontrakt)"

if is_futures_min_mode:
    # Use minimum system with multiplier
    df_positions = calculate_futures_min_system(entry, sl_max, tp, symbol, multiplier)
    # Single entry for comparison = 1 contract * multiplier
    single = {
        "size": multiplier,
        "risk": multiplier * abs(entry - sl_max) * config["point_value"],
        "profit": multiplier * abs(entry - tp) * config["point_value"],
        "rr": abs(entry - tp) / abs(entry - sl_max) if abs(entry - sl_max) > 0 else 0,
        "sl_points": abs(entry - sl_max),
        "unit": "Kontrakte"
    }
    futures_validation = {"valid": True}  # Always valid in min mode
else:
    df_positions = calculate_positions(account, risk_pct, entry, sl_max, tp, symbol)
    single = calculate_single_entry(account, risk_pct, entry, sl_max, tp, symbol)
    # Validate futures minimum contract requirement
    sl_dist_max = abs(entry - sl_max)
    futures_validation = validate_futures_minimum(df_positions, config, account, risk_pct, sl_dist_max)

scenarios = calculate_scenarios(df_positions, df_positions['Risk_USD'].sum())
breakeven_point = find_breakeven_point(scenarios)

# ─────────────────────────────────────────────────────────────────────────────────
# FUTURES WARNING - Show if 5-Split not possible
# ─────────────────────────────────────────────────────────────────────────────────
if not futures_validation["valid"]:
    st.markdown("---")
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.05)); 
                border: 2px solid #ef4444; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;">
        <h3 style="color: #ef4444; margin: 0 0 1rem 0; font-family: 'JetBrains Mono';">
            ⚠️ 5-Split System NICHT anwendbar!
        </h3>
        <p style="color: #f1f5f9; margin: 0.5rem 0; font-family: 'Inter';">
            Bei Futures ist <strong>mindestens 1 Kontrakt</strong> pro Position erforderlich.
        </p>
        <p style="color: #94a3b8; margin: 0.5rem 0; font-family: 'Inter';">
            Aktuelle kleinste Position: <span style="color: #ef4444; font-weight: bold;">{futures_validation['current_min_contracts']:.2f} Kontrakte</span>
        </p>
        <div style="background: #1a1f2e; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
            <p style="color: #f59e0b; margin: 0; font-family: 'JetBrains Mono';">
                💡 Mindest-Risiko für 5-Split: <strong>${futures_validation['min_risk_usd']:.2f}</strong> 
                ({futures_validation['min_risk_pct']:.2f}% von ${account:.0f})
            </p>
        </div>
        <p style="color: #64748b; margin: 1rem 0 0 0; font-size: 0.85rem; font-family: 'Inter';">
            Alternative: Nutze den <strong>Single Entry</strong> oder erhöhe dein Risiko.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────────
# TOP METRICS - Comparison Dashboard
# ─────────────────────────────────────────────────────────────────────────────────
st.markdown("---")

# Show mode indicator for futures
if is_futures_min_mode:
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, rgba(245, 158, 11, 0.2), transparent); 
                border-left: 4px solid #f59e0b; padding: 0.75rem 1rem; margin-bottom: 1rem; border-radius: 0 8px 8px 0;">
        <span style="color: #f59e0b; font-family: 'JetBrains Mono'; font-weight: 600;">
            🎯 KLEINST-SYSTEM MODUS | {multiplier}x Multiplikator | {multiplier * 5} Kontrakte Total
        </span>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4) if is_futures_min_mode else (st.columns(3) + [None])[:4]

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Single Entry Profit</div>
        <div class="metric-value">${:.2f}</div>
    </div>
    """.format(single['profit']), unsafe_allow_html=True)

with col2:
    if futures_validation["valid"]:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value gold">${:.2f}</div>
            <div class="metric-label">5-Split Max Profit</div>
        </div>
        """.format(df_positions['Profit_USD'].sum()), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card" style="border-color: #ef4444;">
            <div class="metric-value" style="color: #ef4444;">N/A</div>
            <div class="metric-label">5-Split nicht möglich</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    if futures_validation["valid"]:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value" style="color: #ef4444;">-${:.2f}</div>
            <div class="metric-label">5-Split Max Loss</div>
        </div>
        """.format(df_positions['Risk_USD'].sum()), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card" style="border-color: #ef4444;">
            <div class="metric-value" style="color: #ef4444;">—</div>
            <div class="metric-label">Split Advantage</div>
        </div>
        """, unsafe_allow_html=True)

if col4 and is_futures_min_mode:
    with col4:
        advantage = ((df_positions['Profit_USD'].sum() / single['profit']) - 1) * 100 if single['profit'] > 0 else 0
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value cyan">+{:.1f}%</div>
            <div class="metric-label">Split Advantage</div>
        </div>
        """.format(advantage), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────────
# TABS - Detailed Analysis
# ─────────────────────────────────────────────────────────────────────────────────
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Vergleich", "📈 Szenarien", "🎯 Positionen", "📋 Export"])

with tab1:
    col_a, col_b = st.columns(2)
    
    # Get unit label
    unit_label = df_positions.iloc[0]['Unit'] if 'Unit' in df_positions.columns else "Lots"
    points_label = "Punkte" if config.get("type") == "futures" else "Pips"
    
    with col_a:
        st.markdown("### 🛒 Single Entry")
        st.markdown(f"""
        | Metrik | Wert |
        |--------|------|
        | **{unit_label}** | {single['size']:.2f} |
        | **Risiko** | ${single['risk']:.2f} |
        | **SL {points_label}** | {single['sl_points']:.1f} |
        | **RR** | {single['rr']:.2f}x |
        | **Max Profit** | ${single['profit']:.2f} |
        """)
        
        st.info("⚡ Binäres Ergebnis: Entweder voller Gewinn oder voller Verlust")
    
    with col_b:
        st.markdown("### 🛡️ Golden Ratio 5-Split")
        
        # Get size column (Lots for forex, Contracts for futures)
        size_col = 'Contracts' if 'Contracts' in df_positions.columns else 'Lots'
        total_size = df_positions[size_col].sum()
        total_risk = df_positions['Risk_USD'].sum()
        
        st.markdown(f"""
        | Metrik | Wert |
        |--------|------|
        | **Total {unit_label}** | {total_size:.2f} |
        | **Total Risiko** | ${total_risk:.2f} |
        | **Avg RR** | {df_positions['RR'].mean():.2f}x |
        | **System RR** | {df_positions['Profit_USD'].sum() / total_risk:.2f}x |
        | **Max Profit** | ${df_positions['Profit_USD'].sum():.2f} |
        """)
        
        if breakeven_point > 0:
            st.success(f"✅ Profitabel auch bei bis zu {breakeven_point}x SL getroffen")
        else:
            st.info("ℹ️ Nur profitabel wenn alle Positionen TP erreichen")

with tab2:
    st.markdown("### 📉 Was passiert wenn...?")
    st.caption("Szenarien zeigen was passiert wenn X Positionen ausgestoppt werden (P5 zuerst, dann P4, P3...)")
    
    # Scenario Chart
    st.plotly_chart(create_scenario_chart(scenarios), use_container_width=True)
    
    # Detailed Scenario Table
    st.markdown("**Detaillierte Szenarien:**")
    for s in scenarios:
        color = "#10b981" if s['status'] == "profit" else "#ef4444" if s['status'] == "loss" else "#64748b"
        icon = "✅" if s['status'] == "profit" else "❌" if s['status'] == "loss" else "➖"
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; padding:0.5rem 1rem; margin:0.25rem 0; 
                    background:linear-gradient(90deg, {color}15, transparent); border-left:3px solid {color}; border-radius:0 8px 8px 0;">
            <span>{icon} {s['description']}</span>
            <span style="font-family:'JetBrains Mono'; color:{color}; font-weight:600;">${s['net']:+.2f}</span>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("### 🎯 Position Details")
    
    # Visual SL Ladder
    st.plotly_chart(create_sl_ladder_chart(entry, sl_max, tp, df_positions, symbol), use_container_width=True)
    
    col_p, col_r = st.columns([2, 1])
    
    with col_p:
        # Position Cards - different layout for futures min system
        for _, row in df_positions.iterrows():
            decay_pct = float(row['Decay'].replace('%', ''))
            bar_width = decay_pct
            
            # Check if this is futures min system (has Contracts and Ticks columns)
            if 'Contracts' in row and 'SL_Ticks' in row:
                # Futures Min System Layout
                st.markdown(f"""
                <div class="position-row">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <strong style="font-size:1.1rem; color:#f59e0b;">{row['Position']}</strong>
                            <span class="fibonacci-badge" style="margin-left:0.5rem;">{row['Decay']}</span>
                        </div>
                        <div style="text-align:right;">
                            <span style="color:#ef4444;">-${row['Risk_USD']:.2f}</span>
                            <span style="color:#64748b; margin:0 0.5rem;">→</span>
                            <span style="color:#10b981;">+${row['Profit_USD']:.2f}</span>
                        </div>
                    </div>
                    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:0.5rem; margin-top:0.75rem; font-size:0.8rem;">
                        <div style="background:#1e293b; padding:0.5rem; border-radius:6px; text-align:center;">
                            <div style="color:#64748b; font-size:0.7rem;">KONTRAKTE</div>
                            <div style="color:#f59e0b; font-weight:600;">{row['Contracts']}</div>
                        </div>
                        <div style="background:#1e293b; padding:0.5rem; border-radius:6px; text-align:center;">
                            <div style="color:#64748b; font-size:0.7rem;">SL PREIS</div>
                            <div style="color:#ef4444; font-weight:600;">{row['SL_Price']:.{digits}f}</div>
                        </div>
                        <div style="background:#1e293b; padding:0.5rem; border-radius:6px; text-align:center;">
                            <div style="color:#64748b; font-size:0.7rem;">SL PUNKTE</div>
                            <div style="color:#94a3b8; font-weight:600;">{row['SL_Points']:.2f}</div>
                        </div>
                        <div style="background:#1e293b; padding:0.5rem; border-radius:6px; text-align:center;">
                            <div style="color:#64748b; font-size:0.7rem;">SL TICKS</div>
                            <div style="color:#94a3b8; font-weight:600;">{row['SL_Ticks']:.0f}</div>
                        </div>
                    </div>
                    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:0.5rem; margin-top:0.25rem; font-size:0.8rem;">
                        <div style="background:#1e293b; padding:0.5rem; border-radius:6px; text-align:center;">
                            <div style="color:#64748b; font-size:0.7rem;">RR</div>
                            <div style="color:#06b6d4; font-weight:600;">{row['RR']:.1f}x</div>
                        </div>
                        <div style="background:#1e293b; padding:0.5rem; border-radius:6px; text-align:center;">
                            <div style="color:#64748b; font-size:0.7rem;">TP PREIS</div>
                            <div style="color:#10b981; font-weight:600;">{row['TP_Price']:.{digits}f}</div>
                        </div>
                        <div style="background:#1e293b; padding:0.5rem; border-radius:6px; text-align:center;">
                            <div style="color:#64748b; font-size:0.7rem;">TP PUNKTE</div>
                            <div style="color:#94a3b8; font-weight:600;">{row['TP_Points']:.2f}</div>
                        </div>
                        <div style="background:#1e293b; padding:0.5rem; border-radius:6px; text-align:center;">
                            <div style="color:#64748b; font-size:0.7rem;">TP TICKS</div>
                            <div style="color:#94a3b8; font-weight:600;">{row['TP_Ticks']:.0f}</div>
                        </div>
                    </div>
                    <div style="margin-top:0.5rem; background:#1e293b; border-radius:4px; height:4px;">
                        <div style="background:linear-gradient(90deg, #f59e0b, #06b6d4); width:{bar_width}%; height:100%; border-radius:4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Standard Forex/CFD Layout
                unit = row.get('Unit', 'Lots')
                weight = row.get('Weight', row['Decay'])
                size_val = row.get('Lots', row.get('Contracts', 0))
                
                st.markdown(f"""
                <div class="position-row">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <strong style="font-size:1.1rem; color:#f59e0b;">{row['Position']}</strong>
                            <span class="fibonacci-badge" style="margin-left:0.5rem;">{weight}</span>
                        </div>
                        <div style="text-align:right;">
                            <span style="color:#10b981;">+${row['Profit_USD']:.2f}</span>
                        </div>
                    </div>
                    <div style="display:flex; gap:2rem; margin-top:0.5rem; font-size:0.85rem; color:#94a3b8;">
                        <span>{unit}: {size_val:.2f}</span>
                        <span>SL: {row['SL_Price']:.{digits}f}</span>
                        <span>Risk: ${row['Risk_USD']:.2f}</span>
                        <span>RR: {row['RR']:.1f}x</span>
                    </div>
                    <div style="margin-top:0.5rem; background:#1e293b; border-radius:4px; height:4px;">
                        <div style="background:linear-gradient(90deg, #f59e0b, #06b6d4); width:{bar_width}%; height:100%; border-radius:4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col_r:
        st.plotly_chart(create_risk_distribution_chart(df_positions), use_container_width=True)

with tab4:
    st.markdown("### 📋 MT5 Order Export")
    
    mt5_orders = generate_mt5_orders(df_positions, entry, tp, symbol)
    
    st.markdown('<div class="copy-box">', unsafe_allow_html=True)
    st.code(mt5_orders, language="text")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # JSON Export
    st.markdown("### 💾 JSON Export")
    
    export_data = {
        "timestamp": datetime.now().isoformat(),
        "setup": {
            "account": account,
            "risk_pct": risk_pct,
            "symbol": symbol,
            "entry": entry,
            "sl_max": sl_max,
            "tp": tp,
            "direction": "SHORT" if is_short else "LONG"
        },
        "positions": df_positions.to_dict(orient="records"),
        "comparison": {
            "single_profit": single['profit'],
            "split_profit": df_positions['Profit_USD'].sum(),
            "advantage_pct": ((df_positions['Profit_USD'].sum() / single['profit']) - 1) * 100 if single['profit'] > 0 else 0
        },
        "breakeven_max_sl_hits": breakeven_point
    }
    
    st.download_button(
        label="⬇️ Download JSON",
        data=json.dumps(export_data, indent=2, default=str),
        file_name=f"golden_ratio_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json"
    )

# ─────────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#64748b; font-size:0.8rem; padding:1rem;">
    💎 Golden Ratio Master Pro v2.0 | Fibonacci-Based Position Management<br>
    <span style="color:#f59e0b;">φ = 1.618...</span> | The Golden Path to Risk Management
</div>
""", unsafe_allow_html=True)
