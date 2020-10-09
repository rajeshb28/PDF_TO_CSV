import os
import json
import socket
import time
import tabula
from utility.logger import init_logger, log, metrics_logging
from flask_restplus import reqparse, Api, Resource, fields
import numpy as np

from middleware.filesource import FilesourceMiddleware
from flask import Flask, Response, request
from flask_cors import CORS
from etl.database.metadata import Metadata

import pandas as pd


from sqlalchemy import create_engine 

from ast import literal_eval
import csv

app = Flask(__name__, static_url_path='/static/')
app.config ['CORS_HEADERS'] ='Content-Type'
Cors = CORS(app)

api = Api(app)
init_logger()

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


filesource_parser= reqparse.RequestParser()
filesource_parser.add_argument('file_source_type', help='Application id',location='headers', required=False)

#Defining api models from documentation
model_400 = api.model('Errorresponse400', {'message':fields.String, 'errors':fields.Raw})
model_500 = api.model('Errorresponse400', {'message':fields.Integer, 'errors':fields.String})
model_health_200 =api.model('successResponse200',{'success':fields.Boolean,'status':fields.Integer})

log.info("AB-server api started Successfully")

#----------------------------------------------------------

current_cwd=os.getcwd()
UPLOAD_FOLDER = current_cwd+"\\data\\"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload',methods = ['POST'])
def upload():
    
    try :
        return_status =None
        result =None
        filename =request.args['filename']

        csv_filename =filename.split('.')[0]+".csv"
        final_file =UPLOAD_FOLDER+csv_filename
        file_type = csv_filename.split('.')[-1]
        filedata = request.data
        file_path = os.path.join(UPLOAD_FOLDER,filename)
        with open(file_path, "wb") as binary_file:
            binary_file.write(filedata)
            print(file_path)
            tabula.convert_into(file_path,final_file, output_format="csv", pages='all')
        print(final_file)
        if file_type == "csv" :
            raw_data= pd.read_csv(final_file,nrows=50)
            data =raw_data.rename(columns=raw_data.iloc[0])
            df =data.drop([0,1])
            df.columns = ['OCC' if x=='%Occ' else x for x in df.columns]
            final_data = df.loc[:,~df.columns.duplicated()]

            result= json.loads(final_data.to_json(orient="records"))
            db_Table =filename.split('.')[0]

            db = create_engine("postgres://guide_user:guide_user123@35.226.209.188:5432/guide_database")
            final_data.to_sql(db_Table, db, if_exists='replace')
            print(db_Table+" Table creaated in database")
            #db.Engine.dispose()
            
        else:
            result=json.loads(pd.read_excel(file_path,nrows=50).head(10).to_json (orient="records"))
        
        return_status=200
    except  :
        result ={}
        log.exception('Exception while uploading the file  ')
        return_status = 500
        result['status'] =0
        result['message'] = 'Internal Error has Occurred while processing the File request'
    finally:
        resp = Response(json.dumps(result) ,status = return_status, mimetype ="application/json")
        #metrics_logging(request, resp, int(round(time.time() * 100 ))start)    
    return resp

    resp = Response(json.dumps(data) ,status = return_status, mimetype ="application/json")
    print('---------------------')
    print(resp)
    return resp    
    
#----------------------------------------------------

@api.route('/file_source')
@api.expect(filesource_parser)
@api.response(200, 'Successful')
@api.response(400, 'validation Error', model_400)
@api.response(500, 'Internal processing Error', model_500)
class Filesource(Resource):
    def post(self):
        return_status = None
        result = {}
        start =int(round(time.time()*1000))

        try :
            
            log.info("api Request Initiated")
            fp = FilesourceMiddleware(filesource_parser)
            return_status, result = fp.run(request)
            log.info("__")
        except :
            result ={}
            log.exception('Exception while submitting file processing Request')
            return_status = 500
            result['status'] =0
            result['message'] = 'Internal Error has Occurred while processing the File request'
        finally:
            #resp = Response(json.dumps(result, cls=NpEncoder) ,status = return_status, mimetype ="application/json")
            resp = Response(json.dumps(result) ,status = return_status, mimetype ="application/json")
            #metrics_logging(request, resp, int(round(time.time() * 100 ))start)    
        return resp

@api.route('/workspaces')
@api.response(200, 'Successful')
@api.response(400, 'validation Error', model_400)
@api.response(500, 'Internal processing Error', model_500)
class Workspaces(Resource):
    def get(self):
        return_status = None
        result = {}
        start =int(round(time.time()*1000))        
        try :
            etl_metadata_obj=Metadata()
            id=request.args.get("id")
            data=etl_metadata_obj.select_workflows(id)

            return_status = 200
            result = {"status":"success",
                      "data":data
                       }
            log.info("__")
        except :
            result ={}
            log.exception('Exception while submitting file processing Request')
            return_status = 500
            result['status'] =0
            result['message'] = 'Internal Error has Occurred while processing the File request'
        finally:
            resp = Response(json.dumps(result), status = return_status, mimetype ="application/json") 
            del etl_metadata_obj
        return resp
    def post(self):
        return_status = None
        result = {}
        start =int(round(time.time()*1000))        
        try :
            etl_metadata_obj=Metadata()
            data=etl_metadata_obj.insert(request.json)
            return_status = 200
            result = {"status":"success",
                      "data":data
                       }
            log.info("__")
        except :
            result ={}
            log.exception('Exception while submitting file processing Request')
            return_status = 500
            result['status'] =0
            result['message'] = 'Internal Error has Occurred while processing the File request'
        finally:
            resp = Response(json.dumps(result), status = return_status, mimetype ="application/json") 
            del etl_metadata_obj
        return resp

@api.route('/download')
@api.response(200, 'Successful')
@api.response(400, 'validation Error', model_400)
@api.response(500, 'Internal processing Error', model_500)
class Downloadfiles(Resource):
    def post(self):
        return_status = None
        result = {}
        start =int(round(time.time()*1000))        
        try :
            file_name=""
            file_name=request.json["file_name"]
            columns=request.json["columns"]
            if file_name:
              download_file=file_name.split('\\')[-1]
            
            download_file=r"C:\\Users\\venkats_mandadapu\\{}".format(download_file)
            chunk_size=1000000
            reader = pd.read_csv(file_name, header=0, iterator=True)
            chunks = []
            loop = True
            while loop:
                try:
                   chunk = reader.get_chunk(chunk_size)[columns]
                   chunks.append(chunk)
                except StopIteration:
                    loop = False
                    print("Iteration is stopped")

            df_ac = pd.concat(chunks, ignore_index=True)
            df_ac.to_csv(download_file, index=False)
            return_status = 200
            result = {"status":"success",
                      "download_file":download_file
                       }
            log.info("__")
        except :
            result ={}
            log.exception('Exception while submitting file processing Request')
            return_status = 500
            result['status'] =0
            result['message'] = 'Internal Error has Occurred while processing the File request'
        finally:
            resp = Response(json.dumps(result), status = return_status, mimetype ="application/json") 
        return resp


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    log.info(port)
    log.info("runing ...")
    app.run(host = '127.0.0.1', port=port)