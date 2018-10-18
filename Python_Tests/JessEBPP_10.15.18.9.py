#!/usr/bin/env python3
from datetime import datetime
import sys
temp_unix = "temp.txt"
temp = "E:/EBPP_Shared/files/temp.txt"
file = "E:/EBPP_Shared/files/ebd_relMay-2018.txt"
WD = {}
# https://pynative.com/python-mysql-update-data/
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

linenum = 0  # startingnum to see break point
with open(temp_unix, encoding="utf8") as f:
    for line in f:
        RL = line.rstrip().split('\t')
        Ccode = RL[17]  # County Code
        spname = RL[4]  # species name
        obs_ct = RL[8]  # obs count
        obs_dt = RL[27]  # obs date
        try:  # evaluating obs count value - make sure it is a number
            obs_ct = int(obs_ct)
        except ValueError:
            obs_ct = 1  # if str or 'X', I know there was at least one sighting xD
        try:  # evaluating dates for %m-%d
            Ydate = datetime.strptime(obs_dt, '%Y-%m-%d')  # datetime obj with year
        except KeyError:  # if not a date, make something up
            Ydate = datetime.strptime(obs_dt, '%Y-%m-%d')
        except ValueError:
            Ydate = datetime.strptime("1100-01-01", '%Y-%m-%d')
        Mdate = str(Ydate)[5:10]  # does not contain year, just %m-%d
        try:  # establish a dict for each Ccode
            WD[Ccode]
        except KeyError:
            WD[Ccode] = {}
        try:  # establish a dict for each species in its Ccode
            WD[Ccode][spname]
        except KeyError:
            WD[Ccode][spname] = {}
        try:  # establish a dict for each date for each species in its Ccode
            WD[Ccode][spname][Mdate]
        except KeyError:
            WD[Ccode][spname][Mdate] = {}
        try:
            WD[Ccode][spname][Mdate]["sum"]
        except:
            WD[Ccode][spname][Mdate]["sum"] = 0
        try:
            WD[Ccode][spname][Mdate]["CT"]
        except:
            WD[Ccode][spname][Mdate]["CT"] = 0
        WD[Ccode][spname][Mdate]["sum"] = WD[Ccode][spname][Mdate]["sum"] + obs_ct
        WD[Ccode][spname][Mdate]["CT"] = WD[Ccode][spname][Mdate]["CT"] + 1
        running_num = WD[Ccode][spname][Mdate]["CT"] / WD[Ccode][spname][Mdate]["sum"]
        linenum += 1
        print(linenum, Ccode, spname, running_num)
try:
    conn = mysql.connector.connect(host='ebpp-1.******.rds.amazonaws.com',
                                   database='******',
                                   user='******',
                                   password='******')
except mysql.connector.Error as error:
    print("Failed to update record to database: {}".format(error))

cursor = conn.cursor(buffered=True)

for Ccode_l in WD:
    for spname_l in WD[Ccode_l]:
        for Mdata_l in WD[Ccode_l][spname_l]:
            running_num = WD[Ccode_l][spname_l][Mdata_l]["CT"] / WD[Ccode_l][spname_l][Mdata_l]["sum"]
            sql = "INSERT INTO Test_X (Ccode_l,spname_l,Mdata_l,running_num) VALUES (%s, %s, %s, %s)"
            #val = ("1", "2", "3", "4")
            val = (Ccode_l, spname, Mdata_l, running_num)
            cursor.execute(sql, val)
            conn.commit()