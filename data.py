import mysql.connector


def databaseRecord(name,ans):
  config = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost',
  'port':8889,
  'database': 'assign',
  'raise_on_warnings': True,
  }

  link = mysql.connector.connect(**config)
  cursor = link.cursor(dictionary=True)
  sql = "INSERT INTO Record (name, Satisfied) VALUES (%s, %s)"
  val = (name, ans)
  cursor.execute(sql,val)
  link.commit()
  link.close()
