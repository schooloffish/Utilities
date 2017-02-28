from flask import Flask,send_file,render_template
from encryptFiles import get_random_picture
from student import student 

app = Flask(__name__)

app.register_blueprint(student,url_prefix='/api/v1')

@app.route('/')
def hello_world():
    return 'Hello,World!'

@app.route('/image')
def get_image():
    picture_path=get_random_picture('D:\\PUA\\new')
    print(picture_path)
    return send_file(picture_path,mimetype='image/png')

@app.route('/video')
def get_video():
    return render_template('video.html')

if __name__=='__main__':
    app.run()