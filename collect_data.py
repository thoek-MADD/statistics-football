import requests as req
import pathlib

country_code = "G"
country = "Greece"
league = "ethnikiKatigoria"
base_url = f"https://www.football-data.co.uk/mmz4281/YEAR/{country_code}1.csv"

year = 0
end_year = 21

path = pathlib.Path(f"data/{country}")
path.mkdir(parents=True, exist_ok=True)

while year < end_year:

    next_year = year + 1
    year_string = f"{year:02d}{next_year:02d}"

    url = base_url.replace("YEAR", year_string)
    r = req.get(url, allow_redirects=True)
    open(f"data/{country}/{league}_{year_string}.csv", "wb").write(r.content)

    year = next_year
