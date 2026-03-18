import subprocess

def get_git_version():
    try:
        # Get the latest tag; suppress stderr to avoid 'No names found' noise when no tags exist
        tag = subprocess.check_output(
            ['git', 'describe', '--tags', '--abbrev=0'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        return tag
    except Exception:
        return "v1.0.0"
