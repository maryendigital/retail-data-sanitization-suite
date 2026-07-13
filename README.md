# 🛒 Retail & E-commerce Data Sanitization Suite

A collection of lightweight, practical Python tools designed to clean, normalize, and structure raw data dumps from web scraping tools. 

### ⚠️ A Note on My Approach ("Vibe Coding")
I am not a traditional software engineer building massive cloud data pipelines. I am an AI Operator who builds **practical, local, AI-assisted Python tools** that take a messy CSV/Excel dump and turn it into a clean, structured, and mathematically sound Excel report ready for business analysis in seconds.

---

## 🛠️ What's Inside?

| Script | Business Use Case | Key Data Cleaning Logic |
| :--- | :--- | :--- |
| `pharmacy_price_normalizer.py` | Cleans daily pricing dumps from pharmacy chains (e.g., Farmatodo). | Detects and converts localized currency formats (e.g., `Bs. 7.608,39` ➡️ `7608.39`). Extracts pure numeric unit prices from messy text strings. |
| `hardware_retail_cleaner.py` | Processes hardware store inventory scrapes (e.g., EPA). | Removes CSS/JS garbage columns, splits base price and decimals, and prepares the dataset for immediate Excel viewing. |
| `ecommerce_catalog_parser.py` | Structures raw marketplace dumps (e.g., MercadoLibre). | Maps technical CSS class names to human-readable business columns (Product, Price, Seller, Stock). |
| `gmaps_data_cleaner.py` | Cleans raw CSV exports from Google Maps. | Programmatically generates validated WhatsApp API links for B2B outreach from raw phone number strings. |

---

## 💡 My Workflow
1. **No over-engineering:** Uses `pandas`, `tkinter` (for simple local file selection), and standard regex.
2. **VS Code Integration:** Generates a temporary `.xlsx` file and automatically opens it in VS Code (using the Excel Viewer extension) for a quick visual sanity check before permanently saving.
3. **Defensive Cleaning:** Handles missing values, weird characters, and mixed decimal/thousand separators without breaking the pipeline.

---

## ⚙️ How to Run
1. Clone the repo.
2. Install dependencies: `pip install pandas openpyxl`
3. Run any script from your terminal: `python pharmacy_price_normalizer.py`
4. Select your raw CSV/Excel file via the GUI, review the preview in VS Code, and choose to save the clean version.

> *"My focus is not on writing complex architecture, but on delivering clean, structured, and reliable data that businesses can actually use to make decisions."*
