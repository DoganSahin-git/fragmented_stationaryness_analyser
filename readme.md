create virtual environment
python3 -m venv venv

activate virtual environment
source venv/bin/activate

install dependencies
pip install -r requirements.txt

run flask
flask --app main run

Upload excel file that is compatible with the example excel file. The script will calculate the median value and divides the time series data into fragments by stationaryness.
