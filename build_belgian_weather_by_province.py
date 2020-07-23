import os
import subprocess
import locale
from datetime import datetime, timedelta
from pathlib import Path
home = str(Path.home())

locale.setlocale(locale.LC_ALL,'en_GB.UTF-8')

os.chdir(os.path.join(home, 'dev', 'github', 'OpenWeatherMap'))
os.system(os.path.join(home, 'dev', 'github', 'OpenWeatherMap', 'build_belgian_weather_by_province.sh'))


current_command="git add output*"
os.system(current_command)
print(f'{current_command} - executed')

current_command = f"git commit -m 'docs: update with Weather and UV-Index for {datetime.strftime(datetime.now()- timedelta(days=1),'%B %d, %Y')}'"
os.system(current_command)
print(f'{current_command} - executed')

current_command= 'npm run patch'
os.system(current_command)
print(f'{current_command} - executed')

current_command= 'npm run push'
os.system(current_command)
print(f'{current_command} - executed')

