# GiQuant

This Python package contain various tools for Quantative Finance and Trading.
It should be considered an alpha version but feel free to try it out!

Install from PyPi with: `python3 -m pip install giquant`


## TimeSeriesLanguage

`giquiant.tsl` is a DSL (domain specific language) for manipulation of time series.

Show the help with: `python3 -m giquant.tsl.expr --help`


## Trading

The trade subpackage has some tools related to trading.

Show the help with:

* `python3 -m giquant.trade.dwnl --help`
* `python3 -m giquant.trade.cl --help`
* `python3 -m giquant.trade.cc --help`


## Web Server

I'm using Phusion Passenger 6 when deploying GiQuant to a web server (since its compatible with older python versions). 
Any WSGI server can be used though, see the  [Flask docs](https://flask.palletsprojects.com/en/stable/deploying/) for 
the details of deployment of Flask apps.

```
# Create the necessary folders and config according the docs of you web & WSGI server
# It is useful to set `PassengerAppEnv development` (or the equivalent) when configuring everything 
# (just remember to remove this when finished).

# In the code folder for the new app. For instance /var/www/siteX
cp /var/www/venv1/lib/python3.X/site-packages/giquant/tsl/passenger_wsgi.py .

# change passenger_wsgi.py to
from giquant.tsl.server import app
application = app

```
