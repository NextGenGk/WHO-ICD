from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# WHO ICD API Authentication
CLIENT_ID = os.getenv("WHO_CLIENT_ID")
CLIENT_SECRET = os.getenv("WHO_CLIENT_SECRET")
TOKEN_URL = os.getenv("WHO_TOKEN_URL")   # Confirm with WHO docs
BASE_URL = os.getenv("WHO_BASE_URL")

def get_access_token():
    """Get OAuth2 access token from WHO ICD API"""
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    try:
        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print("Error getting token:", e)
        return None

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "response_data": None})

@app.post("/", response_class=HTMLResponse)
def call_api(
    request: Request,
    endpoint: str = Form(...),
    id: str = Form(default=""),
    include: str = Form(default=""),
    releaseId: str = Form(default=""),
    q: str = Form(default=""),
    subtreesFilter: str = Form(default=""),
    chapterFilter: str = Form(default=""),
    useFlexisearch: str = Form(default="false"),
    flatResults: str = Form(default="true"),
    propertiesToBeSearched: str = Form(default=""),
    highlightingEnabled: str = Form(default="true"),
    searchText: str = Form(default=""),
    matchThreshold: str = Form(default=""),
    api_version: str = Form(...),
    accept_language: str = Form(...)
):
    access_token = get_access_token()
    if not access_token:
        return templates.TemplateResponse("form.html", {
            "request": request,
            "response_data": {"error": "Could not retrieve access token"}
        })

    headers = {
        "API-Version": api_version.strip(),
        "Accept-Language": accept_language.strip(),
        "Authorization": f"Bearer {access_token}"
    }

    url = ""
    params = {}
    data = {}

    if endpoint == "entity":
        url = f"{BASE_URL}/entity"
        if releaseId.strip():
            params["releaseId"] = releaseId.strip()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            data = {"error": str(e)}

    elif endpoint == "entity_id":
        if not id.strip():
            return templates.TemplateResponse("form.html", {
                "request": request,
                "response_data": {"error": "ID is required for /entity/{id}"}
            })
        url = f"{BASE_URL}/entity/{id.strip()}"
        if releaseId.strip():
            params["releaseId"] = releaseId.strip()
        if include.strip():
            params["include"] = include.strip()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            data = {"error": str(e)}

    elif endpoint == "entity_search_get":
        url = f"{BASE_URL}/entity/search"
        if q.strip():
            params["q"] = q.strip()
        if subtreesFilter.strip():
            params["subtreesFilter"] = subtreesFilter.strip()
        if chapterFilter.strip():
            params["chapterFilter"] = chapterFilter.strip()
        if useFlexisearch.strip():
            params["useFlexisearch"] = useFlexisearch.strip()
        if flatResults.strip():
            params["flatResults"] = flatResults.strip()
        if propertiesToBeSearched.strip():
            params["propertiesToBeSearched"] = propertiesToBeSearched.strip()
        if releaseId.strip():
            params["releaseId"] = releaseId.strip()
        if highlightingEnabled.strip():
            params["highlightingEnabled"] = highlightingEnabled.strip()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            data = {"error": str(e)}

    elif endpoint == "entity_search_post":
        url = f"{BASE_URL}/entity/search"
        if q.strip():
            data["q"] = q.strip()
        if subtreesFilter.strip():
            data["subtreesFilter"] = subtreesFilter.strip()
        if chapterFilter.strip():
            data["chapterFilter"] = chapterFilter.strip()
        if useFlexisearch.strip():
            data["useFlexisearch"] = useFlexisearch.strip()
        if flatResults.strip():
            data["flatResults"] = flatResults.strip()
        if propertiesToBeSearched.strip():
            data["propertiesToBeSearched"] = propertiesToBeSearched.strip()
        if releaseId.strip():
            data["releaseId"] = releaseId.strip()
        if highlightingEnabled.strip():
            data["highlightingEnabled"] = highlightingEnabled.strip()
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            data = {"error": str(e)}

    elif endpoint == "entity_autocode":
        url = f"{BASE_URL}/entity/autocode"
        if searchText.strip():
            params["searchText"] = searchText.strip()
        if releaseId.strip():
            params["releaseId"] = releaseId.strip()
        if subtreesFilter.strip():
            params["subtreesFilter"] = subtreesFilter.strip()
        if matchThreshold.strip():
            params["matchThreshold"] = matchThreshold.strip()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            data = {"error": str(e)}

    else:
        data = {"error": "Invalid endpoint selected"}

    return templates.TemplateResponse("form.html", {"request": request, "response_data": data})
