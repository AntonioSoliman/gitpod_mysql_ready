
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Animali"
)

mycursor = mydb.cursor()

sql = "INSERT INTO Mammiferi (id, Nome_Proprio, Razza, Peso , Eta ) VALUES (%s, %s, %s, %s,%s)"
val = [
  (1, "Leo", "Leone", 190, 8),
  (2, "Bella", "Cane", 25, 5),
  (3, "Mia", "Gatto", 4, 3),
  (4, "Bobby", "Orso", 300, 12),
  (5, "Ella", "Elefante", 540, 15)
]
mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")