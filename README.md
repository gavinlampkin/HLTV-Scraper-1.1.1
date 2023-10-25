# HLTV Scraper

HLTV Scraper is used for retrieving data from HLTV.org. I chose to use selenium instead of requests to get a better understanding of how it works.
You can retrieve top players' and teams' stats effortlessly as well as look up your favorite player and see how they compare to the average statistics.
LIVE match data from your favorite teams is available in real-time, coming soon, all of the data available on HLTV will be compared against the other teams' players and data.

## Libraries Needed


```bash
pip install selenium
pip install bs4
pip install pandas
pip install sys
pip install datetime
```

## Usage
py scraper.py
```python
For Fast Usage:
Method 1 (Specifying Start Date & End Date) Example:
	py scraper.py 2022-07-03 2022-10-23
 
Method 2 (Specifying Start Date only, End Date will be considered as of today) Example:
	py scraper.py 2022-07-03
 
Method 3 (Searching for a specific player's stats!) Example searching for player name 's1mple':
	py scraper.py search for s1mple
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
