# 🛒 Retail & E-commerce Data Sanitization Suite

A collection of lightweight, practical Python tools designed to clean, normalize, and structure raw data dumps from web scraping tools (e.g., Facebook Marketplace, local e-commerce, pharmacy chains, and hardware stores).

### ⚠️ The Problem I Solve
Raw scraping data is messy. Prices come formatted as `Bs. 7.608,39`, unit prices are hidden inside text strings like `Tabletas a Bs 75.65`, and technical CSS selectors ruin the column names. 

I am not a data engineer building massive cloud pipelines. I build **practical, local, AI-assisted Python tools** that take a messy CSV/Excel dump and turn it into a clean, structured, and mathematically sound Excel report ready for business analysis in seconds.

---

## 💡 My Approach (Vibe Coding & Pragmatism)
These tools are built for **speed, resilience, and local execution**. 
- **No over-engineering:** They use `pandas`, `tkinter` (for simple local file selection), and standard regex.
- **VS Code Integration:** They generate a temporary `.xlsx` file and automatically open it in VS Code (using the Excel Viewer extension) for a quick visual sanity check before permanently saving.
- **Defensive Cleaning:** They handle missing values, weird characters, and mixed decimal/thousand separators without breaking the pipeline.
- **Anti-Bot Awareness:** Includes a pre-flight network check to ensure your IP isn't blocked by Cloudflare/Akamai before you waste time running a massive scraper.

---

## 📂 What's Inside?

| Script | Business Use Case | Key Data Cleaning Logic |
| :--- | :--- | :--- |
| `pharmacy_price_normalizer.py` | Cleans daily pricing dumps from pharmacy chains (e.g., Farmatodo). | Detects and converts localized currency formats (e.g., `1.000,50` ➡️ `1000.50`). Extracts pure numeric unit prices from messy text strings. |
| `hardware_retail_cleaner.py` | Processes hardware store inventory scrapes (e.g., EPA). | Removes CSS/JS garbage columns, splits base price and decimals, and prepares the dataset for immediate Excel viewing. |
| `ecommerce_catalog_parser.py` | Structures raw marketplace dumps (e.g., MercadoLibre). | Maps technical CSS class names to human-readable business columns (Product, Price, Seller, Stock). Filters out junk data. |
| `gmaps_lead_enricher.py` | Cleans raw CSV exports from Google Maps. | Programmatically generates validated WhatsApp API links for B2B outreach from raw phone number strings. |
| `fb_marketplace_converter.py` | Converts raw Facebook Marketplace CSV dumps. | Handles encoding issues (UTF-8/Latin-1), structures the data, and provides a safe VS Code preview before final export. |
| `anti_bot_sonda.py` | Pre-flight network security check. | Uses `curl_cffi` with TLS fingerprinting (`chrome120`) to test if an API/website will block your IP before running the main scraper. |

---

## 🛠️ Tech Stack
- **Core:** Python 3.10+, Pandas, OpenPyXL, Tkinter, Regex
- **Network/Evasion:** `curl_cffi` (for TLS fingerprinting/anti-bot checks)
- **Environment:** Local execution, VS Code (with Excel Viewer extension)

---

## ⚙️ How to Run
1. Clone the repository.
2. Install dependencies: 
   ```bash
   pip install pandas openpyxl tk curl_cffi
