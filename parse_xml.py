import re
#import _mysql
import MySQLdb
import csv
import time
from xml.dom.minidom import *

from user_info import *

sleep_time = 0.5

conn = MySQLdb.connect(host=mysqlHost,user=mysqlUser,passwd=mysqlPasswd,db=mysqlDB)
cursor = conn.cursor()

error_file = open('csv_error.txt', 'a')
index = csv.writer(open('data/xmlcsv/index.csv', 'w'), dialect='excel')

tab = "	"

index.writerow( [ "File ID", "Year", "Race", "Loop Title", "Data Section", "Data Title", "Data Title 2", "Content ID", "Content URL", "File URL" ] )


cursor.execute("""SELECT Package.Year, Package.title1, LoopPackage.title, ContentPages.sectionHeader, ContentPages.title2, ContentPages.title1, fi.ID, fi.`file`, fi.`url`, ContentPages.`url2`, ContentPages.ID FROM (SELECT ID,ContentID,url,filetype,`file` FROM Files WHERE (filetype = 'XML') AND file != '') as fi, ContentPages,LoopPackage, Package WHERE fi.ContentID = ContentPages.ID AND ContentPages.PackageID = Package.ID AND ContentPages.LoopID = LoopPackage.ID ORDER BY fi.ID ASC;""")

#0: Year
#1: Package.title1
#2: LoopPackage.title
#3: ContentPages.sectionHeader
#4: ContentPages.title2
#5: ContentPages.title1
#6: File.ID
#7: file
#8: File.URL
#9: ContentPages.URL
#10: Content.ID


def getNode(nodelist, tagname):
	for i in range(0,nodelist.length) :
		x = nodelist.item(i)
		if x.nodeType == Node.ELEMENT_NODE and x.tagName == tagname :
			return x
	return False

for i in range(0,cursor.rowcount):
	row = cursor.fetchone()
	year = row[0]
	fid = row[6]
	
	#print fid, ' - ', row[5]

	filewriter = csv.writer(open('data/xmlcsv/' + str(year) + '/' + str(fid) + '.csv', 'wb'), dialect='excel')


	index.writerow( [ row[6], row[0], row[1], row[2], row[3], row[4], row[5], row[10], row[9], row[8] ] )


	filewriter.writerow( [ row[0] ] )
	filewriter.writerow( [ row[1] ] )
	filewriter.writerow( [ row[2] ] )
	filewriter.writerow( [ row[3] ] )
	filewriter.writerow( [ row[4] ] )
	filewriter.writerow( [ row[5] ] )
	filewriter.writerow( [ "File ID: " + str(row[6]) ] )
	filewriter.writerow( [ "Content ID: " + str(row[10]) ] )



	try:
		dom = parseString(row[7])
	except:
		error_file.write("Error Parsing File " + str(fid) + "\n")
		continue


	if ( dom.getElementsByTagName('TimingResults').length == 0 ):
		error_file.write("Error: " + str(fid) + "\n")
		continue

	results = dom.getElementsByTagName('TimingResults')[0].getElementsByTagName("Result")
	props = set()
	for r in results:
		#print r
		for x in r.childNodes:
			if x.nodeType == Node.ELEMENT_NODE:
				props.add(x.tagName)


	props2 = []
	for x in props:
		props2.append(x)

	filewriter.writerow( props2 )

	for r in results:
		row = []
		for x in props2:
			n = getNode(r.childNodes,x)
			if(n and n.childNodes.length > 0):
				row.append(n.childNodes[0].data)
			else:
				row.append("")
		filewriter.writerow(row)





cursor.close()
conn.close()

error_file.close()
