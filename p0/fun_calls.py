import sqlite3
import urllib.request
import pypdf
import re
import sqlite3
from sqlite3 import Error


def fetchincidents(url):

    
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"                          
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()       # Sending a request to URL and obtaining content 

    #print(type(data))

    with open("Extracted.pdf", 'wb') as e:                                  # Writing the <bytes> type content to file - Extracted.pdf
        e.write(data)

    listings = []               
    collect = []

    with open('Extracted.pdf', 'rb') as content:
        reader = pypdf.PdfReader(content)                                   # reading content from the pdf file
        text = []

        for page in reader.pages:                                           # traversing through all pages of the pdf file
            text.append(page.extract_text())                                # saving content of all pages as each item of list
        
          
    with open('Resultant.txt','w') as r:                                    # Generating a .txt file with the content items of list
        for i in text:
            r.write(i+'\n')
    
    with open('Resultant.txt', 'r') as p:                                   # reading lines of text and saving to a list - listings
        listings.append(p.readlines())

    for i in range(len(listings[0])):                                       # saving each line of content as item og a list - collect
        collect.append(listings[0][i])
    
    return collect


def extractincidents(collect):
    
    
    """ for i in collect:
        print(i) """
    
    a = re.search(r'D\w*e \/ T\w*e',collect[0]).group()        # Regular Expressions for Header fields in file - Date / Time, Incident Number, Location, Nature, Incident ORI
    b = re.search(r'I\w*t N\w*r',collect[0]).group()           # re.search to match the pattern of the field name and saving them to a variable
    c = re.search(r'L\w*n',collect[0]).group()
    d = re.search(r'Na\w*e',collect[0]).group()
    e = re.search(r'I\w*t O\w*I',collect[0]).group()

    #print(len(collect))                                       # Retruns number of rows of content in pdf file 

    date_time = []                                             # Lists to save each field value of pdf file
    incident_number = []
    ori = []
    address = []
    nature = []

    stop_lines = []                                            # To identify rows which are exceeding the content in specific line and with continuation on the following line

    for i in range(1, len(collect)-1):                         # List traversal excluding 1st row - Headers, last row - pdf updated time stamp which need not be considered as part of "Date / Time" (i.e, 1/2/2023 10:25)
        
        dt = re.search(r'^\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{1,2}', collect[i])
    
        if(dt):                                                 # If pattern match with "Date / Time", saving to a list
            date_time.append(dt.group())
        else:                                                   # Else, Index capture of rows with extra content
            stop_lines.append(i)
    
    #print(stop_lines)

    for i in stop_lines:
        _ = collect[i].strip()
        collect[i-1] = collect[i-1].strip() + _                # Appending the lines with excess content to it's previous line
        collect[i] = ''                                        # Updating the stop_lines as empty. **If we pop(), indexes change and becomes tough to organize**

    row_count = 0       
    
    for i in range(1, len(collect)-1):
        
        if(collect[i]!=''):

            row_count+=1
        
            x = re.search(r"\d{4}-\d{8}", collect[i])

            if(x):
                incident_number.append(x.group())

            y = re.search(r"[C][O][P] \w*|[M][V][A] \w*|[9][1][1] [C][a][l][l]\w*|[A-Z][a-z]\w*",collect[i][x.end():].strip())

            if(y):
                address.append(collect[i][x.end():x.end()+y.start()].strip())
            elif(re.findall(r'^\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{1,2}', collect[i])):
                address.append('NA')
            
            if(x and y):
                z = re.compile(r'EMSSTAT|1400\d{1}|OK\d{7}', re.X)
                zoi = re.search(z, collect[i][x.end()+y.end():])

            if(z):
                ori.append(zoi.group())

            #print(x, y)                                                                   # To validate indices boundaries - Incident Number & Nature

            if(y and z):
                nature.append(collect[i][x.end()+y.start():x.end()+y.end()+zoi.start()].strip())
            elif(re.findall(r'^\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{1,2}', collect[i])):
                nature.append('NA')
            
        
    incidents = []

    for i in range(row_count):
        incidents.append((date_time[i], incident_number[i], address[i], nature[i], ori[i]))

    """ for i in range(len(incidents)):
        print(incidents[i]) """
    
    return incidents



def createdb(db_file, stmt):
    """ create a database connection to a SQLite database & create a table """
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS incidents;")
        cursor.execute(stmt)
        cursor.close()
    except Error as e:
        print("Error Occured", e)
    finally:
        if conn:
            conn.close()
    
def populatedb(db_file, incidents):

    try:
        sql = ''' INSERT INTO incidents(incident_time,incident_number,incident_location,nature,incident_ori) VALUES(?,?,?,?,?) '''

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        for i in range(len(incidents)):
            cursor.execute(sql, incidents[i])
            conn.commit()
        cursor.close()
        
        #print(cursor.lastrowid)
    
    except Error as e:
        print("Error Occured", e)

    finally:
        if conn:
            conn.close()
    


def Sel_status(db_file,query):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for r in rows:
            print(r[0]+'|'+str(r[1]))
        cursor.close()
    
    except Error as e:
        print("Error Occured", e)

    finally:
        if conn:
            conn.close()