SELECT counts.cid, Files.ID, Files.filetype FROM (SELECT ContentPages.ID as cid, COUNT(*) as cnt FROM ContentPages, (SELECT ID, ContentID, filetype FROM Files WHERE filetype='TXT' OR filetype='XML') as fi WHERE fi.`ContentID`=ContentPages.`ID` GROUP BY ContentPages.ID ORDER BY cnt ASC) as counts, Files WHERE Files.ContentID = counts.cid AND counts.cnt = 1 ORDER BY filetype


SELECT Files.filetype, COUNT(*) FROM (SELECT ContentPages.ID as cid, COUNT(*) as cnt FROM ContentPages, (SELECT ID, ContentID, filetype FROM Files WHERE filetype='TXT' OR filetype='XML') as fi WHERE fi.`ContentID`=ContentPages.`ID` GROUP BY ContentPages.ID ORDER BY cnt ASC) as counts, Files WHERE Files.ContentID = counts.cid AND counts.cnt = 1 GROUP BY Files.filetype


SELECT Files.filetype, COUNT(*) FROM (SELECT ContentPages.ID as cid, COUNT(*) as cnt FROM ContentPages, (SELECT ID, ContentID, filetype FROM Files) as fi WHERE fi.`ContentID`=ContentPages.`ID` GROUP BY ContentPages.ID ORDER BY cnt ASC) as counts, Files WHERE Files.ContentID = counts.cid AND counts.cnt = 1 GROUP BY Files.filetype




/* Are there any files that are just TXT or just XML (not including PDF files) */

SELECT fi2.filetype, COUNT(*) FROM (SELECT ContentPages.ID as cid, COUNT(*) as cnt FROM ContentPages, (SELECT ID, ContentID, filetype FROM Files WHERE Files.filetype='XML' OR Files.filetype='TXT') as fi WHERE fi.`ContentID`=ContentPages.`ID` GROUP BY ContentPages.ID ORDER BY cnt ASC) as counts, (SELECT ID, ContentID, filetype FROM Files WHERE Files.filetype='XML' OR Files.filetype='TXT') as fi2 WHERE fi2.ContentID = counts.cid AND counts.cnt = 1 GROUP BY fi2.filetype



/* What are the just XML ones? */
SELECT fi2.ID, fi2.ContentID, fi2.filetype FROM (SELECT ContentPages.ID as cid, COUNT(*) as cnt FROM ContentPages, (SELECT ID, ContentID, filetype FROM Files WHERE Files.filetype='XML' OR Files.filetype='TXT') as fi WHERE fi.`ContentID`=ContentPages.`ID` GROUP BY ContentPages.ID ORDER BY cnt ASC) as counts, (SELECT ID, ContentID, filetype FROM Files WHERE Files.filetype='XML' OR Files.filetype='TXT') as fi2 WHERE fi2.ContentID = counts.cid AND counts.cnt = 1 AND fi2.filetype='XML'




/* 
	Check how many files are only availble in one format 
	Most important if only PDF
 */

SELECT fi2.filetype, COUNT(*) FROM (SELECT ContentPages.ID as cid, COUNT(*) as cnt FROM ContentPages, (SELECT ID, ContentID, filetype FROM Files WHERE Files.filetype='XML' OR Files.filetype='TXT' or Files.filetype='PDF') as fi WHERE fi.`ContentID`=ContentPages.`ID` GROUP BY ContentPages.ID ORDER BY cnt ASC) as counts, (SELECT ID, ContentID, filetype FROM Files WHERE Files.filetype='XML' OR Files.filetype='TXT' OR Files.filetype='PDF') as fi2 WHERE fi2.ContentID = counts.cid AND counts.cnt = 1 GROUP BY fi2.filetype





/* Get Files that should be filled in already but are not */
SELECT Package.year,fi.* FROM (SELECT ID,ContentID,url,filetype,file FROM Files WHERE (filetype = 'TXT' OR filetype = 'XML') AND (file is NULL OR file = "")) as fi, ContentPages, Package WHERE fi.ContentID = ContentPages.ID AND ContentPages.PackageID = Package.ID AND (Package.year = 2011 OR Package.year = 2010 OR Package.year = 2009 );


