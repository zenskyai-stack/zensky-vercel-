ZenSky Flask website - Render deployment

1) Upload this folder to a GitHub repo.
2) Open Render.com > New > Web Service.
3) Connect the GitHub repo.
4) Settings:
   - Language: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
5) Add environment variables if needed:
   SECRET_KEY, EMAIL_USER, EMAIL_PASSWORD, ADMIN_EMAIL, ADMIN_PASSWORD
6) Deploy. Render will give a live URL like https://your-app.onrender.com

Note:
- This app uses SQLite. On free hosting, saved contacts may reset after redeploy/restart unless you use a persistent disk or external database.
