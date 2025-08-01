from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import json
from decimal import Decimal


app = Flask(__name__)


@app.route('/')
def start_page(name=None):
    return render_template('start_page.html')



def read_excel_file(file):
    
    file.save(file.filename)
    data = pd.read_excel(file)

    return data

def set_array_time(data):

    array_time = []
    for i in range(len(data)):

        array_time.append(data['date'].iloc[i])

    return array_time

def set_array_values(data):

    array_values = []
    for i in range(len(data)):

        array_values.append(float((data['high'].iloc[i] - data['low'].iloc[i])/2 + data['low'].iloc[i]))

    return array_values

def calculate_partial_corr(partial_array_values):
        
    index_series = []
    diminished_series = np.empty(len(partial_array_values))

    count = len(partial_array_values)+1

    for i in range(1, count):

        index_series.append(i)

        if i == 1:
            diminished_series[i-1] = partial_array_values[i]

        if i == count-1:
            diminished_series[i-1] = partial_array_values[i-1]

        if i != 1 and i != count-1:
            diminished_series[i-1] = np.nan

    ts = pd.Series(diminished_series, index=index_series)

    ts_interpolated = ts.interpolate()

    ts_interpolated = ts_interpolated.to_numpy()

    partial_corr = np.corrcoef(partial_array_values, ts_interpolated)[0,1]

    return partial_corr


def calculate_result_array(start_index, end_index, array_time, array_values):

    partial_array_values = []

    for i in range(start_index,end_index+1):
        partial_array_values.append(array_values[i])
    
    ca_start = array_time[start_index]
    ca_end = array_time[end_index]
    ca_duration = end_index-start_index+1
    ca_abs_partial_corr = round(abs(Decimal(calculate_partial_corr(partial_array_values))), 9)

    calculation_array =  [ca_start, ca_end, ca_duration, ca_abs_partial_corr]

    return calculation_array

def get_scale_table():
    
    scale_table = None
    with open('scale_table.json', 'r') as file:
        scale_table = json.load(file)

    return scale_table

def get_partial_dataframe(result_dataframe, val):

    partial_dataframe = pd.DataFrame(columns=['index', 'start_date', 'end_date', 'duration', 'abs_partial_corr'])

    for i in range(0, len(result_dataframe)):
            
        abs_partial_corr = result_dataframe['abs_partial_corr'].iloc[i]
        val_upper_value = val + 0.01

        if val_upper_value >= abs_partial_corr > val:

            new_row = { 'index':result_dataframe.index[i], 'start_date':result_dataframe['start_date'].iloc[i], 'end_date':result_dataframe['end_date'].iloc[i], 'duration':result_dataframe['duration'].iloc[i], 'abs_partial_corr':result_dataframe['abs_partial_corr'].iloc[i] }

            partial_dataframe.loc[len(partial_dataframe)] = new_row


    partial_dataframe = partial_dataframe.sort_values(by=['duration','abs_partial_corr'], ascending=False)


    return partial_dataframe


def check_availability_and_place(partial_dataframe, final_dataframe):

    for i in range(0,len(partial_dataframe)):

        result_df_abs_partial_corr = partial_dataframe['abs_partial_corr'].iloc[i]
        start_date = partial_dataframe['start_date'].iloc[i]
        duration = partial_dataframe['duration'].iloc[i]

        fine_to_set = True

        index = final_dataframe.index[final_dataframe['date']==start_date].tolist()
        index = index[0]

        for j in range(0, duration):

            value = final_dataframe['fixedness'].iloc[index+j]

            if value != 'NAN':
                fine_to_set = False
                
        if fine_to_set == True:

            for k in range(0, duration):

                final_dataframe.at[index+k,'fixedness'] = str(result_df_abs_partial_corr)

    return final_dataframe



@app.post('/view')
def view():

    file = request.files['file']
    data = read_excel_file(file)

    array_time = set_array_time(data)
    array_values = set_array_values(data)

    start_count = 0
    end_count = 2

    result_array = []

    for j in range(start_count,len(array_values)-(end_count)):

        for i in range(end_count, len(array_values)-j):

            result_array.append(calculate_result_array(j, i+j, array_time, array_values))

    result_dataframe = pd.DataFrame(result_array, columns=['start_date', 'end_date', 'duration', 'abs_partial_corr'])

    result_dataframe = result_dataframe.sort_values(by=['abs_partial_corr'], ascending=False)


    scale_table = get_scale_table()
    
    final_dataframe = pd.DataFrame(array_time, columns=['date'])
    final_dataframe = final_dataframe.assign(fixedness='NAN')

    for key, val in scale_table.items():
    
        partial_dataframe = get_partial_dataframe(result_dataframe, val)
        final_dataframe = check_availability_and_place(partial_dataframe, final_dataframe)


    fixedness = final_dataframe['fixedness'].values.tolist()


    fixedness_percentage = []
    
    for n in range(0,len(fixedness)):

        if fixedness[n] != 'NAN':

            fixedness_percentage.append(float(fixedness[n])*100)

        else:

            fixedness_percentage.append('NAN')


    return render_template('start_page.html', labels=array_time, median_price=array_values, fixedness=fixedness_percentage)



if __name__ == '__main__':
    app.run(debug=True)



