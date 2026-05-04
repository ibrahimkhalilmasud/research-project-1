"""
MR MIKE — Research Dashboard  v3.0
Enhanced: visual redesign + dropdown search + sort controls
Run with:  streamlit run research_dashboard.py
"""

import streamlit as st
import os, re, base64
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# ── config ───────────────────────────────────────────────────────
BASE         = Path(__file__).parent
REFRESH_SECS = 60

# File extensions that can be previewed inline (no download needed)
VIEWABLE_EXTS  = {".pdf", ".jpg", ".jpeg", ".png", ".avif"}
MAX_PREVIEW_MB = 50   # PDFs above this size fall back to download

st.set_page_config(
    page_title="Mr Mike — Research Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main { background: #07090F !important; }
.block-container { padding: 1.2rem 2rem 3rem 2rem; max-width: 1700px; }

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #07090F; }
::-webkit-scrollbar-thumb { background: #C9A84C; border-radius: 10px; }

/* ── HERO HEADER ── */
.dash-header {
  background: linear-gradient(135deg, #0A1628 0%, #0F2040 50%, #0A1628 100%);
  border-radius: 16px; padding: 22px 28px; margin-bottom: 20px;
  border: 1px solid rgba(201,168,76,.22);
  box-shadow: 0 8px 40px rgba(0,0,0,.5);
  display: flex; align-items: center; gap: 18px;
  position: relative; overflow: hidden;
}
.dash-header::before {
  content: ''; position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent 0%, #C9A84C 50%, transparent 100%);
}
.dash-header::after {
  content: ''; position: absolute;
  bottom: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(201,168,76,.3) 50%, transparent 100%);
}
.dash-icon { font-size: 2.4rem; }
.dash-title { font-size: 1.55rem; font-weight: 800; color: #FFFFFF; letter-spacing: -.4px; }
.dash-sub { font-size: .72rem; color: #9A7A3A; text-transform: uppercase; letter-spacing: 1.4px; margin-top: 3px; }
.dash-ts { margin-left: auto; text-align: right; }
.dash-ts-val { font-size: .75rem; color: #C9A84C; font-weight: 600; }
.dash-ts-lbl { font-size: .65rem; color: #444; text-transform: uppercase; letter-spacing: .8px; }

/* ── STAT CARDS ── */
.stat-box {
  background: linear-gradient(145deg, #0C1520 0%, #111E2E 100%);
  border-radius: 14px; padding: 18px 10px;
  text-align: center;
  border: 1px solid rgba(255,255,255,.06);
  border-top: 3px solid;
  box-shadow: 0 4px 20px rgba(0,0,0,.4);
  position: relative; overflow: hidden;
  transition: all .2s ease;
}
.stat-box:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(0,0,0,.55); }
.stat-box::after {
  content: ''; position: absolute;
  bottom: 0; left: 20%; right: 20%; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201,168,76,.25), transparent);
}
.stat-num { font-size: 2rem; font-weight: 800; line-height: 1; }
.stat-lbl { font-size: .62rem; color: #666; margin-top: 7px;
             font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }

/* ── CATEGORY HEADER ── */
.cat-header {
  padding: 12px 18px; border-radius: 10px; color: #FFF;
  font-weight: 700; font-size: .9rem;
  margin: 22px 0 10px 0;
  display: flex; align-items: center; gap: 10px;
  box-shadow: 0 4px 18px rgba(0,0,0,.35);
  position: relative; overflow: hidden;
}
.cat-header::before {
  content: ''; position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(90deg, rgba(0,0,0,.25) 0%, transparent 60%);
}
.cat-pill {
  margin-left: auto; background: rgba(255,255,255,.15);
  border-radius: 20px; padding: 2px 10px;
  font-size: .7rem; font-weight: 500; white-space: nowrap;
}

/* ── FILE CARD ── */
.file-card {
  background: linear-gradient(145deg, #0C1520 0%, #0F1A28 100%);
  border-radius: 12px; padding: 13px 16px; margin-bottom: 10px;
  border: 1px solid rgba(255,255,255,.055);
  border-left: 4px solid;
  box-shadow: 0 2px 14px rgba(0,0,0,.35);
  transition: all .2s ease;
  position: relative; overflow: hidden;
}
.file-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 26px rgba(201,168,76,.18);
  border-color: rgba(201,168,76,.28);
  background: linear-gradient(145deg, #0F1D2E 0%, #121F2E 100%);
}
.file-card::after {
  content: ''; position: absolute;
  bottom: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201,168,76,.08), transparent);
}
.file-title { font-weight: 600; font-size: .87rem; color: #DCE4F0; line-height: 1.45; }
.file-meta  { font-size: .69rem; color: #4A5568; margin-top: 5px; line-height: 1.7; }
.file-rec   { font-size: .72rem; color: #D4820A; font-weight: 600; margin-top: 4px; }

/* ── BADGES ── */
.badge {
  display: inline-block; padding: 2px 8px; border-radius: 20px;
  font-size: .6rem; font-weight: 700; margin-left: 5px; vertical-align: middle;
}
.badge-low      { background: rgba(30,127,78,.18);  color: #52C496; border: 1px solid rgba(30,127,78,.4); }
.badge-moderate { background: rgba(212,98,10,.18);  color: #E88830; border: 1px solid rgba(212,98,10,.4); }
.badge-high     { background: rgba(176,48,48,.18);  color: #E86060; border: 1px solid rgba(176,48,48,.4); }
.badge-type     { background: rgba(100,120,200,.15); color: #8898D8; border: 1px solid rgba(100,120,200,.3); }

/* ── SEARCH RESULT BANNER ── */
.srb {
  background: linear-gradient(135deg, rgba(201,168,76,.1) 0%, rgba(201,168,76,.04) 100%);
  border: 1px solid rgba(201,168,76,.28);
  border-radius: 10px; padding: 10px 16px; margin-bottom: 16px;
  font-size: .81rem; color: #C9A84C; font-weight: 500;
  display: flex; align-items: center; gap: 8px;
}

/* ── QUICK-OPEN CARD (sidebar) ── */
.qo-card {
  background: rgba(201,168,76,.07);
  border: 1px solid rgba(201,168,76,.3);
  border-radius: 10px; padding: 12px 14px; margin: 8px 0 6px 0;
}
.qo-title { font-size: .82rem; font-weight: 700; color: #C9A84C; }
.qo-meta  { font-size: .68rem; color: #777; margin-top: 3px; }

/* ── RECENT CARD ── */
.recent-card {
  background: linear-gradient(145deg, #0C1520 0%, #0F1A28 100%);
  border-radius: 10px; padding: 12px 16px; margin-bottom: 8px;
  border: 1px solid rgba(255,255,255,.05);
  border-left: 3px solid #C9A84C;
  box-shadow: 0 2px 10px rgba(0,0,0,.3);
  transition: all .15s;
}
.recent-card:hover { transform: translateX(3px); }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
  background: #03050A !important;
  border-right: 1px solid rgba(201,168,76,.12) !important;
}
section[data-testid="stSidebar"] * { color: #CCC !important; }
section[data-testid="stSidebar"] strong,
section[data-testid="stSidebar"] b  { color: #C9A84C !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(201,168,76,.15) !important; }

section[data-testid="stSidebar"] input {
  background: #0A1220 !important;
  border: 1px solid rgba(201,168,76,.3) !important;
  border-radius: 8px !important; color: #FFF !important;
}
section[data-testid="stSidebar"] input::placeholder { color: #444 !important; }
section[data-testid="stSidebar"] input:focus {
  border-color: #C9A84C !important;
  box-shadow: 0 0 0 2px rgba(201,168,76,.18) !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: #0A1220 !important;
  border: 1px solid rgba(201,168,76,.3) !important;
  border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] {
  background: rgba(201,168,76,.2) !important;
  border: 1px solid rgba(201,168,76,.4) !important;
}
section[data-testid="stSidebar"] .stButton button {
  background: linear-gradient(135deg, #C9A84C 0%, #D4AF37 100%) !important;
  color: #07090F !important; border: none !important;
  font-weight: 700 !important; border-radius: 8px !important;
  letter-spacing: .4px; transition: all .2s !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
  opacity: .88 !important; transform: translateY(-1px) !important;
}
section[data-testid="stSidebar"] .stRadio label { color: #AAA !important; font-size: .84rem !important; }
section[data-testid="stSidebar"] .stRadio [aria-checked="true"] + label {
  color: #C9A84C !important; font-weight: 600 !important;
}

/* ── MAIN BUTTONS ── */
.stButton button {
  border-radius: 8px !important; font-size: .76rem !important;
  font-weight: 500 !important;
  background: rgba(201,168,76,.07) !important;
  border: 1px solid rgba(201,168,76,.22) !important;
  color: #C9A84C !important; transition: all .15s !important;
}
.stButton button:hover {
  background: rgba(201,168,76,.18) !important;
  border-color: #C9A84C !important; transform: translateY(-1px) !important;
}

hr { border-color: rgba(201,168,76,.1) !important; margin: 6px 0 !important; }

.stAlert {
  background: rgba(201,168,76,.05) !important;
  border: 1px solid rgba(201,168,76,.18) !important;
  border-radius: 10px !important;
}

/* expander */
details summary {
  background: rgba(201,168,76,.05) !important;
  border: 1px solid rgba(201,168,76,.15) !important;
  border-radius: 8px !important; color: #C9A84C !important;
  font-weight: 600 !important; font-size: .85rem !important;
}

/* section label override */
.section-lbl {
  font-size: .65rem; color: #C9A84C; font-weight: 700;
  text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;
}

/* ── INLINE VIEWER PANEL ── */
.viewer-panel {
  background: linear-gradient(145deg, #080E18 0%, #0A1525 100%);
  border: 1px solid rgba(201,168,76,.35);
  border-radius: 16px; padding: 16px 20px;
  margin: 14px 0 22px 0;
  box-shadow: 0 4px 30px rgba(0,0,0,.5);
}
.viewer-title {
  font-size: .88rem; font-weight: 700; color: #C9A84C;
  margin-bottom: 10px; display: flex; align-items: center; gap: 6px;
}

/* ── MOBILE RESPONSIVE ── */
@media screen and (max-width: 768px) {
  .block-container { padding: 0.6rem 0.8rem 2rem 0.8rem !important; }
  .dash-title       { font-size: 1.05rem !important; }
  .dash-sub         { font-size: .60rem !important; }
  .dash-ts-val      { font-size: .65rem !important; }
  .stat-box         { padding: 12px 6px !important; }
  .stat-num         { font-size: 1.5rem !important; }
  .stat-lbl         { font-size: .52rem !important; }
  .file-title       { font-size: .80rem !important; }
  .file-meta        { font-size: .62rem !important; }
  .cat-header       { font-size: .78rem !important; padding: 10px 14px !important; }
  .qo-title         { font-size: .76rem !important; }
  .qo-meta          { font-size: .64rem !important; }
  /* Stack all Streamlit columns to full-width on small screens */
  [data-testid="column"] { min-width: 100% !important; width: 100% !important; }
  /* Viewer: use more vertical space on phone */
  .viewer-panel object,
  .viewer-panel iframe { height: 85vh !important; }
}
</style>
""", unsafe_allow_html=True)

# ── constants ─────────────────────────────────────────────────────
SKIP_DIRS = {
    "BACK UP VERSION","Videos","PHOTOS","Articles","Fruits",
    "Natures Remss","Plants & Herbs That Destroy Cancer",
    "Top hair Shampoo in the world","Lost iPhone",
    "Photos of Main Door","Clean photos","01. VITAMINS",
}

FILE_ICONS = {
    ".pdf":"📄",".docx":"📝",".doc":"📝",".gdoc":"☁️",
    ".gsheet":"📊",".jpg":"🖼️",".jpeg":"🖼️",".png":"🖼️",
    ".avif":"🖼️",".mp4":"🎬",".mp3":"🎵",".xlsx":"📊",
}

FOLDER_CAT = {
    "Ashwagandha":"Herbal Products","Black Seed Oil":"Herbal Products",
    "Cordyceps":"Herbal Products","Haritaki":"Herbal Products",
    "Shikakai":"Herbal Products","Shilajit":"Herbal Products",
    "Shungite":"Herbal Products","Spirulina":"Herbal Products",
    "01. Herbal Products & Botanicals":"Herbal Products",
    "02. Essential Oils":"Essential Oils",
    "03. Vitamins & Supplements":"Vitamins & Supplements",
    "Magnesium":"Vitamins & Supplements",
    "14. Advanced Supplements":"Vitamins & Supplements",
    "19. L-Lysine & Amino Acids":"Vitamins & Supplements",
    "04. Dental Health":"Dental Health",
    "05. Pharmaceutical & Medicine":"Medicine",
    "18. Ivermectin Research":"Medicine",
    "06. Grounding & Earthing Technology":"Biohacking",
    "04. Grounding Sheets & Earthing":"Biohacking",
    "07. Dr. Abas Mazni - Natural Remedies":"Natural Products",
    "08. Nutrition - Fruits & Food Therapy":"Nutrition",
    "09. Ghee & Healthy Fats":"Nutrition",
    "10. Green Juice & Superfoods":"Nutrition",
    "16. Medicinal Teas & Herbal Infusions":"Nutrition",
    "Oil of Oregano & Black Seed Oil":"Nutrition",
    "Olive oil":"Nutrition",
    "06. Therapeutic Oils & Natural Extracts":"Nutrition",
    "11. Hair Care & Shampoo Analysis":"Personal Care",
    "02. Personal Care & Hygiene Products":"Personal Care",
    "Hair Control PP405":"Personal Care",
    "Pharmacopia Verbena Body Wash":"Personal Care",
    "BRESIH - Natural Cleaning Products":"Personal Care",
    "13. Topical Sprays & Suncare":"Personal Care",
    "12. Natural Health Plants & Air Purification":"Plants & Environment",
    "15. Chemical Exposure & Toxicology":"Chemicals",
    "17. Borax Research":"Chemicals",
    "20. Biomarkers & Diagnostics":"Medical Science",
    "23. Water Quality & Hydration":"Environment",
    "10. Skincare & Toxicology Analysis":"Skincare",
    "03. Home Cleaning & Maintenance":"Home",
    "04. Travel & Flight Intelligence":"Travel",
    "05. Home Development & Smart Living":"Home Development",
    "01. Solar Energy Systems":"Home Development",
    "02. Swimming Pool Health & Technology":"Home Development",
    "03. Faraday Cage & EMF Protection":"Home Development",
    "05. Tower Garden & Vertical Farming":"Home Development",
    "06. Kitchen Equipment & Cookware":"Home Development",
    "07. Interior Lighting & Shelf Design":"Home Development",
    "08. Indowud - Composite Building Materials":"Home Development",
    "09. Construction & Sustainable Materials":"Home Development",
    "07. Business & Market Intelligence":"Business",
    "08. Technology & Smart Devices":"Technology",
    "01. iPhone Security & Optimization":"Technology",
    "02. PLAUD - AI Voice Recording":"Technology",
    "03. Easy Expense - Expense Management":"Technology",
    "04. Zilkee - Recovery Converter":"Technology",
    "05. Proton Mail - Privacy & Security":"Technology",
    "06. Eufy by Anker - Smart Home Security":"Technology",
    "07. Phone Intelligence & OSINT Tools":"Technology",
    "08. Smart Switches & Home Automation":"Technology",
    "09. Litecard - Digital Business Card":"Technology",
    "09. Automotive Research":"Automotive",
    "22. Reference - Scientific Evidence":"Reference",
    "_Reference & Index":"Reference",
    "21. Miscellaneous Health":"Misc",
    "11. Lifestyle & Mindset":"Lifestyle",
    "12 Law of Karma you should know":"Lifestyle",
}

CAT_COLORS = {
    "Herbal Products":"#1E7F4E","Essential Oils":"#117A65",
    "Vitamins & Supplements":"#1A5276","Dental Health":"#6C3483",
    "Medicine":"#B03030","Biohacking":"#283593",
    "Natural Products":"#6B6E29","Nutrition":"#0E7490",
    "Personal Care":"#922B5E","Plants & Environment":"#2D6A4F",
    "Chemicals":"#D4620A","Medical Science":"#1A5276",
    "Environment":"#117A65","Skincare":"#922B5E",
    "Home":"#2E4057","Home Development":"#2E4057",
    "Travel":"#1A5276","Business":"#7E5109",
    "Technology":"#1B3A5C","Automotive":"#2E4057",
    "Misc":"#555","Lifestyle":"#C9A84C",
    "Reference":"#6B6B6B","Uncategorised":"#444",
}

CAT_EMOJI = {
    "Herbal Products":"🌿","Essential Oils":"🫙","Vitamins & Supplements":"💊",
    "Dental Health":"🦷","Medicine":"💉","Biohacking":"⚡",
    "Natural Products":"🍃","Nutrition":"🥑","Personal Care":"🧴",
    "Plants & Environment":"🌱","Chemicals":"⚗️","Medical Science":"🔬",
    "Environment":"💧","Skincare":"✨","Home":"🏠",
    "Home Development":"🏗️","Travel":"✈️","Business":"📊",
    "Technology":"💻","Automotive":"🚗","Misc":"📁",
    "Lifestyle":"☀️","Reference":"📌","Uncategorised":"❓",
}

RISK_MAP = {
    "haritaki_fluoride_pineal": ("MODERATE","Use with Limitation"),
    "purejit_shilajit":         ("MODERATE","Use with Caution"),
    "nitric_oxide":             ("LOW","Safe to Use"),
    "nitric oxide":             ("LOW","Safe to Use"),
    "moringa_risk":             ("LOW","Recommended"),
    "beetroot_risk":            ("LOW","Recommended"),
    "beetroot_ complete":       ("LOW","Recommended"),
    "acidic_bonding_toxicity":  ("MODERATE","Use with Caution"),
    "coconut_jasmine_toxicity": ("LOW","Use with Care"),
    "eye_cream_toxicity":       ("MODERATE","Use with Caution"),
    "gliss_ultimate_repair":    ("MODERATE","Use with Caution"),
    "cork_construction":        ("LOW","Recommended"),
    "translucent_concrete":     ("MODERATE","Use with Caution"),
    "paper_bottle_business":    ("MODERATE","Viable Opportunity"),
    "watercress":               ("LOW","Recommended"),
    "spirulina":                ("LOW","Recommended"),
    "shungite":                 ("MODERATE","Use with Caution"),
    "faraday cage":             ("LOW","Informational"),
    "methylene blue":           ("MODERATE","Consult Doctor"),
    "borax":                    ("MODERATE","Use with Caution"),
    "swimming in chlorinated":  ("MODERATE","Use with Caution"),
    "saltwater swimming":       ("LOW","Recommended"),
    "ozone systems":            ("LOW","Recommended"),
    "hayward aquarite":         ("LOW","Recommended"),
    "ashwagandha":              ("LOW","Recommended"),
}

# ── helpers ───────────────────────────────────────────────────────
def get_category(filepath: Path) -> str:
    parts = filepath.relative_to(BASE).parts
    for p in reversed(parts[:-1]):
        if p in FOLDER_CAT:
            return FOLDER_CAT[p]
    for p in parts[:-1]:
        if p in FOLDER_CAT:
            return FOLDER_CAT[p]
    return "Uncategorised"

def get_risk(name: str):
    n = name.lower()
    for k, v in RISK_MAP.items():
        if k in n:
            return v
    return ("", "")

def clean_name(fname: str) -> str:
    stem = Path(fname).stem
    n = re.sub(r"[_\-]+"," ", stem)
    n = re.sub(r"\s+"," ", n).strip()
    words = []
    for w in n.split():
        words.append(w if (w.isupper() and len(w) > 1) or w.isdigit() else w.capitalize())
    return " ".join(words)

def file_icon(fname: str) -> str:
    return FILE_ICONS.get(Path(fname).suffix.lower(), "📄")

MAX_DOWNLOAD_MB = 100  # files larger than this won't be served as downloads

def get_download_data(path: Path):
    """Read a file's bytes for use with st.download_button.
    Returns None for files that are missing or exceed MAX_DOWNLOAD_MB."""
    try:
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > MAX_DOWNLOAD_MB:
            return None, f"File too large to serve ({size_mb:.0f} MB)"
        with open(path, "rb") as f:
            return f.read(), None
    except Exception as exc:
        return None, str(exc)

# ── scanner ───────────────────────────────────────────────────────
@st.cache_data(ttl=REFRESH_SECS)
def scan_files():
    records = []
    for dirpath, dirnames, filenames in os.walk(BASE):
        dirnames[:] = [d for d in sorted(dirnames)
                       if d not in SKIP_DIRS and not d.startswith(".")]
        for fname in sorted(filenames):
            if fname.startswith(".") or fname == "desktop.ini":
                continue
            fp = Path(dirpath) / fname
            try:
                mtime = datetime.fromtimestamp(fp.stat().st_mtime)
            except Exception:
                continue
            risk, rec = get_risk(fname)
            cat = get_category(fp)
            rel = str(fp.relative_to(BASE))
            records.append({
                "path":   fp,
                "rel":    rel,
                "fname":  fname,
                "name":   clean_name(fname),
                "ext":    fp.suffix.lower(),
                "icon":   file_icon(fname),
                "cat":    cat,
                "risk":   risk,
                "rec":    rec,
                "date":   mtime,
                "date_s": mtime.strftime("%d %b %Y"),
                "is_report": bool(risk) or any(
                    k in fname.lower() for k in
                    ["report","brief","research","analysis","toxicity",
                     "assessment","guide","review","study"]),
            })
    records.sort(key=lambda x: x["date"], reverse=True)
    return records

# ── badge helper ─────────────────────────────────────────────────
def risk_badge(risk):
    if risk == "LOW":
        return '<span class="badge badge-low">✅ LOW</span>'
    elif risk == "MODERATE":
        return '<span class="badge badge-moderate">⚠️ MOD</span>'
    elif risk == "HIGH":
        return '<span class="badge badge-high">🔴 HIGH</span>'
    return ""

# ── load data ─────────────────────────────────────────────────────
records = scan_files()

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style='text-align:center;padding:18px 0 8px;'>
      <div style='font-size:2.2rem;'>🔬</div>
      <div style='font-size:1.05rem;font-weight:800;color:#C9A84C;letter-spacing:-.2px;'>Mr Mike</div>
      <div style='font-size:.68rem;color:#7A5F2A;margin-top:2px;letter-spacing:1.2px;text-transform:uppercase;'>Research Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── 1. KEYWORD FILTER ─────────────────────────────────────────
    st.markdown('<div class="section-lbl">🔍 Keyword Filter</div>', unsafe_allow_html=True)
    search = st.text_input(
        "Search", placeholder="Type keywords to filter all files...",
        label_visibility="collapsed", key="kw_search"
    )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── 2. DROPDOWN QUICK-OPEN ────────────────────────────────────
    st.markdown('<div class="section-lbl">⚡ Quick Open — Type to Find File</div>', unsafe_allow_html=True)

    # Build dropdown options: "Icon  Name  [Category]"
    NONE_OPT = "— start typing to search —"
    dropdown_opts = [NONE_OPT] + [
        f"{r['icon']}  {r['name']}  [{r['cat']}]"
        for r in records
    ]
    # Map option string → record
    opt_map = {
        f"{r['icon']}  {r['name']}  [{r['cat']}]": r
        for r in records
    }

    selected_opt = st.selectbox(
        "Quick Open",
        dropdown_opts,
        label_visibility="collapsed",
        key="quick_open_select"
    )

    # Show mini-card + open button when file is selected
    if selected_opt and selected_opt != NONE_OPT:
        qr = opt_map.get(selected_opt)
        if qr:
            st.markdown(f"""
            <div class="qo-card">
              <div class="qo-title">{qr['icon']} {qr['name']}</div>
              <div class="qo-meta">
                📂 {qr['cat']}&nbsp;&nbsp;·&nbsp;&nbsp;🗓 {qr['date_s']}
                {f"&nbsp;&nbsp;·&nbsp;&nbsp;" + risk_badge(qr['risk']) if qr['risk'] else ""}
              </div>
              {f'<div style="font-size:.68rem;color:#D4820A;margin-top:4px;">→ {qr["rec"]}</div>' if qr["rec"] else ""}
            </div>
            """, unsafe_allow_html=True)
            bc1, bc2 = st.columns(2)
            with bc1:
                data, err = get_download_data(qr["path"])
                if data:
                    st.download_button(
                        "📥 Download", data=data,
                        file_name=qr["fname"],
                        key="qo_download",
                        use_container_width=True,
                    )
                elif err:
                    st.warning(err, icon="⚠️")
            with bc2:
                st.markdown(
                    f"<div style='font-size:.65rem;color:#4A5568;padding:8px 0;'>"
                    f"{qr['ext'].replace('.','').upper()}</div>",
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    # ── 3. FILTERS ────────────────────────────────────────────────
    st.markdown('<div class="section-lbl">🏷 Filters</div>', unsafe_allow_html=True)

    all_cats = sorted(CAT_COLORS.keys())
    selected_cats = st.multiselect(
        "Category", all_cats,
        placeholder="All categories", label_visibility="visible"
    )

    risk_filter = st.multiselect(
        "Risk Level", ["LOW","MODERATE","HIGH","Reports Only"],
        placeholder="All levels", label_visibility="visible"
    )

    type_filter = st.multiselect(
        "File Type",
        ["📄 PDF","📝 Word","☁️ GDoc","📊 Sheets","🖼️ Image","🎬 Video"],
        placeholder="All types", label_visibility="visible"
    )

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── 4. SORT ───────────────────────────────────────────────────
    st.markdown('<div class="section-lbl">↕ Sort By</div>', unsafe_allow_html=True)
    sort_by = st.selectbox(
        "Sort", ["🆕 Newest First","📅 Oldest First","🔤 Name A–Z","🔤 Name Z–A","📂 Category"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # ── 5. VIEW MODE ──────────────────────────────────────────────
    st.markdown('<div class="section-lbl">👁 View Mode</div>', unsafe_allow_html=True)
    view_mode = st.radio(
        "View", ["📂 By Category","📋 All Files","🆕 Recently Added","🔬 Risk Reports"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # ── 6. REFRESH ────────────────────────────────────────────────
    if st.button("🔄  Refresh Now", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown(
        f"<div style='font-size:.65rem;color:#4A3A1A;text-align:center;"
        f"margin-top:5px;letter-spacing:.4px;'>Auto-refresh every {REFRESH_SECS}s</div>",
        unsafe_allow_html=True
    )

# ── APPLY FILTERS ─────────────────────────────────────────────────
filtered = records[:]

if search:
    q = search.lower()
    filtered = [r for r in filtered
                if q in r["name"].lower()
                or q in r["cat"].lower()
                or q in r["rel"].lower()
                or q in r["fname"].lower()]

if selected_cats:
    filtered = [r for r in filtered if r["cat"] in selected_cats]

if risk_filter:
    def risk_match(r):
        if "Reports Only" in risk_filter:
            return r["is_report"]
        return r["risk"] in risk_filter
    filtered = [r for r in filtered if risk_match(r)]

if type_filter:
    ext_map = {
        "📄 PDF":[".pdf"],"📝 Word":[".docx",".doc"],
        "☁️ GDoc":[".gdoc"],"📊 Sheets":[".gsheet",".xlsx"],
        "🖼️ Image":[".jpg",".jpeg",".png",".avif"],"🎬 Video":[".mp4"],
    }
    allowed = []
    for tf in type_filter:
        allowed += ext_map.get(tf, [])
    filtered = [r for r in filtered if r["ext"] in allowed]

# ── APPLY SORT ────────────────────────────────────────────────────
if sort_by == "🆕 Newest First":
    filtered.sort(key=lambda x: x["date"], reverse=True)
elif sort_by == "📅 Oldest First":
    filtered.sort(key=lambda x: x["date"])
elif sort_by == "🔤 Name A–Z":
    filtered.sort(key=lambda x: x["name"].lower())
elif sort_by == "🔤 Name Z–A":
    filtered.sort(key=lambda x: x["name"].lower(), reverse=True)
elif sort_by == "📂 Category":
    filtered.sort(key=lambda x: (x["cat"], x["name"].lower()))

# ── HERO HEADER ───────────────────────────────────────────────────
now_str = datetime.now().strftime("%d %b %Y · %H:%M")
st.markdown(f"""
<div class="dash-header">
  <div class="dash-icon">🔬</div>
  <div>
    <div class="dash-title">Mr Mike — Research Dashboard</div>
    <div class="dash-sub">Personal Knowledge Intelligence System</div>
  </div>
  <div class="dash-ts">
    <div class="dash-ts-val">{now_str}</div>
    <div class="dash-ts-lbl">Last Updated</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── STAT CARDS ────────────────────────────────────────────────────
cats_seen    = set(r["cat"] for r in filtered)
reports_cnt  = sum(1 for r in filtered if r["is_report"])
low_cnt      = sum(1 for r in filtered if r["risk"] == "LOW")
mod_cnt      = sum(1 for r in filtered if r["risk"] == "MODERATE")
high_cnt     = sum(1 for r in filtered if r["risk"] == "HIGH")

c1,c2,c3,c4,c5,c6 = st.columns(6)
for col, num, lbl, color in [
    (c1, len(filtered),    "Total Files",  "#C9A84C"),
    (c2, len(cats_seen),   "Categories",   "#4A90D9"),
    (c3, reports_cnt,      "Reports",      "#7B68EE"),
    (c4, low_cnt,          "✅ Low Risk",   "#52C496"),
    (c5, mod_cnt,          "⚠️ Moderate",  "#E88830"),
    (c6, high_cnt,         "🔴 High Risk",  "#E86060"),
]:
    col.markdown(f"""
    <div class="stat-box" style="border-top-color:{color}">
      <div class="stat-num" style="color:{color}">{num}</div>
      <div class="stat-lbl">{lbl}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ── SEARCH RESULT BANNER ──────────────────────────────────────────
active_filters = []
if search:         active_filters.append(f'keyword "{search}"')
if selected_cats:  active_filters.append(f"{len(selected_cats)} categor{'y' if len(selected_cats)==1 else 'ies'}")
if risk_filter:    active_filters.append(f"risk: {', '.join(risk_filter)}")
if type_filter:    active_filters.append(f"type: {', '.join(type_filter)}")

if active_filters:
    st.markdown(f"""
    <div class="srb">
      🔍 Showing <strong>{len(filtered)}</strong> of <strong>{len(records)}</strong> files
      &nbsp;·&nbsp; Filtered by: {' + '.join(active_filters)}
    </div>""", unsafe_allow_html=True)

# ── FILE CARD RENDERER ────────────────────────────────────────────
def render_file_card(r, col, border_color):
    with col:
        rb   = risk_badge(r["risk"])
        ext  = r["ext"].replace(".","").upper()
        path_parts = str(r["rel"]).split(os.sep)
        short_path = "/".join(path_parts[-3:]) if len(path_parts) >= 3 else r["rel"]

        st.markdown(f"""
        <div class="file-card" style="border-left-color:{border_color}">
          <div class="file-title">
            {r['icon']} {r['name']}{rb}
            <span class="badge badge-type">{ext}</span>
          </div>
          <div class="file-meta">📁 …/{short_path}&nbsp;&nbsp;·&nbsp;&nbsp;🗓 {r['date_s']}</div>
          {f'<div class="file-rec">→ {r["rec"]}</div>' if r["rec"] else ""}
        </div>""", unsafe_allow_html=True)

        data, err = get_download_data(r["path"])
        if data:
            st.download_button(
                "📥 Download", data=data,
                file_name=r["fname"],
                key=f"dl_{r['rel']}",
                use_container_width=True,
            )
        elif err:
            st.caption(f"⚠️ {err}")

# ══════════════════════════════════════════════════════════════════
# VIEW: BY CATEGORY
# ══════════════════════════════════════════════════════════════════
if view_mode == "📂 By Category":
    if not filtered:
        st.info("No files match your current filters. Try adjusting the search or filters.")
    else:
        by_cat = defaultdict(list)
        for r in filtered:
            by_cat[r["cat"]].append(r)

        # Jump-to dropdown
        jcol1, jcol2 = st.columns([1, 3])
        with jcol1:
            sorted_cats = sorted(by_cat.keys())
            jump_opts   = ["— Jump to category —"] + [
                f"{CAT_EMOJI.get(c,'📁')} {c} ({len(by_cat[c])})" for c in sorted_cats
            ]
            st.selectbox("Jump to", jump_opts, label_visibility="collapsed", key="jump_cat")

        for cat in sorted(by_cat.keys()):
            items  = by_cat[cat]
            color  = CAT_COLORS.get(cat, "#888")
            emoji  = CAT_EMOJI.get(cat, "📁")
            rpts   = sum(1 for i in items if i["is_report"])

            with st.expander(
                f"{emoji}  {cat}   ·   {len(items)} files  ·  {rpts} reports",
                expanded=True
            ):
                # 3-column grid
                cols = st.columns(3)
                for idx, r in enumerate(items):
                    render_file_card(r, cols[idx % 3], color)

# ══════════════════════════════════════════════════════════════════
# VIEW: ALL FILES
# ══════════════════════════════════════════════════════════════════
elif view_mode == "📋 All Files":
    st.markdown(f"""
    <div class="cat-header" style="background:linear-gradient(135deg,#1A2744,#0F1928)">
      📋 All Files
      <span class="cat-pill">{len(filtered)} files · sorted by {sort_by}</span>
    </div>""", unsafe_allow_html=True)

    if not filtered:
        st.info("No files match your current filters.")
    else:
        cols = st.columns(3)
        for idx, r in enumerate(filtered):
            color = CAT_COLORS.get(r["cat"], "#888")
            render_file_card(r, cols[idx % 3], color)

# ══════════════════════════════════════════════════════════════════
# VIEW: RECENTLY ADDED
# ══════════════════════════════════════════════════════════════════
elif view_mode == "🆕 Recently Added":
    st.markdown("""
    <div class="cat-header" style="background:linear-gradient(135deg,#7E5109,#5A3A08)">
      🆕 Recently Added Files
      <span class="cat-pill">Last 50 files by date</span>
    </div>""", unsafe_allow_html=True)

    recent = sorted(filtered, key=lambda x: x["date"], reverse=True)[:50]
    if not recent:
        st.info("No files found.")
    else:
        for r in recent:
            emoji = CAT_EMOJI.get(r["cat"], "📁")
            rb    = risk_badge(r["risk"])
            c1, c2 = st.columns([6, 1])
            with c1:
                st.markdown(f"""
                <div class="recent-card">
                  <div class="file-title">{r['icon']} {r['name']}{rb}</div>
                  <div class="file-meta">
                    {emoji} {r['cat']} &nbsp;·&nbsp;
                    📁 {r['rel'].split(os.sep)[-2] if os.sep in r['rel'] else 'Root'}
                    &nbsp;·&nbsp; 🗓 {r['date_s']}
                    {f"&nbsp;·&nbsp; → {r['rec']}" if r['rec'] else ""}
                  </div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)
                data, err = get_download_data(r["path"])
                if data:
                    st.download_button(
                        "📥", data=data,
                        file_name=r["fname"],
                        key=f"rec_{r['rel']}",
                        use_container_width=True,
                    )
                elif err:
                    st.caption(f"⚠️ {err}")

# ══════════════════════════════════════════════════════════════════
# VIEW: RISK REPORTS
# ══════════════════════════════════════════════════════════════════
elif view_mode == "🔬 Risk Reports":
    st.markdown("""
    <div class="cat-header" style="background:linear-gradient(135deg,#2C0A0A,#3D1515)">
      🔬 Risk Reports & Research Briefs
      <span class="cat-pill">Classified by risk level</span>
    </div>""", unsafe_allow_html=True)

    risk_records = [r for r in filtered if r["is_report"]]

    if not risk_records:
        st.info("No reports match current filters.")
    else:
        for level, label, section_color in [
            ("HIGH",     "🔴 HIGH RISK",      "#B03030"),
            ("MODERATE", "⚠️ MODERATE RISK",  "#D4620A"),
            ("LOW",      "✅ LOW RISK",        "#1E7F4E"),
            ("",         "📄 Unrated Reports", "#4A4A4A"),
        ]:
            group = [r for r in risk_records if r["risk"] == level]
            if not group:
                continue

            with st.expander(f"{label}  ·  {len(group)} reports", expanded=(level in ("HIGH","MODERATE"))):
                cols = st.columns(3)
                for idx, r in enumerate(sorted(group, key=lambda x: x["name"])):
                    render_file_card(r, cols[idx % 3], section_color)

# ── FOOTER ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style='text-align:center;font-size:.68rem;color:#333;padding:6px 0 10px;'>
  Mr Mike Research Dashboard &nbsp;·&nbsp;
  <span style='color:#C9A84C;'>v3.0</span> &nbsp;·&nbsp;
  {len(records)} files indexed
</div>""", unsafe_allow_html=True)
