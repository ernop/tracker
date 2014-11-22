----------------------------------------
Life Tracking
----------------------------------------

What is it?
---------------------
A python + django system for tracking purchases and measurements of your life.  Sort of like a better daytum clone.

purchases
--------------
enter everything you buy: cost, quantity, location, and domain (food, body, house etc.) and it will make linkages & nice graphs for you in django, with google charts.

purchases are linked by source (where you got it), who_with, product

products each have a domain of life (transportation, food, drink, health, etc.)

and each object has a page that shows summaries of all the related objects.

measurements
----------------------
enter measurements and it will make little graphs.

diary
------
each "day" page contains 

-all the pictures you've taken that day (from exif data)
-pictures you've saved that day (from create date)
-past/current notes (what notes did you write N years ago?)
-option to add new notes
-add mp3s (recorded in the browser) to notes
-measurements

d3 graphs
-----------------
of who you met, through who, by time

month summary
------------------
expenses grouped by domain
activities / measurements per day

notes
------
a blob of text, or an mp3
