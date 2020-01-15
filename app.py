from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug, os
import pyrebase


firebaseConfig = {
    'apiKey': "AIzaSyCuSWvHVaPJdd5iQQ1ZXQ0AjKmq8Na3wNw",
    'authDomain': "heroku-rest-3-img.firebaseapp.com",
    'databaseURL': "https://heroku-rest-3-img.firebaseio.com",
    'projectId': "heroku-rest-3-img",
    'storageBucket': "heroku-rest-3-img.appspot.com",
    'messagingSenderId': "264515374397",
    'appId': "1:264515374397:web:2627b1957dcec5bf424954",
    'measurementId': "G-BH7MSJKQKT"
  } 

app = Flask(__name__)
api = Api(app)
UPLOAD_FOLDER = 'static/img'


firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class PhotoUpload(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file',type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('name',type=str,required=True,help='cant be blank')

        data = parser.parse_args()
        name = data['name']

        if data['file'] == "":
            return {
                    'data':'',
                    'message':'No file found',
                    'status':'error'
                    }
        photo = data['file']
        # type(photo)

        if photo:
            # filename = '{}.png'.format(name)
            # photo.save(os.path.join(UPLOAD_FOLDER,filename))
            storage.child("{}.png".format(name)).put(data['file'])
            return {
                    'data':'',
                    'message':'photo uploaded',
                    'status':'success'
                    }
        return {
                'data':'',
                'message':'Something whent wrong',
                'status':'error'
                }

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',type=str,required=True,help='cant be blank')
        data = parser.parse_args()

        name = data['name']
   


        try:
            # storage.child("{}.png".format(name)).download("{}.png".format(name))
            url = storage.child("{}.png".format(name)).get_url()
            return {
                    'data':url,
                    'message':'photo recieved',
                    'status':'success'
                    }
        except:
            return {
                    'name':name,
                    'data':'',
                    'message':'Something whent wrong',
                    'status':'error'
                    }







api.add_resource(HelloWorld, '/check')
api.add_resource(PhotoUpload,'/upload')

if __name__ == '__main__':
    app.run(debug=True)