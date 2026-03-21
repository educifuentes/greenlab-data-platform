import subprocess
import os

def get_git_version():
    # 1. Check for environment variable (most reliable in production containers)
    if "APP_VERSION" in os.environ:
        return os.environ["APP_VERSION"]
        
    # 2. Check for a hardcoded VERSION file if injected during CI/CD
    if os.path.exists("VERSION"):
        try:
            with open("VERSION", "r") as f:
                return f.read().strip()
        except:
            pass

    # 3. Fallback to local git CLI lookup
    try:
        tag = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        return tag
    except Exception:
        return "v1.0.0"
