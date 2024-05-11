import psycopg2
from psycopg2.extras import RealDictCursor

try:
    conn = psycopg2.connect("host=localhost dbname=fastapi user=postgres password='bhavesh'",cursor_factory=RealDictCursor)
except Exception as e:
    print(e)


# while True:
#   try:
#       conn = psycopg2 connect(host='localhost', database='fastapi', user= 'postgres'
#               password='password123', cursor factory=RealDictCursor
        # cursor = conn.cursor()
        # print ("Database connection was succesfull!")
#         break
#   except Exception as error:
#       print ("Connecting to database failed") print("Error:",error)