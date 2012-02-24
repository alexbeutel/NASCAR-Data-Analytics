NASCAR Data Analytics
==================================

The included code is a number of scripts to scrape
[nascarmedia.com](https://www.nascarmedia.com/)'s Statistical Services.

The scripts are used as follow:

 * `nascar_scrape.py` is used for crawling [nascarmedia.com](https://www.nascarmedia.com/)'s Statistical
 Services and saving link information to a MySQL database
 * `download_data.php` is used to take all of the links for data file froms
 NASCAR media and downloading them, both to a file on the computer and the
 database
 * `parse_text.py` converts all text (TXT and AGATE) files downloaded to CSV
 (Excel) format (only by splitting along "\\t")
 * `parse_xml.py` converts XML files to CSV format
 * `queries.sql` are a few MySQL queries to check the datasets available

Because `download_data.php`, `parse_text.py` and `parse_xml.py` output data to
the filesystem, all three require specific subfolder structures to output their
files as can be seen in the code.
Also, both `parse_text.py` and `parse_xml.py` make files index.csv, which holds
information about each file outputted.


Dependencies
=================================

`nascar_scrape.py` has a couple Python dependencies:

 * Mechanize: http://wwwsearch.sourceforge.net/mechanize/
 * MySQLdb: http://sourceforge.net/projects/mysql-python/


Each script requires MySQL credentials and `nascar_scrape.py` requires
credentials to login to [nascarmedia.com](https://www.nascarmedia.com/).  Credentials
for Python scripts should go in `user_info.py`, in the form:

	mysqlHost = "MYSQL.SERVERADDRESS.COM" 
	mysqlUser = "MYSQL_USER"
	mysqlPasswd = "MYSQL_PASSWORD"
	mysqlDB = "MYSQL_DATABASE"
	nascar_user = 'NASCAR_MEDIA_USERNAME'
	nascar_pw = 'NASCAR_MEDIA_PASSWORD' 


and credentials for `download_data.php` should go in
`user_info.php`, in the form:

	<?php
	$dbhost = "MYSQL.SERVERADDRESS.COM";
	$db_user ="MYSQL_USER";
	$db_pw = "MYSQL_PASSWORD";
	$database = "MYSQL_DATABASE";
	?>

Table information is included in `mysql_tables.sql`.
