# myHomeSearchProject2
### A home search app deployed in Heroku for Project 2
Find the right home for your family’s needs. Is your first question in finding a home is which school will my children attend?  Then myHomeSearch app is the right home search for you. If you know which school you would like for your kids to go, just choose school name in the drop-down menu and fill in the specifications you want for your house and click search. This will return a list of homes available within the boundary of that school. If you don’t know the schools in the area, just use our list of top-ranking schools with the corresponding median home prices in the area. This app will take the home buying experience to a new level and will eliminate frustration and save you time.  
## Do some web scraping
### scrapeSchoolRanking.ipynb/school_ranking.csv
This file was used to scrape www.niche.com, a school ranking website, to get the top 25 public high schools in San Diego County. Returned data was stored in school_ranking.csv.
### zillowScraper.ipynb
This file was used to scrape https://zillow.com for current homes for sale based on the zip codes of the top 25 ranking school in San Diego County. We had to insert a time delay code to trick the web interface from thinking it is being scraped. The output of the scraping is up to 20 home ids per zip code. Apparently, Zillow to protect their data, uses different pool of ids between the web API interface and the web itself so these ids were ultimately not useful for this app. Auth ors kept this code as future reference for scraping the website.
### Zillow.ipynb/all_comps.csv
This file was used instead to get 20 home data per zip code using these steps:
1.  Go to Zillow website to get the address of a home for sale per zipcode.
1.	Run the deepSearch API to get the zpid for that home
1.	Using that zpid, run the compSearch API to get comparable properties. Specify the number of properties to be returned.
1.	Return the result as a csv fle (all_comps.csv)
1.	A total of 450 properties was returned.
### Fetch_by_zip.py/median_price_SDcounty.csv
To get the median home prices per zip code, the Zillow getRegionChildren API was used. Returned data was stored in median_price_SDcounty.csv.
### schoolRanking_medianPrice.ipynb
The files school_ranking.csv and median_price_SDcounty.csv are joined to combine the data. This file has the school ranking information and the median home prices per school zip code. It also has the longitude and latitude information per school for geo-mapping used in logic.js.
### Database
Sqlite was used as a database for the data storage. DBeaver was used as the editor of choice for this database.
### Appchart.js 
Create a scatter plot using d3/js. Plot the school ranking and home median prices per school zip code and use the affordability ratio as size of the circles.
