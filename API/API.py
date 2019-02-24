from flask import Flask,jsonify,request
from flask_cors import *
import pymongo
from name_decoder import name_decoder,find_longest_consecutive,get_human_names
from flask_restful import reqparse
from config import DB_PASSWORD,DB_USERNAME
from werkzeug.exceptions import BadRequest
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
        print(name)
        first_name, last_name = name.split(' ')

        # print(insert_result)
        binary_sum = name_decoder(name)
        # print(binary_sum)
        output = find_longest_consecutive(binary_sum)
        # print(result)
        result = {'name':name,'output':output}
        insert_result = collection.insert_one({'first_name': first_name, 'last_name': last_name})
        return jsonify(result), 200

    except IOError:
        message = 'An error occured trying to read the input.'
        return jsonify(message=message), 400

    except ValueError:
        message = 'Wrong data type found in the input.'
        return jsonify(message=message), 400

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

@app.route('/send_file', methods=['POST'])
def received_file():



    try:
        file = request.files['file']

        text = str(file.read().decode("utf-8"))

        names = get_human_names(text)
        resultlist = []
        for name in names:
            first_name, last_name = name.split(' ')
            binary_sum = name_decoder(name)
            output = find_longest_consecutive(binary_sum)
            result = {'name': name, 'output': output}
            resultlist.append(result)
            insert_result = collection.insert_one({'first_name': first_name, 'last_name': last_name})

        return jsonify({'data':resultlist}), 200
    except IOError:
        message = 'An error occured trying to read the input.'
        return jsonify(message=message), 400

    except ValueError:
        message = 'Wrong data type found in the input.'
        return jsonify(message=message), 400

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
