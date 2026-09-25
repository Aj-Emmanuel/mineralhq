import os
import sys
import time
import webbrowser
from threading import Thread

import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from main import app


# ---------------------------------------------------------
# Find application directory
# ---------------------------------------------------------
if getattr(sys, "frozen", False):
    # PyInstaller EXE
    BASE_DIR = sys._MEIPASS

    # In the EXE, the spec will place the frontend here
    FRONTEND_DIST = os.path.join(
        BASE_DIR,
        "mineral-id-app",
        "dist"
    )

else:
    # Running normally from mineral-api/
    BACKEND_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    # mineral-api and mineral-id-app are siblings
    PROJECT_DIR = os.path.dirname(BACKEND_DIR)

    FRONTEND_DIST = os.path.join(
        PROJECT_DIR,
        "mineral-id-app",
        "dist"
    )


FRONTEND_ASSETS = os.path.join(
    FRONTEND_DIST,
    "assets"
)


# ---------------------------------------------------------
# Remove the health-check "/" route from main.py
# ---------------------------------------------------------
app.router.routes = [
    route
    for route in app.router.routes
    if not (
        getattr(route, "path", None) == "/"
        and getattr(route, "methods", None) == {"GET"}
    )
]


# ---------------------------------------------------------
# Mount React/Vite assets
# ---------------------------------------------------------
if os.path.exists(FRONTEND_ASSETS):

    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_ASSETS),
        name="assets"
    )

else:

    print("WARNING: Frontend assets folder not found:")
    print(FRONTEND_ASSETS)


# ---------------------------------------------------------
# Serve React frontend
# ---------------------------------------------------------
@app.get("/")
async def serve_frontend():

    index_path = os.path.join(
        FRONTEND_DIST,
        "index.html"
    )

    if os.path.exists(index_path):

        return FileResponse(
            index_path,
            media_type="text/html"
        )

    return {
        "error": "Frontend not found",
        "expected_path": index_path
    }


# ---------------------------------------------------------
# Open browser
# ---------------------------------------------------------
def open_browser():

    time.sleep(2)

    webbrowser.open(
        "http://127.0.0.1:8001"
    )


# ---------------------------------------------------------
# Start application
# ---------------------------------------------------------
if __name__ == "__main__":

    print("=" * 60)
    print("       NIGERIAN MINERALS AI")
    print("=" * 60)

    print("Starting FastAPI backend...")
    print("Backend: http://127.0.0.1:8001")

    print()
    print("Checking frontend...")

    if os.path.exists(FRONTEND_DIST):

        print("Frontend: FOUND")
        print(
            f"Frontend path: {FRONTEND_DIST}"
        )

    else:

        print("WARNING: Frontend dist folder NOT FOUND")
        print(
            f"Expected: {FRONTEND_DIST}"
        )

    print()
    print("Opening browser...")

    browser_thread = Thread(
        target=open_browser,
        daemon=True
    )

    browser_thread.start()

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        reload=False
    )