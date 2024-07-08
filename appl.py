from flask import Flask, request, render_template, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# Global variable to store the allocation DataFrame
global_allocation_data = None

@app.route('/', methods=['GET', 'POST'])
def main():
    global global_allocation_data
    if request.method == 'POST':
        groups_file = request.files['groups_file']
        hostels_file = request.files['hostels_file']

        groups_data = pd.read_csv(groups_file)
        hostels_data = pd.read_csv(hostels_file)

        final_allocation = room_allocation(groups_data, hostels_data)

        # Store the allocation DataFrame globally
        global_allocation_data = final_allocation

        return render_template('allocation.html', tables=[final_allocation.to_html(classes='data')])

    return render_template('index.html')

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
            # Update capacity directly in the DataFrame
            hostels_data.at[suitable_room.name, 'Capacity'] -= group['Members']

    return pd.DataFrame(allocated_rooms)

def allocate_room(group, hostels_data):
    compatible_rooms = hostels_data[(hostels_data['Gender'] == group['Gender']) & (hostels_data['Capacity'] >= group['Members'])]
    compatible_rooms = compatible_rooms.sort_values(by='Capacity')
    return compatible_rooms.iloc[0] if not compatible_rooms.empty else None

@app.route('/download_allocation', methods=['GET'])
def download_allocation():
    global global_allocation_data
    if global_allocation_data is None:
        return "No allocation data available. Please go back and upload the files first.", 400

    output_buffer = BytesIO()
    global_allocation_data.to_csv(output_buffer, index=False)
    output_buffer.seek(0)

    return send_file(output_buffer, as_attachment=True, download_name='allocated_rooms.csv', mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=True)
