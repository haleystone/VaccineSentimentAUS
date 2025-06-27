import csv
import time
from collections import defaultdict

import requests


class TwitterCollector:
    def __init__(self, config) -> None:
        self.bearer_token = config.bearer_token
        self.next_token = None

    def create_headers(self):
        self.headers = {"Authorization": "Bearer {}".format(self.bearer_token)}

    def create_url(self, url):
        self.url = url

    def set_languages(self, lang_code):
        if lang_code == "en":
            lang = "lang:en"
            location = "place_country:AU"
        elif lang_code == "ar" or lang_code == "vi":
            location = ""
            lang = f"lang:{lang_code}"
        else:
            print("invalid language code")
            return
        return lang, location

    def create_query_params(self, search_term, lang, location):
        if location != "":
            geo = ""
        else:
            geo = "has:geo"
        query = f"{search_term} {lang} {location} {geo}"
        query_params = {
            "query": query,
            "start_time": "2021-08-19T12:00:00Z",
            "end_time": "2023-02-19T12:00:00Z",
            "tweet.fields": "created_at,lang,text,geo",
            # 'user.fields': 'username',
            "expansions": "geo.place_id",
            "place.fields": "country,full_name,geo",
            "max_results": 500,
        }
        print(query)
        return query_params

    def connect_to_twitter(self, params):
        if self.next_token:
            # print(self.next_token)
            params["next_token"] = self.next_token
        response = requests.request(
            "GET", self.url, headers=self.headers, params=params
        )
        time.sleep(3.1)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

        response = response.json()
        try:
            self.next_token = response["meta"]["next_token"]
        except:
            # print(f"no next token for {params['query']}")
            pass
        return response

    def collect_historical(self, search_terms, lang):
        all_tweets = []
        lang, location = self.set_languages(lang)
        total_tweets = 0
        ## make duplicate filtering specific to one search term
        for search_term in search_terms:
            loc_library = []
            search_term_ids = []
            q_params = self.create_query_params(search_term, lang, location)
       # for i in range(100):
            try:
                response = self.connect_to_twitter(q_params)
            except:
                print(f"error for query: {search_term}")
                break

            ## exception for no results
            if response["meta"]["result_count"] == 0:
                print(f"no results for {search_term}")
                break
            try:
                loc_library.append(response["includes"])
                for tweet in response["data"]:
                    for place in loc_library:
                        for p in place["places"]:
                            if p["id"] == tweet["geo"]["place_id"]:
                                tweet["location"] = p["full_name"]
                                if tweet["id"] not in search_term_ids:
                                    search_term_ids.append(tweet["id"])
                                    all_tweets.append(tweet)
                                    total_tweets += 1
                                    print(f"{total_tweets} tweets collected")
            except:
                print('error here')
        return all_tweets

    def count_search_terms(self, file_name, lang_search_terms):
        myFile = open(file_name, "r")
        total_tweets = 0
        reader = csv.DictReader(myFile)
        search_terms = defaultdict(int)
        for dictionary in reader:
            total_tweets += 1
            if dictionary["search_term"] in lang_search_terms:
                search_terms[dictionary["search_term"]] += 1

        print("The list of dictionaries is:")
        print(search_terms)
        print(f"number of tweets: {total_tweets}")
