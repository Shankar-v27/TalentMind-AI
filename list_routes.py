#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_server import app

print("\n=== All Registered Routes ===\n")
for route in app.routes:
    if hasattr(route, 'methods'):
        print(f"{route.methods} {route.path}")
    else:
        print(f"GET {route.path}")

print("\n=== Routes with 'rank' in path ===\n")
for route in app.routes:
    if hasattr(route, 'path') and 'rank' in route.path.lower():
        if hasattr(route, 'methods'):
            print(f"{route.methods} {route.path}")
        else:
            print(f"GET {route.path}")
