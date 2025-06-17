#!/usr/bin/env python3
# Save this as check_config.py in your app directory

import os
import sys
from dotenv import load_dotenv

def check_config():
    """Load environment and check required variables."""
    # Load .env file
    load_dotenv()

    required_vars = ['CONFIG_NAME', 'DATABASE_URL']
    missing_vars = []

    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            missing_vars.append(var)
            print(f"❌ {var} is not set")
        else:
            if var == 'DATABASE_URL':
                print(f"✅ {var} is configured (value hidden)")
            else:
                print(f"✅ {var} = {value}")

    if missing_vars:
        print(f"❌ Missing required variables: {', '.join(missing_vars)}")
        sys.exit(1)

    print("✅ All required variables are set")

if __name__ == "__main__":
    check_config()
