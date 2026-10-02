from flask import Flask,request,jsonify
from flask_cors import CORS
import os
import sys
from src.components.chatbot import Chatbot
from src.utils import Utils, extract_text, SUPPORTED_EXTENSIONS
from src.logger import logging
from src.exception import CustomException


app= Flask(__name__)
CORS(app)

@app.route('/',methods=["GET"])
def proper():
    idle_message="User has not replied or is away kindly message them."
    try:
        logging.info(idle_message)
        chat=Chatbot()
        result=chat.generateresponse(idle_message)
        logging.info(f"Response from User {result}")
    except Exception as e:
        logging.info(str(e))
        return jsonify({"response":False,"message":str(e)}),500
    return jsonify({"response":True,"message":result})
        
        
# @app.route('/summarize',methods=['GET'])
def generate():
    response=""
    while True:
        user_message=input("Hey Interact with me I am A Chatbot")
        os.system('cls' if os.name == 'nt' else 'clear')
        if user_message=='q':
            break
        else:
            try:
                chat=Chatbot()
                logging.info(f"Chatbot initialized with user query={user_message}")
                response=chat.generateresponse(user_message)
                print(response)
                logging.info(response)
            except Exception as e:
                raise CustomException(e,sys)
                logging.info(f"{str(e)}")
        
        
            


@app.route('/data',methods=["POST"])
def index():
    data=request.get_json(silent=True)
    query=data.get('data') if data else None
    logging.info(query)
    if not query:
        return jsonify({"response":False,"message":"Missing 'data' field in request body"}),400
    try:
        chat=Chatbot()
        logging.info('Chatbot initialized')
        response=chat.generateresponse(query)
        logging.info(response)
    except Exception as e:
        logging.info(f"{str(e)}")
        return jsonify({"response":False,"message":str(e)}),500
    return jsonify({"response":True,"message":response})

@app.route('/upload',methods=["POST"])
def upload():
    file=request.files.get('file')
    if file is None or not file.filename:
        return jsonify({"response":False,"message":"No file provided (expected multipart field 'file')"}),400
    ext=os.path.splitext(file.filename)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return jsonify({"response":False,"message":f"Unsupported file type '{ext}'. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"}),400
    try:
        text=extract_text(file,ext)
        if not text.strip():
            return jsonify({"response":False,"message":"No text could be extracted from the file"}),400
        utils=Utils()
        chunks=utils.add_document(text)
        logging.info(f"Ingested {file.filename}: {chunks} chunks")
    except Exception as e:
        logging.info(str(e))
        return jsonify({"response":False,"message":str(e)}),500
    return jsonify({"response":True,"message":f"Added '{file.filename}' ({chunks} chunks) to the knowledge base. Ask me anything about it!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=5000)        
    
