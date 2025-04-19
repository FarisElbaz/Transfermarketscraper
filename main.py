from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.transfermarkt.co.uk"
CONFEDERATIONS = [
    "/wettbewerbe/europa",
    "/wettbewerbe/amerika",
    "/wettbewerbe/afrika",
    "/wettbewerbe/asien",
    "/wettbewerbe/europaJugend",
    "/wettbewerbe/amerikaJugend",
    "/wettbewerbe/afrikaJugend",
    "/wettbewerbe/asienJugend"
]
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_leagues(conf_url, scraped_leagues):
    """Scrape leagues from a confederation page."""
    print(f"Fetching leagues from {conf_url}...")
    response = requests.get(BASE_URL + conf_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    
    leagues = []
    for link in soup.find_all("a", href=True):
        if "/startseite/wettbewerb/" in link["href"]:
            parts = link["href"].split("/")
            league_id = parts[-1]
            league_name = parts[1]  # Extracting correct league name from URL structure
            if league_id not in scraped_leagues:
                leagues.append({"league_name": league_name, "league_id": league_id})
                scraped_leagues.add(league_id)
    
    print(f"Found {len(leagues)} leagues in {conf_url}.")
    return leagues

def scrape_all_leagues():
    all_leagues = []
    scraped_leagues = set()
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_leagues, conf_url, scraped_leagues) for conf_url in CONFEDERATIONS]
        for future in futures:
            leagues = future.result()
            all_leagues.extend(leagues)
    return all_leagues

leagues_df = pd.DataFrame(scrape_all_leagues())
print(leagues_df)