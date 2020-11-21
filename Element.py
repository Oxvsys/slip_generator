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

element_format = '<{0} id="{1}" style="position: absolute; top: {2}px; left: {3}px;background: red; margin:0;width:{4}px;height:{5}px;font-size:{5}px;outline:{6}px solid black;">Hello</{0}>\n'


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
        return element_format.format(self.tag, self.id, self.coordinates['y1'], self.coordinates['x1'], width, height,border)
