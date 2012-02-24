import re
import mechanize
#import _mysql
import MySQLdb
import time

from user_info import *

sleep_time = 0.4

conn = MySQLdb.connect(host=mysqlHost,user=mysqlUser,passwd=mysqlPasswd,db=mysqlDB)
cursor = conn.cursor()

br = mechanize.Browser()
br.set_handle_robots(False)
br.open("https://www.nascarmedia.com/login.aspx")

br.select_form(name='main')
br['CT_Right_0$txtEmail'] = nascar_user
br['CT_Right_0$txtPassword'] = nascar_pw

response = br.submit()

error_file = open('nascar_error.txt', 'a')


print response.geturl()

baseURL = "https://www.nascarmedia.com"


def getCenterString( text, beginMarker, endMarker, inclusive ):
	startIndex = text.find(beginMarker) 
	if(startIndex == -1) :
		return False
	endIndex = text.find(endMarker,startIndex + len(beginMarker))
	if( endIndex == -1) :
		return False
	
	if ( inclusive ):
		new_text = text[startIndex :endIndex + len(endMarker)]
	else:
		new_text = text[startIndex + len(beginMarker):endIndex]
	return new_text

def getCenterStrings( text, beginMarker, endMarker, inclusive ):
	ar = [ ]
	startIndex = text.find(beginMarker)
	while (startIndex != -1 ):
		endIndex = text.find(endMarker,startIndex + len(beginMarker))
		if( inclusive ):
			center_text = text[startIndex : endIndex + len(endMarker)]
		else:
			center_text = text[startIndex + len(beginMarker) : endIndex]

		ar.append(center_text)

		startIndex = text.find(beginMarker,endIndex + len(endMarker))
	return ar

def dealWithPackage(url, pulledTitle, year, div, link):


	cursor.execute("""SELECT ID FROM Package WHERE Year = %s AND url1 = %s ORDER BY ID DESC""", (year, url)) 
	if(cursor.rowcount >= 1) :
		return False

	time.sleep(sleep_time)
	resp3 = br.open(url)
	content2 = resp3.read()

	mainContent = getCenterString(content2, "CT_Main_1_pnlStatPackage", "<div class=\"clearboth\">", False)

	title = getCenterString(mainContent, "<h2>", "</h2>", False)
	if(title == False):
		title = ""


	cursor.execute("""INSERT INTO Package (Year, divHTML, linkHTML, url1, title1, url2, title2) VALUES (%s, %s, %s, %s, %s, %s, %s)""", (int(year), div, link, url, pulledTitle, resp3.geturl(), title))
	
	cursor.execute("""SELECT ID FROM Package WHERE Year = %s AND url1 = %s ORDER BY ID DESC""", (year, url)) 
	row = cursor.fetchone()
	pid = row[0]
	
	tindex1 = url.find("stat_packages.aspx")
	if(tindex1 != -1):
		tindex = url.find("LoopPackage")
		if(tindex == -1):
			dealWithSimplePackage(mainContent,pid)
		else:
			dealWithLoopPackage(mainContent,pid)
	else:
		print "ERROR: ", url
		error_file.write("ERROR: " + url)





def dealWithSimplePackage(mainContent,pid,lid=-1):

	links = getCenterStrings(mainContent, "<strong>", "</strong>", False)
	sectionHeader = ""
	for link in links:
		# Make sure not header, if so continue
		# May want to use in the future?
		if ( link.find("<a") == -1 ) :
			sectionHeader = getCenterString(link, "<u>", "</u>", False)
			continue

		url = getCenterString(link, "href=\"", "\"", False)

		#linkTitle does not catch cases like "Alphabetical" and "By Car"
		linkTitle = getCenterString(link, "\">", "</a>", False)

		print url, "\n", linkTitle

		tindex1 = url.find("stat_packages.aspx")
		if(tindex1 == -1):
			print "ERROR: ",url
			error_file.write("ERROR: " + url)
			continue

		dealWithContentPage(baseURL + url, linkTitle, sectionHeader, pid, link,lid)



def dealWithLoopPackage(mainContent,pid):

	mainContent = getCenterString(mainContent, "CT_Main_1_pnlStatPackageSeries", "</div>", False)

	links = getCenterStrings(mainContent, "<a", "</a>", True)
	sectionHeader = ""
	for link in links:

		url = getCenterString(link, "href=\"", "\"", False)

		linkTitle = getCenterString(link, "\">", "</a>", False)
		
		print url, "\n", linkTitle

		tindex1 = url.find("stat_packages.aspx")
		if(tindex1 == -1):
			print "ERROR: ",url
			error_file.write("ERROR: " + url)
			continue


		time.sleep(sleep_time)
		resp3 = br.open(baseURL + url)
		content2 = resp3.read()

		mainContent2 = getCenterString(content2, "CT_Main_1_pnlStatPackage", "<div class=\"clearboth\">", False)

		title = getCenterString(mainContent, "<h2>", "</h2>", False)
		if(title == False):
			title = ""

		cursor.execute("""INSERT INTO LoopPackage (PID, LinkHTML, title, url, title2, url2) VALUES (%s, %s, %s, %s, %s, %s)""", (pid, link, linkTitle, url, title, resp3.geturl()))
	
		cursor.execute("""SELECT ID FROM LoopPackage WHERE PID = %s AND url = %s ORDER BY ID DESC""", (pid, url)) 
		row = cursor.fetchone()
		lid = row[0]

		dealWithSimplePackage(mainContent2,pid,lid)



def dealWithContentPage(url, pulledTitle, sectionHeader, pid, link,lid):
	time.sleep(sleep_time)
	resp3 = br.open(url)
	content2 = resp3.read()

	mainContent = getCenterString(content2, "CT_Main_1_pnlStatPackageLink", "<div class=\"clearboth\">", False)

	title = getCenterString(mainContent, "<h2>", "</h2>", False)
	if(title == False):
		title = ""

	cursor.execute("""INSERT INTO ContentPages (PackageID, LoopID, linkHTML, sectionHeader, url1, title1, url2, title2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (pid, lid, link, sectionHeader, url, pulledTitle, resp3.geturl(), title))
	
	cursor.execute("""SELECT ID FROM ContentPages WHERE PackageID = %s AND LoopID = %s AND url1 = %s ORDER BY ID DESC""", (pid, lid, url)) 
	row = cursor.fetchone()
	cid = row[0]
	
	regex = "<a href=\"[^\"]*\"[^>]*><strong>VIEW [A-Za-z]* FILE</strong></a>"
	fileLinks = re.findall(regex, mainContent)
	for links in fileLinks:
		url = getCenterString(links,"href=\"", "\" ", False)
		filetype = getCenterString(links,"VIEW ", " FILE", False)

		cursor.execute("""INSERT INTO Files (ContentID,linkHTML,filetype, url) VALUES (%s, %s, %s, %s)""", (cid,links,filetype,url))
		




for year in [2005, 2004]:

	time.sleep(sleep_time)
	resp2 = br.open(baseURL + "/news/stat_packages.aspx?packageyear=" + str(year))

	print resp2.geturl()
	

	cursor.execute("""SELECT ID FROM Years WHERE Year = %s ORDER BY ID DESC""", (year)) 
	if(cursor.rowcount < 1):
		cursor.execute("""INSERT INTO Years (ID, Year, URL) VALUES (%s, %s, %s)""", (year, str(year), resp2.geturl()))

	content = resp2.read()

	mainContent = getCenterString(content, "CT_Main_1_pnlStatPackages", "<div class=\"clearboth\">", False)

	if( mainContent == False):
		print "Error for ",  str(year)
		continue
	

	divs = getCenterStrings(mainContent,"<div>","</div>",False)
	for div in divs:
		split = div.find("<br>")
		link1 = div[:split]
		link2 = div[split + len("<br>"):]
		links = [link1, link2]
		if(split == -1):
			links = [div]
		for link in links:
			print link
			url = getCenterString(link, "<a href=\"","\"",False)
			title = getCenterString(link, "\">","</a>",False)
			print url, title

			dealWithPackage(baseURL + url, title, year, div, link)


cursor.close()
conn.close()

error_file.close()
