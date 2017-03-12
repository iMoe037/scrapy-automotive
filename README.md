# Scrapy-AutoMotive

## Update - Due to caranddriver transitioning from static HTML to Angular Components. This Script is no longer working and is not being actively maintained.

This project uses Scrapy to scape car data from the web.

What infomation does it pull?

 * Latest Makes
 * Latest Models
 * MSRP Range & Price
 * Vehicle Type
 * Engine Type
 * Transmission Type
 * Car Dimensions
 * Image Url
 * Car Summary
 * 5 star Rating
 * City / Highway MPG
 * 0 -60 & Top Speed
 * and more Specs...

Which sites are being scraped?

 * [Car & Driver](http://www.caranddriver.com/)
 * [Left Lane](http://www.leftlanenews.com/)

What does the data look like?

XML or JSON with Scrapy

<a href="http://imgur.com/XV8bx6h"><img src="http://i.imgur.com/XV8bx6h.png" title="source: imgur.com" /></a>

What do I need to run the scrapper?

*	Python
*	Pip
*	Scrapy

If you need these google is your friend, if your on mac I'd use [Homebrew](http://brew.sh/) to simplify the install process

I had a virtualenv setup in the root directory

Assuming you have everything installed and an virtual env

```sh
$ source venv/bin/activate
```
****You might have called you virtual env something else I called mine venv. Go to your venv folder or whatever you called it**

You should see this in your terminal
```sh
(venv) username $

```

If all is good, then

```sh
$ pip install scrapy
$ cd automotive
```
Command  to get results in terminal

```sh
$ scrapy crawl automotive
```
If you want to export the data to a csv or jSON, add to the command: flag -o and give it a file name like thedata.csv or anothername.json

Example
```sh
$ scrapy crawl automotive -o mynameforfile.csv
$ scrapy crawl automotive -o mybetternameforafile.json
```


**To Do**
* Scrape more pictures
* Maybe add reviews
