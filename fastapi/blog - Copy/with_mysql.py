from fastapi import FastAPI
import mysql.connector

app=FastAPI()

# Database connection settings
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "python_fastapi",
}

@app.get('/all_tables')
def show_tables():
    query='show tables;'
    try:
        #connect to database
        conn=mysql.connector.connect(**DB_CONFIG)
        cursor=conn.cursor()
        #execute the query
        cursor.execute(query)
        tables= [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return {"all tables":tables}
    except mysql.connector.Error as e:
        return {"error":str(e)}
