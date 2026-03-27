# eZamDB: eZamówienia Data Extractor

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Requests](https://img.shields.io/badge/library-requests-lightgrey.svg)
![Pandas](https://img.shields.io/badge/library-pandas-green.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Technical Stack](#️-technical-stack)
- [Repository Structure](#-repository-structure)
- [How It Works](#-how-it-works)
- [Usage](#-usage)
- [Input Validation](#-input-validation)
- [Data Source](#️-data-source)
- [Related Repositories](#-related-repositories)
- [License](#-license)

---

## 📌 Project Overview

This repository is the **first stage** of the eZamówienia data pipeline. It extracts tender data from the official Polish public procurement platform — **[eZamówienia](https://ezamowienia.gov.pl)** — via its REST API.

The tool downloads **contract notices** (, ) within a specified **date range** and **CPV code**, handles cursor-based pagination automatically in pages of 500 records, and exports the results to a CSV file ready for the next pipeline stage.

> **Part of a larger project:**
> **`eZam-Database-extraction`** → [`eZam-Database-formating`](https://github.com/98CharleS/eZam-Database-formating) → *(analysis & Tableau dashboards — coming soon)*

---

## 🛠️ Technical Stack

- **Language:** Python
- **HTTP Client:** `requests`
- **Data Processing:** `pandas`
- **Output format:** CSV

---

## 📁 Repository Structure

```
eZam-Database-extraction/
│
├── main.py             # Entry point — orchestrates extraction & pagination
├── extract.py          # HTTP requests, JSON parsing, data structuring
├── link_maker.py       # Builds API request URLs with dates, CPV & pagination
├── date_transform.py   # Parses and converts date strings for API use
├── validations.py      # Input validation — dates format, order & CPV code
└── README.md
```

---

## 🔄 How It Works

### Pagination Strategy

The eZamówienia API uses cursor-based pagination via a `SearchAfter` parameter. The extractor handles this automatically:

1. **Validates** input dates and CPV code format.
2. **Fetches** the first page and stores results in a DataFrame.
3. **Loops** — each iteration uses the last record's `ObjectId` as the `SearchAfter` cursor for the next request.
4. **Terminates** when the number of new records matches the previous page, indicating the end of available data.
5. **Exports** all accumulated records to `output.csv`.

### Extracted Fields

Each record in the output CSV contains:

| Field | Description |
|---|---|
| `id` | Internal sequential ID assigned by the script |
| `ObjectId` | API pagination cursor |
| `tenderId` | Unique tender identifier |
| `noticeNumber` | Official notice number |
| `bzpNumber` | BZP (Public Procurement Bulletin) number |
| `orderObject` | Description of the order |
| `orderType` | Type of procedure |
| `cpvCode` | CPV code of the tender |
| `publicationDate` | Date the tender was published |
| `submittingOffersDate` | Deadline for submitting offers |
| `organizationName` | Name of the procuring organization |
| `organizationCity` | City of the procuring organization |
| `organizationCountry` | Country of the procuring organization |
| `isBelowEUThreshold` | Whether the amount is below the EU threshold |
| `Result` | Procedure result |

---

## 🚀 Usage

### Prerequisites

```bash
pip install requests pandas
```

### Configuration

Open `main.py` and set the three variables at the top of the file:

```python
date1 = "01.01.2024"   # Start date (DD.MM.YYYY)
date2 = "31.12.2024"   # End date   (DD.MM.YYYY)
cpv   = "all"          # CPV code to filter by, or "all" for no filter
```

### Run

```bash
python main.py
```

Results are saved to `output.csv` in the project root (using `;` as delimiter). If the default location is not writable, the script will prompt for an alternative save path.

---

## ✅ Input Validation

The `validations.py` module checks all inputs before any API call is made:

- Date format must follow `DD.MM.YYYY` (both `.` and `-` separators are accepted)
- Start date must be earlier than or equal to the end date
- CPV code must follow the format `XXXXXXXX-X` (8 digits, dash, 1 check digit) — e.g. `42111100-1`, or `"all"` to skip CPV filtering

---

## 🗺️ Data Source

Data is sourced from the **[eZamówienia REST API](https://ezamowienia.gov.pl)** — the official platform for public procurement in Poland, operated under EU directive requirements.

---

## 🔗 Related Repositories

| Repository | Description |
|---|---|
| *(this repo)* | Stage 1 — API extraction to CSV |
| [eZam-Database-formating](https://github.com/98CharleS/eZam-Database-formating) | Stage 2 — CSV → SQLite, cleaning & aggregations |
| *(coming soon)* | Stage 3 — Analysis & Tableau dashboards |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
