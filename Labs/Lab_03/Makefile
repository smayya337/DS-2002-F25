.PHONY: all fetch analyze clean

analyze: fetch
	echo 'Analyzing data...' && ./analyze_data.sh && echo 'Analyzed data!'

fetch:
	echo 'Fetching raw METARs...' && ./fetch_metars.sh && echo 'Fetched raw METARs!'

clean:
	echo 'Cleaning workspace...' && rm -rf raw_metars weather_report.csv && echo 'Cleaned workspace!'

all: clean fetch analyze

