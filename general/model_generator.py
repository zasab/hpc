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
import pm4py
from pm4py.visualization.petri_net import visualizer as pn_visualizer
import time

def generate_model(log, model_name, account_names_array, current_time, model_format):
    net, im, fm = pm4py.discover_petri_net_inductive(log)
    parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: model_format, "rankdir": "TB" }

    # gviz = pn_visualizer.apply(net, im, fm, log=log, parameters=parameters, variant=pn_visualizer.Variants.FREQUENCY)
    # freq_model_path = os.path.join(config.general.models_dir, '_'.join(account_names_array) +'_'+ model_name +'_freq_' + str(current_time) +'.' + model_format)
    # pn_visualizer.save(gviz, freq_model_path)
   
    gviz_perf = pn_visualizer.apply(net, im, fm, log=log, parameters=parameters, variant=pn_visualizer.Variants.PERFORMANCE)
    perf_model_path = os.path.join(config.general.models_dir, ''.join(account_names_array) + model_name +'freq' + str(current_time) +'.' + model_format)
    pn_visualizer.save(gviz_perf, perf_model_path)


    fitness_tbr = pm4py.fitness_token_based_replay(log, net, im, fm)
    # prec = pm4py.precision_token_based_replay(log, net, im, fm)
    prec = '1.0'

    return net, perf_model_path, str(fitness_tbr['average_trace_fitness']), prec

def apply(df, account_names_array):
    df = df[df['ACCOUNT'].isin(list(account_names_array))]
    current_time =  str(time.time())
    if '.' in current_time:
        current_time = current_time.split('.')[0]

    # connected_compnents
    CC_df = df[df['ST'].isin(['R'])]
    print(len(CC_df.COMMAND.unique()))
    CC_df.rename(columns={'PROCESSED_COMMAND': 'concept:name', 'CURRENT_TIMESTAMP': 'time:timestamp', 'DEPENDENCY-BASED-CASE-ID': 'case:concept:name'}, inplace=True)
    CC_dataframe = pm4py.format_dataframe(CC_df, case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')
    CC_log = pm4py.convert_to_event_log(CC_dataframe)
    CC_net , CC_model_file, CC_fitness, CC_precision = generate_model(CC_log, 'DEPENDENCY', account_names_array, current_time, "png")
    generate_model(CC_log, 'DEPENDENCY', account_names_array, current_time, "pdf")


    # account_groups
    AG_df = df[df['ST'].isin(['R'])]
    print(len(AG_df.COMMAND.unique()))
    AG_df.rename(columns={'PROCESSED_COMMAND': 'concept:name', 'CURRENT_TIMESTAMP': 'time:timestamp', 'ACCOUNT-GROUP-BASED-CASE-ID': 'case:concept:name'}, inplace=True)
    AG_dataframe = pm4py.format_dataframe(AG_df, case_id='case:concept:name', activity_key='concept:name', timestamp_key='time:timestamp')
    AG_log = pm4py.convert_to_event_log(AG_dataframe)
    AG_net , AG_model_file, AG_fitness, AG_precision = generate_model(AG_log, 'ACCOUNTGROUP', account_names_array, current_time, "png")
    generate_model(AG_log, 'ACCOUNTGROUP', account_names_array, current_time, "pdf")

    return {
        'cc_model': CC_model_file,
        'cc_net': CC_net,
        'cc_fitness': CC_fitness,
        'cc_precision': CC_precision,
        'ag_model': AG_model_file,
        'ag_net': AG_net,
        'ag_fitness': AG_fitness,
        'ag_precision': AG_precision,
    }