import psycopg2

 

# Open a DB session

dbSession       = psycopg2.connect("dbname='postgres' user='postgres' password='postgres'");

 

# Open a database cursor

dbCursor = dbSession.cursor();

 

# SQL statement to create a table



#sqlInsertRow1  = "CREATE TABLE NanoCat(name varchar(500));";
#
sqlInsertRow1  = "INSERT INTO NanoCat values('New York City')";
##
#dbCursor.execute(sqlInsertRow1);
 

# Insert statement


#sqlSelect = "select * from NanoCat";
##
#dbCursor.execute(sqlSelect);
##
#rows = dbCursor.fetchall();
##
## 
##
### Print rows
##
#for row in rows:
##
#    print(row);





 

# Select statement

#sqlSelect = "select * from postgres.public.'BadCat'";
#
#dbCursor.execute(sqlSelect);
#
#dbSession.commit()




#rows = dbCursor.fetchall();

 

# Print rows

#for row in rows:
#
#    print(row);
    
dbCursor.close()
dbSession.close()