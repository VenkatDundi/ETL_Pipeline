# -*- coding: utf-8 -*-
# Example main.py
import argparse
import urllib.request
import pypdf
import re
import sqlite3
from fun_calls import *

def main(url):

    db = r"normanpd.db"
    stmt = "CREATE TABLE incidents (incident_time TEXT,incident_number TEXT,incident_location TEXT,nature TEXT,incident_ori TEXT);"
    query = "select nature,count(*) as Nature_Count from incidents group by nature order by Nature_Count desc,nature"

    #url = input("Enter the URL!")
    
    # Download data
    incident_data = fetchincidents(url)

    # Extract data
    incidents = extractincidents(incident_data)
	
    # Create new database
    createdb(db, stmt)
	
    # Insert data
    populatedb(db, incidents)
	
    # Print incident counts
    Sel_status(db, query)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)