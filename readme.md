## Fragmented Stationaryness Analyser
This python app, takes an .xlsx file as formed in sample-data.xlsx, calculates and ranks the most stationary parts of median value along with the whole time series data, plots and prints the result on a flask page. Please refer to [project tracking page](https://dogansahin-git.github.io/project-tracking-page) for screenshots and details.

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
open a browser and give the adress 127.0.0.1:5000 to run the app
<br/>
### Extra adjustments
- Please leave default scale_table.json file as it is, if you are using the app for the first time.
  Check to adjust scale_table.json for narrower or wider stationaryness measure splits. Wider intervals will cause less number of partials but longer fixedness result chucks in time series.
  Here is one helper script to adjust intervals.
```
python3 adjust_scale_table.py
```
- under **def view():** there are two variables defined as ***start_count = 0*** and ***end_count = 2***
  this sets the minimum fixedness calculation range. The range can't be less than 3 to constitute a linear like line with possible variation. However it can be adjusted to a longer fixedness result chucks in time series.
