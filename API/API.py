from flask import Flask,jsonify
from flask_cors import *
import pymongo
from name_decoder import name_decoder,find_longest_consecutive
from flask_restful import reqparse
from config import DB_PASSWORD,DB_USERNAME
app = Flask(__name__)
CORS(app, supports_credentials=True)

client = pymongo.MongoClient('mongodb://'+DB_USERNAME+':'+DB_PASSWORD+'@ds255889.mlab.com:55889/assignment2')
db = client.assignment2
db.authenticate(DB_USERNAME, DB_PASSWORD)

collection = db.Name


@app.route('/send_name', methods=['POST'])
def received_name():


    try:
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        args = parser.parse_args()
        name = args.get("name")

        first_name, last_name = name.split(' ')
        insert_result = collection.insert_one({'first_name': first_name, 'last_name': last_name})
        # print(insert_result)
        binary_sum = name_decoder(name)
        # print(binary_sum)
        result = find_longest_consecutive(binary_sum)
        # print(result)
        return jsonify(result), 200

    except IOError:
        message = 'An error occured trying to read the input.'
        return jsonify(message=message), 500

    except ValueError:
        message = 'Wrong data type found in the input.'
        return jsonify(message=message), 500

    except ImportError:
        print("NO module found")
        message = 'system error'
        return jsonify(message=message), 500

    except EOFError:
        print('Why did you do an EOF on me?')
        message = 'system error'
        return jsonify(message=message), 500
    except KeyboardInterrupt:
        print('You cancelled the operation.')
        message = 'system error'
        return jsonify(message=message), 500
    except:
        print('An error occured.')
        message = 'system error'
        return jsonify(message=message), 500




if __name__ == '__main__':
    app.run()
