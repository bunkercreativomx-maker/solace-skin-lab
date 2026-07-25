import os
import subprocess
from pathlib import Path
from hermes_cli.config import load_env

root = Path('/opt/data/solace-skin-lab')
credentials = load_env()
token = credentials.get('GITHUB_PERSONAL_ACCESS_TOKEN') or credentials.get('GITHUB_TOKEN')
if not token:
    raise SystemExit('No GitHub token available in Hermes environment')
env = os.environ.copy()
env['GITHUB_PUSH_TOKEN'] = token
env['GIT_ASKPASS'] = str(root/'.git-askpass-hermes.sh')
env['GIT_TERMINAL_PROMPT'] = '0'
subprocess.run(['chmod', '700', env['GIT_ASKPASS']], check=True)
result = subprocess.run(['git', 'push', 'origin', 'main'], cwd=root, env=env)
raise SystemExit(result.returncode)
