import base64
import uuid
import cv2
import os
import json

import copy

from Element import Element
from Element import html_content

zoom_factor = 2

required_width = 1130

events = [i for i in dir(cv2) if 'EVENT' in i]
print(events)

is_note_table_started = False

data_json = {}
note_table_json = {
    'x1':0,
    'y1':0,
    'x2':0,
    'y2':0,
    'dividers': [],
    'number_of_rows': 0
}

point_counter = -1
current_box = {
    "x1": 0,
    "y1": 0,
    "x2": 0,
    "y2": 0
}

def note_table_toggle():
    global point_counter, note_table_json, is_note_table_started
    if is_note_table_started:
        print('Note Table Stop')
        is_note_table_started = False
        note_table_json = {}
        point_counter = -1
    else:
        print('Note Table Start')
        is_note_table_started = True
        point_counter = 0



def start_toggle():
    global point_counter
    if point_counter == -1:
        print('Start')
        point_counter = 0
    else:
        print('Stop')
        point_counter = -1


def generate_note_quantity_table():
    global note_table_json

    table_start_x = note_table_json['x1']
    table_start_y = note_table_json['y1']

    table_total_height = note_table_json['y2'] - table_start_y

    number_of_rows_to_generate =  note_table_json['number_of_rows']

    element_height = table_total_height/number_of_rows_to_generate

    previous_column_x = table_start_x
    
    for column_x in note_table_json['dividers']:
        id_prefix = str(input("ID prefix:"))
        for row_count in range(number_of_rows_to_generate):

            element_start_x = previous_column_x
            element_start_y = table_start_y + (element_height * row_count)

            element_end_x = column_x
            element_end_y = table_start_y + (element_height * (row_count + 1))
            element_id = id_prefix + '_' + str(row_count + 1)
            data_json[element_id] = {
                'x1':element_start_x,
                'y1':element_start_y,
                'x2':element_end_x,
                'y2':element_end_y,
                'border':True
            }
        previous_column_x = column_x






    


def extract_json_with_filename(filename):
    global data_json
    file_location = os.path.join('data', filename)
    file = open(file_location, 'w')
    file.write(json.dumps(data_json))
    print('Data extracted to {0}'.format(file_location))


def extract_json():
    extract_json_with_filename('data.json')


def generate_html():
    global data_json, img
    element_html = ''
    for key in data_json:
        element_html += Element(key, data_json[key]).__str__()

    unique_id = str(uuid.uuid1())
    data_filename = unique_id + ".json"
    extract_json_with_filename(data_filename)
    html_file_location = os.path.join('output', unique_id + '.html')
    html_file = open(html_file_location, 'w')

    _, im_arr = cv2.imencode('.jpg', img)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes).decode()
    # print(im_b64)

    final_content = html_content.format(im_b64, element_html)
    html_file.write(final_content)

    print('HTML generated at {0}'.format(html_file_location))


key_action_map = {
    ord('S'): start_toggle,
    ord('s'): start_toggle,
    ord('d'): extract_json,
    ord('D'): extract_json,
    ord('h'): generate_html,
    ord('H'): generate_html,
    ord('n'): note_table_toggle,
    ord('N'): note_table_toggle,
    
}


def mouse_click_handler(event, x, y, flags, param):
    global current_box, data_json, point_counter, note_table_json, is_note_table_started
    if event == cv2.EVENT_LBUTTONDOWN:

        print(x, y)
        # Not started yet
        if point_counter == -1:
            print('Not Started yet,Press \'S\' to start')
            return
        

        cv2.circle(image_to_show, (x, y), 5, (255, 0, 0), -1)

        x/=zoom_factor
        y/=zoom_factor
        if(is_note_table_started):
            
            if point_counter==0:
                note_table_json["x1"] = x
                note_table_json["y1"] = y
                point_counter = 1
            elif point_counter == 1:
                note_table_json["x2"] = x
                note_table_json["y2"] = y
                point_counter = 2
            elif point_counter == 2:
                note_table_json['dividers'] = [x]
                point_counter = 3
            elif point_counter == 3:
                note_table_json['dividers'].append(x)
                note_table_json['dividers'].append(note_table_json["x2"])
                note_table_json['number_of_rows'] = int(input("Number of rows:"))
                generate_note_quantity_table()
                is_note_table_started = False
                point_counter = -1


        else:

            if point_counter == 0:
                current_box["x1"] = x
                current_box["y1"] = y
                point_counter = 1
            elif point_counter == 1:
                current_box["x2"] = x
                current_box["y2"] = y
                element_id = str(input("Element id:"))
                current_box['border'] = False
                data_json[element_id] = copy.deepcopy(current_box)
                point_counter = -1
                # current_box = {}

            
            


orig_img = cv2.imread("images/slip.png")

scale_percent = orig_img.shape[1] / required_width
final_dimensions = (int(orig_img.shape[1] / scale_percent), int(orig_img.shape[0] / scale_percent))
img = cv2.resize(orig_img, final_dimensions, interpolation=cv2.INTER_AREA)

image_to_show = cv2.resize(orig_img, (final_dimensions[0]*zoom_factor,final_dimensions[1]*zoom_factor), interpolation=cv2.INTER_AREA)

cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_click_handler)

while 1:
    cv2.imshow('image', image_to_show)
    k = cv2.waitKey(20) & 0xFF
    if k in key_action_map:
        key_action_map[k]()
    if k == 27:
        break
