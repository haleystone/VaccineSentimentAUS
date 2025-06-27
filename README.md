# Twitter Historical Data Collector

This project collects historical tweets using the Twitter API v2 and saves them for downstream analysis of sentiment across different languages.

---

## Features

- Query historical tweets using specific search terms
- Language-aware query construction
- Location-based filtering 
- Data collection with place metadata
- Integration with Jupyter notebooks or direct script use

---

## Structure
twitter-collector/

├── TwitterCollector.py # Class for querying the API

├── config.py # Loads Twitter API credentials from .env

├── run_historical_collection.py # Script to run collection

├── requirements.txt # pip environment

├── environment.yml # conda environment (optional)

├── search_terms.xlsx # Input Excel with search terms

├── LICENSE

├── README.md

└── .env # API credentials (not committed)
