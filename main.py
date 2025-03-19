from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from requests_oauthlib import OAuth2Session
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
from config import Config
import os
import uvicorn

app = FastAPI()
config = Config()

# Temporary storage (Replace with DB in production)
oauth_tokens = {}

app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/build/index.html")

@app.get("/")
def home():
    return {"message": "Business Analytics API Running"}

@app.get("/quickbooks/login")
def quickbooks_login():
    """ Step 1: Redirect user to QuickBooks authorization page """
    oauth = OAuth2Session(config.quickbooks_client_id, redirect_uri=config.quickbooks_redirect_uri, scope=config.scope)
    authorization_url, state = oauth.authorization_url("https://appcenter.intuit.com/connect/oauth2")

    # Store state (use database in production)
    oauth_tokens["state"] = state

    return RedirectResponse(url=authorization_url)

@app.get("/quickbooks/callback")
def quickbooks_callback(request: Request, code: str, state: str, realmId: str):
    """ Step 2: Handle QuickBooks OAuth2 callback """

    # Verify state
    if state != oauth_tokens.get("state"):
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    oauth = OAuth2Session(config.quickbooks_client_id, redirect_uri=config.quickbooks_redirect_uri)

    # Exchange code for tokens
    try:
        token_data = oauth.fetch_token(
            config.quickbooks_token_url,
            client_secret=config.quickbooks_client_secret,
            code=code
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch token: {str(e)}")

    # Store tokens securely (replace with database storage)
    oauth_tokens["access_token"] = token_data["access_token"]
    oauth_tokens["refresh_token"] = token_data["refresh_token"]
    oauth_tokens["realm_id"] = realmId

    return RedirectResponse(url="https://strat-tips.onrender.com/")
@app.get("/quickbooks/refresh")
def refresh_access_token():
    """ Refresh expired QuickBooks tokens """
    refresh_token = oauth_tokens.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=400, detail="No refresh token available")

    oauth = OAuth2Session(config.quickbooks_client_id)

    try:
        new_token = oauth.refresh_token(
            config.quickbooks_token_url,
            refresh_token=refresh_token,
            client_id=config.quickbooks_client_id,
            client_secret=config.quickbooks_client_secret
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token refresh failed: {str(e)}")

    # Update stored tokens
    oauth_tokens["access_token"] = new_token["access_token"]
    oauth_tokens["refresh_token"] = new_token["refresh_token"]

    return {"message": "Token refreshed successfully!"}

@app.get("/quickbooks/data/{endpoint}")
def get_quickbooks_data(endpoint: str):
    """ Endpoint to fetch QuickBooks data dynamically """
    access_token = oauth_tokens.get("access_token")
    realm_id = oauth_tokens.get("realm_id")

    if not access_token or not realm_id:
        raise HTTPException(status_code=403, detail="Not authorized with QuickBooks")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    base_url = f"https://quickbooks.api.intuit.com/v3/company/{realm_id}"
    response = requests.get(f"{base_url}/{endpoint}", headers=headers)

    if response.status_code != 200:
        return {"error": response.json(), "status_code": response.status_code}

    return response.json()

def main():
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    main()
