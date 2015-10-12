import csv, sqlite3, os, encodings
import time, glob, zipfile
import pandas

datapath = "D:\\LocalDev\\maude2sqlite\\rawdata\\"
dbpath = "D:/LocalDev/maude2sqlite/db/"
unzipdata = False

def main():

    db = dbpath + "maudedata.sqlite"

    #remove our old file
    print('Deleting DB ' + db)
    try:
        os.remove(db)
    except OSError:
        pass

    #create our new file
    print('Create new DB ' + db)
    conn = sqlite3.connect(db)

    #list of zip file naming schemes and
    #the associated table that the data will be loaded into
    tablelist = [["deviceproblemcodes", "deviceproblemcodes"],
                 ["foidevproblem", "foidevproblem"],
                 ["foitext[0-9][0-9][0-9][0-9]", "foitext"],
                 ["foidev[0-9][0-9][0-9][0-9]", "foidev"],
                 ["mdrfoiThru2014", "mdrfoi"],
                 ["patientThru2014", "patient"]
                ]

    #create tables and load data
    for table in tablelist:
        loadData(conn, table[0], table[1])

    #close our db
    print('Close DB')
    conn.close()

def loadData(conn, filename, table):
    print(time.strftime("%Y-%m-%d %H:%M") + ' - Create table ' + table)

    #open our create table file and run it
    f = open(datapath + table + ".tbl")
    curs = conn.cursor()
    curs.execute(f.read())

    #get a list of our columns from our newly created table
    curs = conn.execute('select * from ' + table + ' limit 0')
    columnnames = list(map(lambda x: x[0], curs.description))
    #print(columnnames)
    conn.commit()
    f.close()

    #load data from file into our table
    print('Load data into ' + table)

    #get any files that match our style so we can
    #include all the year based files
    if unzipdata:
        ziplisting = glob.glob(datapath + filename + ".zip")
        for f in ziplisting:
            unzip(f, datapath)

    datalisting = glob.glob(datapath + filename + ".txt")

    #for any data file that matches our naming scheme,
    #use pandas to load it into our table
    for f in datalisting:
        print(f)
        inputfile = pandas.read_csv(f,
                                    sep="|",
                                    header=None,
                                    names=columnnames,
                                    error_bad_lines=False,
                                    warn_bad_lines=True,
                                    quoting=csv.QUOTE_NONE,
                                    encoding="cp1252"
                                   )
        inputfile.to_sql(table, conn, if_exists='append', index=False)
        conn.commit();
        print(time.strftime("%Y-%m-%d %H:%M") + ' - End load data ' + f)

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)

if __name__ == '__main__':
    main()