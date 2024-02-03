import sqlite3
from uuid import uuid3, NAMESPACE_URL


def initializeDB():
  con = sqlite3.connect("main.db")
  cur = con.cursor()

  cur.execute('''CREATE TABLE IF NOT EXISTS urls
    (id INTEGER PRIMARY KEY AUTOINCREMENT, shortUrl TEXT, longUrl text)''')
  con.commit()
  con.close()


def shorturlExists(url: str) -> bool:
  con = sqlite3.connect("main.db")
  cur = con.cursor()

  data = cur.execute("SELECT * FROM urls WHERE shortUrl = ?",
                     (url, )).fetchall()
  if url in data:
    con.close()
    return True
  con.close()
  return False


def generateURL(url: str) -> str:
  return (''.join(str(uuid3(NAMESPACE_URL, url)).split('-'))[:8])


def shortUrl(longURL: str) -> str:
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  shortURL = generateURL(longURL)
  while shorturlExists(shortURL):
    shortURL = generateURL(longURL)
  cur.execute("INSERT INTO urls (shortUrl, longUrl) VALUES (?, ?)",
              (shortURL, longURL))
  con.commit()
  con.close()
  return shortURL


def retriveURL(shortURL: str) -> str:
  con = sqlite3.connect("main.db")
  cur = con.cursor()
  data = cur.execute("SELECT longUrl FROM urls WHERE shortUrl = ?",
                     (shortURL, )).fetchone()
  con.close()
  return data[0]
