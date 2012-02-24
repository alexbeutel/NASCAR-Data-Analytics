import re
#import _mysql
import MySQLdb
import csv
import time

from user_info import *

sleep_time = 0.5

conn = MySQLdb.connect(host=mysqlHost,user=mysqlUser,passwd=mysqlPasswd,db=mysqlDB)
cursor = conn.cursor()

error_file = open('csv_error.txt', 'a')
index = csv.writer(open('data/csv/index.csv', 'w'), dialect='excel')

tab = "	"

index.writerow( [ "File ID", "Year", "Race", "Loop Title", "Data Section", "Data Title", "Data Title 2", "Content URL", "File URL" ] )


cursor.execute("""SELECT Package.Year, Package.title1, LoopPackage.title, ContentPages.sectionHeader, ContentPages.title2, ContentPages.title1, fi.ID, fi.`file`, fi.`url`, ContentPages.`url2`, ContentPages.ID FROM (SELECT ID,ContentID,url,filetype,`file` FROM Files WHERE (filetype = 'TXT' OR filetype='AGATE')) as fi, ContentPages,LoopPackage, Package WHERE fi.ContentID = ContentPages.ID AND ContentPages.PackageID = Package.ID AND ContentPages.LoopID = LoopPackage.ID ORDER BY fi.ID ASC;""")

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
#10 : ContentPages.ID



for i in range(0,cursor.rowcount):
	row = cursor.fetchone()
	year = row[0]
	fid = row[6]
	
	#print fid, ' - ', row[5]

	filewriter = csv.writer(open('data/csv/' + str(year) + '/' + str(fid) + '.csv', 'wb'), dialect='excel')


	index.writerow( [ row[6], row[0], row[1], row[2], row[3], row[4], row[5], row[10], row[9], row[8] ] )


	filewriter.writerow( [ row[0] ] )
	filewriter.writerow( [ row[1] ] )
	filewriter.writerow( [ row[2] ] )
	filewriter.writerow( [ row[3] ] )
	filewriter.writerow( [ row[4] ] )
	filewriter.writerow( [ row[5] ] )
	filewriter.writerow( [ "FileID: " + str(row[6]) ] )


	txtfile = row[7]
	lines = txtfile.splitlines()
	for l in lines:
		a = l.split("	") #split on tab
		filewriter.writerow(a)








cursor.close()
conn.close()

error_file.close()
