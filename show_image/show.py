


from flask import Flask
from flask import render_template

app = Flask(__name__)

def return_img_stream(img_local_path):

    import base64
    img_stream = ''
    with open(img_local_path, 'r') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream

@app.route('/')
def hello_world():
    img_path = '/home/mason/websiteC/0to100/workspace/static/user_icon.png'
    img_stream = return_img_stream(img_path)
    return render_template('index.html',
                           img_stream=img_stream)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
