import subprocess
import os

def get_git_version():
    # Attempt to read from environment variable set during deployment
    app_version = os.environ.get('APP_VERSION')
    if app_version and app_version != 'v1.0.0':
        return app_version
        
    try:
        # Get the latest tag locally
        tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        return tag
    except Exception:
        return app_version if app_version else "v1.0.0"

if __name__ == "__main__":
    print(get_git_version())
