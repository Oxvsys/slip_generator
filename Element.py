html_content = '''
<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body style="margin:0;font-family:sans-serif;">
    <img src="data:image/png;base64, {0}"/>
    {1}
    </body>
'''

element_format = '<{0} id="{1}" style="position: absolute; top: {2}px; left: {3}px;background: red; margin:0;width:{4}px;height:{5}px; line-height: {5}px; font-size:{6}px;outline:{7}px solid black; padding-top: {8}px;padding-bottom: {8}px;padding-left: {9}px">Hello</{0}>\n'

padding_percent_height = 10
padding_percent_width = 1

class Element:
    tag = 'p'
    coordinates = {}
    id = ''

    def __init__(self, element_id, coords):
        self.id = element_id
        self.coordinates = coords

    def __str__(self):
        width = self.coordinates['x2'] - self.coordinates['x1']
        height = self.coordinates['y2'] - self.coordinates['y1']
        border = 1 if self.coordinates['border'] else 0

        offset_height = height * padding_percent_height / 100
        final_height = height - (2*offset_height)
        font_size = final_height * 0.8

        offset_width = width * padding_percent_width /100
        final_width = width - offset_width

        return element_format.format(self.tag, self.id, self.coordinates['y1'], self.coordinates['x1'], final_width, final_height,font_size,border,offset_height,offset_width)
