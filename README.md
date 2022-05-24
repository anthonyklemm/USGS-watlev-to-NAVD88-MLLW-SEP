# USGS-watlev-to-NAVD88-MLLW-SEP
Use this to analyze United States Geological Survey (USGS) water level data files to calculate average daily minimum water level over the entire time series of available data.

This code processes tab-delimited USGS water level gauge data to extract
the minimum daily waterlevel values and then graphs the results, including
a 90-day rolling average of the minimum daily water level values with a linear-
regression trendline.
Data can be found through the USGS water dashboard: https://dashboard.waterdata.usgs.gov/
This method produces a quick approximation of the separation value between the
orthometric height datum of the gauge in NAVD88 to NOAA's conventional charting
datum of Mean Lower Low Water (MLLW), if the gauge in in a tidally influenced
waterway. More on tidal datums can be found at NOAA's WEbsite: 
https://tidesandcurrents.noaa.gov/

Most (if not all) USGS water level gauges reference water level heights to NAVD88. By calculating average daily minimum water level, you
are essentially calculating the local vertical separation value between MLLW and gauge datum (NAVD88). The longer your time series, 
the better it will conform to NOAA CO-OPS standard of a 19 year epoch, encapsulating most major tidal harmonic constituents. 

![Screenshot](https://github.com/anthonyklemm/USGS-watlev-to-NAVD88-MLLW-SEP/blob/main/images/90%20day%20rolling%20average.png?raw=true)

