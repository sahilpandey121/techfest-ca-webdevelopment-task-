# techfest-ca-webdevelopment-task-
this is the webdevelopment task of Pandey sahil ajay ca id   :-CA-060414221652
There are five files i have uploded in it one is pyhton, two are html and 2 are csv which was given.
Now firstly put the htmls file in a folder name (templates) make sure the name of the folder should not change.
so now it should like  CA task folder in it there is a python file and a folder name templates. 
before running the python file make sure to install flask and pandas pip.+

Now run the python file anywhere.
you will get a ip addresses in the output and it will take you to a website 
now uplode both the csv file in it one is of group info and another is of hostel info.
now submite it and you will get the result and you can download it also.

now below is the workflow of the the main backend code


This code sets up a Flask web application to handle room allocations based on group and hostel data provided in CSV files. Here's a step-by-step explanation of how the code works:

Imports and Setup


[part1]


from flask import Flask, request, render_template, send_file
import pandas as pd
from io import BytesIO
Flask, request, render_template, and send_file are imported from the Flask package to handle web requests and responses.
pandas is imported as pd to manage data manipulation.
BytesIO is imported to handle in-memory binary streams, useful for file downloads.
python
Copy code
app = Flask(__name__)


global_allocation_data = None
A Flask application instance is created.
A global variable global_allocation_data is initialized to store the room allocation data.
Main Route
python
Copy code
@app.route('/', methods=['GET', 'POST'])
def main():
    global global_allocation_data
    if request.method == 'POST':
        groups_file = request.files['groups_file']
        hostels_file = request.files['hostels_file']

        groups_data = pd.read_csv(groups_file)
        hostels_data = pd.read_csv(hostels_file)

        final_allocation = room_allocation(groups_data, hostels_data)

        global_allocation_data = final_allocation

        return render_template('allocation.html', tables=[final_allocation.to_html(classes='data')])

    return render_template('index.html')
This route handles both GET and POST requests.
If the method is POST, the uploaded files (groups_file and hostels_file) are processed:
CSV files are read into groups_data and hostels_data DataFrames using pandas.
The room_allocation function is called to perform the room allocation.
The result (final_allocation) is stored in the global variable global_allocation_data.
The allocation.html template is rendered, displaying the allocation DataFrame as an HTML table.
If the method is GET, the index.html template is rendered, which likely contains the file upload form.
Room Allocation Function



[part2]

def room_allocation(groups_data, hostels_data):
    allocated_rooms = []

    for _, group in groups_data.iterrows():
        suitable_room = allocate_room(group, hostels_data)
        if suitable_room is not None:
            allocated_rooms.append({
                'Group ID': group['Group ID'],
                'Hostel Name': suitable_room['Hostel Name'],
                'Room Number': suitable_room['Room Number'],
                'Members Allocated': group['Members']
            })
            hostels_data.at[suitable_room.name, 'Capacity'] -= group['Members']

    return pd.DataFrame(allocated_rooms)
The room_allocation function allocates rooms to groups based on their gender and capacity requirements.
For each group in groups_data:
The allocate_room function is called to find a suitable room in hostels_data.
If a suitable room is found, an allocation record is created and appended to allocated_rooms.
The capacity of the allocated room is reduced by the number of group members.
Finally, a DataFrame containing all the allocation records is returned.
Allocate Room Function
python
Copy code
def allocate_room(group, hostels_data):
    compatible_rooms = hostels_data[(hostels_data['Gender'] == group['Gender']) & (hostels_data['Capacity'] >= group['Members'])]
    compatible_rooms = compatible_rooms.sort_values(by='Capacity')
    return compatible_rooms.iloc[0] if not compatible_rooms.empty else None
The allocate_room function finds a suitable room for a given group.
It filters hostels_data to find rooms that match the group's gender and have enough capacity.
The compatible rooms are sorted by capacity in ascending order.
The function returns the room with the smallest capacity that can accommodate the group, or None if no suitable room is found.
Download Allocation Route




[part3]


@app.route('/download_allocation', methods=['GET'])
def download_allocation():
    global global_allocation_data
    if global_allocation_data is None:
        return "No allocation data available. Please go back and upload the files first.", 400

    output_buffer = BytesIO()
    global_allocation_data.to_csv(output_buffer, index=False)
    output_buffer.seek(0)

    return send_file(output_buffer, as_attachment=True, download_name='allocated_rooms.csv', mimetype='text/csv')
This route handles the download of the allocation data.
If global_allocation_data is None, an error message is returned.
Otherwise, the allocation DataFrame is converted to CSV format and written to an in-memory binary stream (output_buffer).
The send_file function sends the stream as a downloadable file named allocated_rooms.csv.
Running the App



[part4]


if __name__ == '__main__':
    app.run(debug=True)
This code block runs the Flask application in debug mode if the script is executed directly.





