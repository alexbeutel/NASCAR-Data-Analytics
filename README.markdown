NASCAR Data Analytics
==================================

The included code is a number of scripts to scrape nascarmedia.com's Statistical Services.

The scripts are used as follow:

	* nascar_scrape.py is used for crawling nascarmedia.com's Statistical Services and saving link information to a MySQL database
	* download_data.php is used to take all of the links for data file froms NASCAR media and downloading them, both to a file on the computer and the database
	* parse_text.py converts all text (TXT and AGATE) files downloaded to CSV (Excel) format (only by splitting along \t)
	* parse_xml.py converts XML files to CSV format
	* queries.sql are a few MySQL queries to check the datasets available



Dependencies
=================================

nascar scrape.py has a couple Python dependencies:

	* Mechanize: http://wwwsearch.sourceforge.net/mechanize/
	* MySQLdb: http://sourceforge.net/projects/mysql-python/

Also, each script requires MySQL credentials and nascar\_scrape.py requires credentials to login to nascarmedia.com.

Credentials for Python scripts should go in user\_info.py and credentials for download\_data.php should go in user\_info.php