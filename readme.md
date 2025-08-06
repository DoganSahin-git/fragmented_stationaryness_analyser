##Fragmented Stationaryness Analyser

This python app,takes an .xlsx file as formed in sample-data.xlsx, calculates and ranks the most stationary parts of median value along with the whole time series data, plots and prints the result on a flask page.

create virtual environment
```
python3 -m venv venv
```
activate virtual environment
```
source venv/bin/activate
```
install dependencies
```
pip install -r requirements.txt
```
run flask
```
flask --app main run
```

leave default scale_table.json file as it is, if you are using the app for the first time
check adjust scale_table.json for narrower or wider stationaryness measure splits
wider intervals will cause less number of partials but longer result chucks in time. 
here is one helper script to adjust intervals
```
python3 adjust_scale_table.py
```

