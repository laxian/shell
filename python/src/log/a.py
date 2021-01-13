import flask
import os
import sys
 
 
if __name__ == "__main__":
    app = flask.Flask(__name__, static_folder=sys.argv[1])
    os.system('pwd')
    app.run(host='192.168.1.5', port=5000)
    print('--------------------------------')

