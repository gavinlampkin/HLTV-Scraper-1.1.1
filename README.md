# HLTV Scraper

This HLTV scraper is used for scraping stats from top teams and players specified by date or all time.

## Libraries Needed


```bash
pip install selenium
pip install bs4
pip install pandas
pip install sys
pip install datetime
```

## Usage

```python
scraper.py

# for fast usage
Method 1 (Specifying Start Date & End Date) Example:
	py cs.py 2022-07-03 2022-10-23
Method 2 (Specifying Start Date only, End Date will be considered as of today) Example:
	py cs.py 2022-07-03
Method 3 (Searching for a specific player's stats!) Example searching for player name 's1mple':
	py cs.py search for s1mple

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
