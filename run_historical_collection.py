import pandas as pd
import json
from config import Secrets
from TwitterCollector import TwitterCollector

def load_search_terms(file_path):
    """Load search terms from all sheets in an Excel file."""
    df = pd.read_excel(file_path, sheet_name=None)
    search_terms = {
        lang: df_sheet["search_term"].dropna().tolist()
        for lang, df_sheet in df.items()
    }
    return search_terms

def run_collection(language_code, terms):
    """Run Twitter collection for a specific language."""
    secrets = Secrets()
    collector = TwitterCollector(secrets)
    tweets = collector.collect_historical(terms, language_code)
    return tweets

def save_tweets(tweets, output_path):
    """Save collected tweets to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tweets, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # config
    EXCEL_PATH = "search_terms.xlsx"
    LANG_CODE = "en"  # Options: "en", "ar", "vi"
    OUTPUT_JSON = "tweets_en.json"

    # Run the collection
    terms_by_lang = load_search_terms(EXCEL_PATH)
    tweets = run_collection(LANG_CODE, terms_by_lang.get("english", []))
    save_tweets(tweets, OUTPUT_JSON)

