from p0 import fun_calls
import sqlite3

#Sample URL test

url = "https://www.normanok.gov/sites/default/files/documents/2023-02/2023-02-27_daily_incident_summary.pdf"

def test_fetch():
    
    content = fun_calls.fetchincidents(url)  # Fetch content from url
    
    assert len(content)!=0                  # Check if the retruned content list is empty

def test_extract():
    
    content = fun_calls.fetchincidents(url)
    collect = fun_calls.extractincidents(content)       #extract incidents from given url

    assert type(collect) is list and len(collect) != 0  # Checking if return type is list and if its empty

def test_dbcreate():

    fun_calls.createdb('normanpd.db',"CREATE TABLE incidents (incident_time TEXT,incident_number TEXT,incident_location TEXT,nature TEXT,incident_ori TEXT);")        # Create db and table - incidents
    conn = sqlite3.connect('normanpd.db')  # Connecting to database
    cursor = conn.cursor()  # specifying cursor object to execute queries
    cursor.execute("select count(*) from incidents;")

    assert cursor.fetchall()[0][0] == 0  # Checks if the cursor returns an empty result set with 0 rows

def test_dbinsert():

    content = fun_calls.fetchincidents(url)
    collect = fun_calls.extractincidents(content) 
    db = fun_calls.createdb('normanpd.db',"CREATE TABLE incidents (incident_time TEXT,incident_number TEXT,incident_location TEXT,nature TEXT,incident_ori TEXT);")
    fun_calls.populatedb('normanpd.db', collect)
    conn = sqlite3.connect('normanpd.db')  # Connecting to database
    cursor = conn.cursor()

    assert cursor.lastrowid != 0 # Checks if the table entries are made and last row id is not equal to 0

def test_resultstatus():
    
    query = "select nature,count(*) as Nature_Count from incidents group by nature order by Nature_Count desc,nature"
    conn = sqlite3.connect('normanpd.db')  # Connecting to database
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    
    assert len(rows) != 0       # Check if result is not equal to 0










