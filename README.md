# 🔬 Mr Mike — Research Dashboard

> **Personal Knowledge Intelligence System** — A private, password-protected Streamlit web app that indexes, categorises, and surfaces every research file stored on your machine. Run it locally on Windows, or deploy it to the cloud.

---

## 📋 Table of Contents

1. [Key Benefits](#-key-benefits)
2. [How It Works](#-how-it-works)
3. [Repository Structure](#-repository-structure)
4. [Research Categories](#-research-categories)
5. [Quick Start (Windows)](#-quick-start-windows)
6. [Manual Install (any OS)](#-manual-install-any-os)
7. [Authentication Setup](#-authentication-setup)
8. [Using the Dashboard](#-using-the-dashboard)
9. [Configuration Reference](#-configuration-reference)
10. [Changing Your Password](#-changing-your-password)
11. [Deploying to Streamlit Cloud](#-deploying-to-streamlit-cloud)

---

## ✨ Key Benefits

| Benefit | Detail |
|---|---|
| 🔐 **Private & Secure** | Login-gated with PBKDF2-HMAC-SHA256 (600,000 iterations). Nobody can browse your files without a password. |
| ⚡ **Instant Search** | Keyword filter + Quick-Open dropdown let you find any file across thousands of documents in under a second. |
| 📂 **Auto-Organised** | Folders are automatically mapped to 24 research categories — no manual tagging needed. |
| ⚠️ **Risk Intelligence** | PDFs and reports are automatically classified as LOW / MODERATE / HIGH risk based on filename patterns. |
| 📱 **Mobile Friendly** | Fully responsive layout — works on phones and tablets as well as desktops. |
| 🖥️ **One-Click Launch** | Double-click `LAUNCH DASHBOARD.bat` — no terminal needed on Windows. |
| 🔄 **Live Refresh** | File index refreshes automatically every 60 seconds. New files appear without restarting. |
| 📥 **Direct Download** | Every file has a one-click download button — no file manager needed. |
| 🏷️ **Multi-Filter** | Filter simultaneously by category, risk level, file type, and keyword. |
| 📊 **At-a-Glance Stats** | Hero stats bar shows total files, categories, reports, and risk counts instantly. |

---

## 🏗️ How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        Your Computer                            │
│                                                                 │
│   Research folders  ──►  research_dashboard.py  ──►  Browser   │
│   (PDFs, Word, etc)       (Streamlit app)           localhost:8501│
└─────────────────────────────────────────────────────────────────┘
```

### Startup flow

1. **`LAUNCH DASHBOARD.bat`** locates Python/Streamlit and runs:
   ```
   streamlit run research_dashboard.py --server.port 8501
   ```
2. **Authentication** — `require_auth()` is called immediately. If the session is not logged in, a login page is shown and `st.stop()` halts execution. No data is loaded until login succeeds.
3. **File Scanner** — `scan_files()` walks every sub-folder from the project root, skips excluded directories (videos, photos, backups), and builds a list of file records containing:
   - File path, name, extension, icon
   - Category (from `FOLDER_CAT` mapping)
   - Risk level + recommendation (from `RISK_MAP` filename patterns)
   - Last-modified date
4. Results are **cached for 60 seconds** (`@st.cache_data(ttl=60)`) so repeated page loads are instant.
5. The **Sidebar** provides keyword search, Quick-Open dropdown, category/risk/type filters, sort order, and view mode.
6. The **Main area** renders whichever view mode is selected, applying all active filters.

### Password security

Passwords are never stored in plain text. The storage format is:

```
<random-salt>$<PBKDF2-HMAC-SHA256 hex, 600,000 iterations>
```

This exceeds OWASP's minimum recommendation and is computationally expensive to brute-force.

---

## 📁 Repository Structure

```
research-project-1/
│
├── research_dashboard.py          ← Main Streamlit application (single file)
├── requirements.txt               ← Python dependencies
├── RESEARCH_INDEX_MASTER.xlsx     ← Optional: master index spreadsheet
├── CLAUDE.md                      ← Inventory control operational notes
│
├── .streamlit/
│   ├── config.toml                ← Streamlit theme & server settings
│   ├── secrets.toml               ← 🔐 Login credentials (NOT committed to git)
│   └── secrets.toml.example       ← Template showing how to set up credentials
│
├── .gitignore                     ← Excludes secrets.toml and cache files
│
│   ── Windows launchers ──
├── INSTALL FIRST (run once).bat   ← Installs all Python packages
├── LAUNCH DASHBOARD.bat           ← Normal daily launcher
├── FIX & LAUNCH DASHBOARD.bat     ← Repairs packages then launches
└── CREATE DESKTOP SHORTCUT.bat    ← Adds shortcut to Windows Desktop
│
│   ── Research folders ──
├── 01. Health & Wellness Research/
├── 02. Personal Care & Hygiene Products/
├── 03. Home Cleaning & Maintenance/
├── 04. Travel & Flight Intelligence/
├── 05. Home Development & Smart Living/
├── 06. Therapeutic Oils & Natural Extracts/
├── 07. Business & Market Intelligence/
├── 08. Technology & Smart Devices/
├── 09. Automotive Research/
├── 10. Skincare & Toxicology Analysis/
└── 11. Lifestyle & Mindset/
```

> **Note:** `secrets.toml` is in `.gitignore` and is never pushed to GitHub. It lives only on your local machine (or in Streamlit Cloud's secrets manager).

---

## 🗂️ Research Categories

The dashboard automatically maps folders to these 24 categories:

| # | Category | Emoji | Example Topics |
|---|---|---|---|
| 1 | Herbal Products | 🌿 | Ashwagandha, Black Seed Oil, Shilajit, Spirulina |
| 2 | Essential Oils | 🫙 | Therapeutic oils, aromatherapy |
| 3 | Vitamins & Supplements | 💊 | Magnesium, L-Lysine, amino acids |
| 4 | Dental Health | 🦷 | Oral care research |
| 5 | Medicine | 💉 | Pharmaceuticals, Ivermectin research |
| 6 | Biohacking | ⚡ | Grounding/earthing technology |
| 7 | Natural Products | 🍃 | Dr. Abas Mazni natural remedies |
| 8 | Nutrition | 🥑 | Ghee, green juice, medicinal teas, olive oil |
| 9 | Personal Care | 🧴 | Hair care, shampoo analysis, hygiene |
| 10 | Plants & Environment | 🌱 | Air purification, indoor plants |
| 11 | Chemicals | ⚗️ | Toxicology, chemical exposure, Borax |
| 12 | Medical Science | 🔬 | Biomarkers, diagnostics |
| 13 | Environment | 💧 | Water quality, hydration |
| 14 | Skincare | ✨ | Toxicology analysis, cosmetics |
| 15 | Home | 🏠 | Home cleaning & maintenance |
| 16 | Home Development | 🏗️ | Solar energy, pool technology, Faraday cage, gardening, kitchen |
| 17 | Travel | ✈️ | Flight intelligence |
| 18 | Business | 📊 | Market intelligence, paper bottle business |
| 19 | Technology | 💻 | iPhone, PLAUD, Proton Mail, smart home, OSINT |
| 20 | Automotive | 🚗 | Automotive research |
| 21 | Lifestyle | ☀️ | Mindset, Law of Karma |
| 22 | Reference | 📌 | Scientific evidence, index |
| 23 | Misc | 📁 | Miscellaneous health |
| 24 | Uncategorised | ❓ | Files not matching any known folder |

---

## 🚀 Quick Start (Windows)

### Step 1 — Install Python (once)

Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) to the default location:
`C:\Users\USER\Miniconda3\`

> If you already have Python in your system PATH, the launchers will use that instead.

### Step 2 — Install dependencies (once)

Double-click:
```
INSTALL FIRST (run once).bat
```
This installs Streamlit, watchdog, and all required packages. Takes about 1–2 minutes. You only need to do this **once**.

### Step 3 — Set up login credentials

1. Copy `.streamlit/secrets.toml.example` → `.streamlit/secrets.toml`
2. Generate your password hash (see [Authentication Setup](#-authentication-setup))
3. Edit `secrets.toml` with your chosen username and hash

### Step 4 — Launch

Double-click:
```
LAUNCH DASHBOARD.bat
```

A browser window opens automatically at **http://localhost:8501**

### Step 5 — (Optional) Desktop shortcut

Double-click:
```
CREATE DESKTOP SHORTCUT.bat
```

A shortcut named **"Mr Mike Research Dashboard"** appears on your Desktop.

---

### 🔧 Troubleshooting

If the dashboard gives an error on launch, use the repair launcher instead:

```
FIX & LAUNCH DASHBOARD.bat
```

This reinstalls/upgrades all packages before launching.

---

## 💻 Manual Install (any OS)

```bash
# 1. Clone or download the project
git clone https://github.com/ibrahimkhalilmasud/research-project-1.git
cd research-project-1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up credentials
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml with your credentials (see Authentication Setup)

# 4. Run the dashboard
streamlit run research_dashboard.py
```

Open your browser at **http://localhost:8501**

---

## 🔐 Authentication Setup

The dashboard requires a username and password on every session start.

### Credential file location

```
.streamlit/secrets.toml
```

### Format

```toml
[auth]
username      = "your_username"
password_hash = "<salt>$<pbkdf2-hmac-sha256-hex>"
```

### Generate a password hash

Run this one-liner in your terminal:

```bash
python3 -c "
import hashlib, binascii, os
salt = binascii.hexlify(os.urandom(16)).decode()
dk   = hashlib.pbkdf2_hmac('sha256', b'yourpassword', salt.encode(), 600000)
print(salt + '\$' + binascii.hexlify(dk).decode())
"
```

Replace `yourpassword` with your actual password. Copy the printed string into `secrets.toml` as the value of `password_hash`.

### Default credentials (change immediately)

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `MrMike2024!` |

> ⚠️ **Change the default password** before using this in any shared or internet-accessible environment.

### Security notes

- Passwords are hashed with **PBKDF2-HMAC-SHA256 at 600,000 iterations** — exceeds OWASP minimum.
- `secrets.toml` is listed in `.gitignore` and is **never committed to GitHub**.
- On Streamlit Cloud, set credentials via the **Secrets** panel in the dashboard settings (not via a file).

---

## 🖥️ Using the Dashboard

### Login screen

Enter your username and password. The sidebar and all files are hidden until login succeeds.

### Sidebar controls

| Control | What it does |
|---|---|
| **🔍 Keyword Filter** | Type any word to instantly filter all files by name, path, category, or filename |
| **⚡ Quick Open** | Searchable dropdown of every file — start typing to narrow, then click Download |
| **🏷 Category filter** | Multi-select one or more of the 24 categories |
| **Risk Level filter** | Filter by LOW / MODERATE / HIGH / Reports Only |
| **File Type filter** | Filter by PDF, Word, GDoc, Sheets, Image, or Video |
| **↕ Sort By** | Newest First · Oldest First · Name A–Z · Name Z–A · Category |
| **👁 View Mode** | Choose one of four views (see below) |
| **🔄 Refresh Now** | Force-reload the file index immediately |
| **🚪 Sign Out** | Logs you out and returns to the login screen |

### View modes

#### 📂 By Category *(default)*
All files grouped under collapsible category sections. Each section shows a count of files and reports. Files appear in a **3-column grid** with download buttons.

#### 📋 All Files
Every file in a single flat 3-column grid, sorted by the selected sort option. Useful for seeing everything at once or browsing by date.

#### 🆕 Recently Added
The **50 most recently modified files**, sorted newest first. Use this to see what you've added or updated lately.

#### 🔬 Risk Reports
Only files flagged as reports or risk assessments, grouped into:
- 🔴 **HIGH RISK** — expanded by default
- ⚠️ **MODERATE RISK** — expanded by default
- ✅ **LOW RISK**
- 📄 **Unrated Reports**

### File cards

Each file card shows:
- **Icon + Name** (cleaned, human-readable)
- **Risk badge** (LOW / MODERATE / HIGH)
- **File type badge** (PDF, DOCX, etc.)
- **Folder path** (last 3 levels)
- **Last modified date**
- **Recommendation** (e.g. "Use with Caution", "Recommended")
- **📥 Download button**

### Stats bar

The top of the main area shows six live counters:

| Stat | Description |
|---|---|
| Total Files | Number of files matching current filters |
| Categories | Number of distinct categories in results |
| Reports | Files flagged as research reports or assessments |
| ✅ Low Risk | Files with LOW risk rating |
| ⚠️ Moderate | Files with MODERATE risk rating |
| 🔴 High Risk | Files with HIGH risk rating |

---

## ⚙️ Configuration Reference

### `.streamlit/config.toml`

```toml
[theme]
base                     = "dark"
primaryColor             = "#C9A84C"      # Gold accent colour
backgroundColor          = "#07090F"      # Near-black background
secondaryBackgroundColor = "#0A1220"      # Sidebar background
textColor                = "#DCE4F0"      # Body text colour

[server]
headless       = true    # No browser auto-open when headless
enableCORS     = false
maxUploadSize  = 200     # MB — for future upload features
```

### `research_dashboard.py` — key constants

| Constant | Default | Purpose |
|---|---|---|
| `REFRESH_SECS` | `60` | File index cache TTL in seconds |
| `MAX_PREVIEW_MB` | `50` | PDFs larger than this fall back to download-only |
| `MAX_DOWNLOAD_MB` | `100` | Files larger than this cannot be downloaded |
| `_PBKDF2_ITERATIONS` | `600_000` | Password hash iterations (OWASP-compliant) |
| `SKIP_DIRS` | *(set of folder names)* | Folders excluded from the file scan |

### Adding a new research category

1. Add an entry to `FOLDER_CAT` in `research_dashboard.py`:
   ```python
   "My New Folder Name": "My Category",
   ```
2. Add a colour to `CAT_COLORS`:
   ```python
   "My Category": "#2E86C1",
   ```
3. Add an emoji to `CAT_EMOJI`:
   ```python
   "My Category": "🧪",
   ```

### Adding a new risk keyword

Add an entry to `RISK_MAP`:
```python
"keyword_in_filename": ("MODERATE", "Use with Caution"),
```

---

## ☁️ Deploying to Streamlit Cloud

1. Push your code to a **public or private GitHub repository** (the `secrets.toml` file is gitignored and will not be included).
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repository.
3. Set the main file path to `research_dashboard.py`.
4. Open **Settings → Secrets** and paste your credentials:
   ```toml
   [auth]
   username      = "your_username"
   password_hash = "your-salt$your-hash"
   ```
5. Deploy. Your dashboard will be available at a public URL, protected by the login screen.

> **Note:** Streamlit Cloud does not have access to your local research files. For cloud deployment you would need to store your files in cloud storage (e.g. Google Drive, S3) and adapt the file scanner accordingly.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `streamlit` | ≥ 1.35.0 | Web framework powering the entire dashboard |
| `starlette` | ≥ 0.46.0 | Required by current Streamlit (HTTP routing) |
| `watchdog` | ≥ 3.0 | File system watcher for live reload |

All dependencies are standard library or installable with `pip install -r requirements.txt`. No database, no backend server — just Python and a browser.

---

## 🛡️ Privacy & Security

- **Local-first** — All files stay on your machine. Nothing is uploaded anywhere.
- **No telemetry** — Usage stats collection is disabled (`--browser.gatherUsageStats false`).
- **Session-based auth** — Each browser session requires login. Closing the tab or clicking Sign Out ends the session.
- **Secrets never in git** — `.gitignore` explicitly excludes `secrets.toml`.

---

*Mr Mike Research Dashboard v3.0 — Personal Knowledge Intelligence System*
