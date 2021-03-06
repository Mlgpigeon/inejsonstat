inejsonstat.py
===========

**IneJsonStat** is a library for reading the [JSON-stat](http://json-stat.org/) data format responses
from the [Spanish National Institute of Stadistics (INE)](https://www.ine.es/)'s [JSON-stat API](https://www.ine.es/dyngs/DataLab/en/manual.html?cid=1259945948443).

JSON-stat is a JSON format specialized in representing datasets mainly for statistic purposes.
It's used by many institutions around the world, such as:

* [Statistics Norway](http://www.ssb.no/en)
* [Eurostat](http://ec.europa.eu/eurostat/)
* [United Nations Economic Commission for Europe](https://w3.unece.org/PXWeb/en)
* [Bank of Portugal](https://bpstat.bportugal.pt/data/docs)
* [Cantabrian Institute of Statistics](https://www.icane.es/)
* Many others...

The main objective of the library its to ease the use interpretation and manipulation
of retrieved data by the means of creating dynamically objects representing the
hierarchically the different levels of information in a retrieved file.

This project is in early stages and has been developed for the [University of Extremadura](https://www.unex.es/).
You can contribute on its [github repository](https://github.com/Mlgpigeon/inejsonstat.git)
or contact me directly in case of doubt or need via **luismasc16@gmail.com**.

## Installation:
```
>>> pip install inejsonstat
```

## Usage of the INE JSON-stat API:

The INE provides their data in two languages:
*'ES' (spanish)
*'EN' (english)

The INE provides table identifiers  for any kind of request,
which are used for the library as inputs
and can be found here:

https://www.ine.es/dyngs/INEbase/listaoperaciones.htm

The INE provides an optional parameter called nult which if not left blank,
it will return only the n, being n an integer, the last terms of the
requested table

Optional date:
If not left blank, it will give the terms of the requested table in:

-date=YYYYMMDD (a given date)
-date=YYYYMMDD&date=YYYYMMDD (a list of given dates)
-date=YYYYMMDD:YYYYMMDD (a range of dates)
