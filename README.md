General description:
This project is focused on web scraping of data from elections in the Czech repulic in 2017

Libraries requirements:
All mandatory libraries are listed in the file requirements.txt, which is attached to this project
The third party libraries can be installed from the terminal using the command:
pip install -r requirements.txt


Script description:
The script collects: 
    - the code of a selected region
    - name of a city
    - count of registred voters 
    - count of released envelopes
    - count of delivered votes
    - count of votes for each political party in a respective location/city

Script usage:
web_scraper.py "URL" "NAME_OF_THE_OUTPUT_FILE.csv"

The URL arg.:
Navigate to https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ, pick a region of your choice and press the hyperlink "X" character in the "vyber obce" column on the same row.
cCopy the URL from this page and use it as the first argument of the script enclosed by doubleqoutes ("URL")

The csv arg.:
The csv arg is the second mandatory argument. It's a name of the file with ".csv" extension 
Recommended names pattern should contain the name of the region that you've chosen for scraping

example: 
picked region: brno-venkov
results: results_brno_venkov.cs

web_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203" "results_brno_venkov.csv"
