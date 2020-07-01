#/bin/sh
echo "start building the dataset: eosc-gees-weather_in_belgian_provinces_per_day.py"
source ~/miniconda3/etc/profile.d/conda.sh
conda activate pandas
python src/eosc-gees-weather_in_belgian_provinces_per_day.py

echo "finished"

echo "Next actions:"

echo "git add output*"
echo "git commit -m 'docs: update with Weather and UV-Index for June 29, 2020'"
echo "npm run patch"
echo "npm run push"