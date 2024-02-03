from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
import uvicorn
import db
import os

domain = os.environ['domain']

app = FastAPI()
db.initializeDB()


@app.get("/")
async def serve_root():
  return FileResponse("./static/index.html")


@app.post("/short")
async def post_short(url: str = Form(...)):
  shorturl = db.shortUrl(url)
  return HTMLResponse(
      f'<a href="https://{domain}/{shorturl}" target="_blank">{domain}/{shorturl}</a>'
  )


@app.get("/{shorturl}")
async def redirect(shorturl: str):
  longurl = db.retriveURL(shorturl)
  print(longurl)
  if longurl: return RedirectResponse(url=longurl)
  else:
    raise HTTPException(status_code=404, detail="URL not found")


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
