from flask import Flask, render_template, request, Blueprint, Response
from werkzeug.utils import secure_filename
import re
import subprocess
import os, sys
from os.path import dirname, abspath

if getattr(sys, 'frozen', False):
    filedir = os.path.dirname(sys.executable)
elif __file__:
    filedir = os.path.dirname(os.path.abspath(__file__))

if getattr(sys, 'frozen', False):
    basedir = os.path.dirname(os.path.dirname(sys.executable))
elif __file__:
    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(1, basedir)
import config
from flask_api import status
from server.response import *
from server.request import *
from server.error_messages import messages
import general.model_generator as mg
import pandas as pd
import base64

from PIL import Image
import PIL
import glob

discovery = Blueprint('discovery', __name__)
SEP = "\t"

@discovery.route("/discover_model", methods = ["POST", "GET"])
def discover_model():
    try:
        data = create_data(request)
        print()
        print("data: ", data)
        if not os.path.exists(config.logger.normal_log):
            return response_json({"error":  "The normal event log does not exist. First generate normal log."}, status.HTTP_406_NOT_ACCEPTABLE)
            
        dataframe = pd.read_csv(config.logger.normal_log, sep=SEP, encoding="iso-8859-1", error_bad_lines=False)

        account_names = data['account'].strip()
        account_names_array = set(item.strip() for item in account_names.split(','))
        
        for account_name in account_names_array:
            if len(account_name)>0 and account_name not in dataframe['ACCOUNT'].unique():
                return response_json({"error":  "The user "+ account_name + " not found."}, status.HTTP_404_NOT_FOUND)

        account_df = dataframe[dataframe['ACCOUNT'].isin(list(account_names_array))]

        # account_df.to_csv(os.path.join('slurm-log', str(account_names)), sep=SEP, index=False)

        account_df2 = account_df[account_df['ST'].isin(['R'])]
        if account_df2.shape[0] == 0:
            return response_json({"error":  "There is no RUNNING job for this user in the log. The model does not make sense."}, status.HTTP_406_NOT_ACCEPTABLE)

        models_info = mg.apply(account_df, account_names_array)

        cc_model_image = open(models_info['cc_model'], "rb")
        enc_cc_model = base64.b64encode(cc_model_image.read())
        dec_cc_model = enc_cc_model.decode()

        ag_model_image = open(models_info['ag_model'], "rb")
        enc_ag_model = base64.b64encode(ag_model_image.read())
        dec_ag_model = enc_ag_model.decode()

        return response_json({
            "msg":  messages["success"],
            "cc_model": dec_cc_model,
            "cc_fitness": models_info['cc_fitness'],
            "ag_model": dec_ag_model,
            "ag_fitness": models_info['ag_fitness'],
            },
        status.HTTP_200_OK)              
    except Exception as e:
        print("log-> discover_model: EXCEPTION " + " \n [" + str(e) + "]")
        return response_json({"error":  messages["server_side_error"]}, status.HTTP_500_INTERNAL_SERVER_ERROR)