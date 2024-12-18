import os
import sys

import videojungle

if os.environ.get("VJ_API_KEY"):
    VJ_API_KEY = os.environ.get("VJ_API_KEY")
else:
    try:
        VJ_API_KEY = sys.argv[1]
    except Exception:
        VJ_API_KEY = None

if VJ_API_KEY is None:
    raise Exception("API key not found")
