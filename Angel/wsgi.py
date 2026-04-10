"""WSGI entry point for Angel Flask app.

Note: Angel code actually lives in Cove (Angel is a Cove module).
Real entry point is in ~/GrowDirect/Cove/wsgi.py.
This file provided for scaffolding reference.
"""

import os
from angel import create_app

config_name = os.environ.get("FLASK_ENV", "dev")
app = create_app(config_name)

if __name__ == "__main__":
    app.run()
