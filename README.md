# O2O_crawler

Collect information on China O2O startups in recent 10 years (2008-2017). 

# Prerequisite

Phantomjs 2.1.1 (**Firefox + geckodriver** also works)

Selenium 3.4.3

# Installment

Download Phantomjs from [Phantomjs.org](http://phantomjs.org/download.html). Add the excutable phantomjs.exe to PATH. 

`Pip install -U (--user) selenium`


# Usage

`python crawler_juzi.py` 

Create a list of startups from [Juzi](https://radar.itjuzi.com) data source.

`python crawler_article.py` 

Search for their articles on [Google](https://www.google.com).
