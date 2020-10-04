# Limerick & Mid-West Travel Information

This application allows users to view information related to air, rail, bus and bike transport services in Limerick and the wider Mid-Western region on an interactive Google Map. Information is gathered from various APIs and data sources and presented in tabular format upon a user clicking on a marker.

- Airport data is gathered using the API supplied by Aviation Stack:<br>https://aviationstack.com/.
- Rail data is gathered using the official Irish Rail API:<br>http://api.irishrail.ie/realtime/index.htm?realtime_irishrail.
- Bus data is gathered and presented using Ireland's GTFS dataset, which may be downloaded from this link:<br>https://www.transportforireland.ie/transitData/google_transit_combined.zip.
- Bikeshare station data is gathered using the Coca-Cola Bike Share API:<br>https://data.bikeshare.ie/dataapi/resources/station/data/list.

The airport and bikeshare station data each require an API key to be accessed. These can be acquired by requesting one from each of the following:<br>
<tb>- https://aviationstack.com/signup/free<br>
<tb>- https://www.bikeshare.ie/contact-us.html<br>
Each of these APIs are subject to strict usage limits, so in order to ensure that these limits are remained within at all times scraper scripts are used to acquire all required information. These scripts are designed to be executed regularly using a scheduler such as cron.