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
import pandas as pd
import general.df_preprocessing as dfpre
import humanfriendly
from hurry.filesize import size
SEP = "\t"

def apply(dataframe):
    dataframe = dfpre.apply(dataframe)    
    event_num = dataframe.shape[0]
    account_num = len(dataframe['ACCOUNT'].unique())
    jobs_num = len(dataframe['JOBID'].unique())
    min_time = str(dataframe['CURRENT_TIMESTAMP'].min()).split('.')[0] if '.' in str(dataframe['CURRENT_TIMESTAMP'].min()) else str(dataframe['CURRENT_TIMESTAMP'].min())
    max_time = str(dataframe['CURRENT_TIMESTAMP'].max()).split('.')[0] if '.' in str(dataframe['CURRENT_TIMESTAMP'].max()) else str(dataframe['CURRENT_TIMESTAMP'].max())
    

    slurmy_accounts = list()
    slurmy_jobs = list()
    for index, row in dataframe.iterrows():
        if '(unfulfilled)' in str(row['DEPENDENCY']) and row['DEPENDENCY'] != '(null)':
            if row['ACCOUNT'] not in slurmy_accounts:
                slurmy_accounts.append(row['ACCOUNT'])

            if row['JOBID'] not in slurmy_jobs:
                slurmy_jobs.append(row['JOBID'])
        else:
            pass

    slurmy_accounts_num = len(slurmy_accounts)
    slurmy_jobs_num = len(slurmy_jobs)

    average_cpu_usage = sum(dataframe['CPUS'].tolist()) / len(dataframe['CPUS'].tolist())

    RAM_list = list()
    for RAM in dataframe['MIN_MEMORY'].to_list():
        if RAM != 'None' and any(char.isdigit() for char in RAM) and RAM not in dataframe['PARTITION'].unique():
            num_bytes = humanfriendly.parse_size(RAM)
            RAM_list.append(num_bytes)
            
            
    average_RAM_usage = sum(RAM_list) / len(RAM_list)

    res = {
        "startTime": str(min_time),
        "endTime": str(max_time),
        "eventsNumber": str(event_num),
        "jobNumber": str(jobs_num),
        "accountNumber": str(account_num),
        "SLURMaccountsPercentage": str(round(slurmy_accounts_num/account_num, 2)),
        "SLURMaccounts": str(slurmy_accounts),
        "SLURMaccountNumber": str(slurmy_accounts_num) + " out of " + str(account_num),
        "SLURMjobssPercentage": str(round(slurmy_jobs_num/jobs_num, 2)),
        "SLURMjobNumber": str(slurmy_jobs_num) + " out of " + str(jobs_num),
        "CPUusageAvg": str(round(average_cpu_usage, 2)),
        "RAMusageAvg": str(size(round(average_RAM_usage, 2)))     
    }

    return res


if __name__ == "__main__":
    dataframe = pd.read_csv(config.logger.local_log, sep=SEP, encoding="iso-8859-1", error_bad_lines=False)
    print(apply(dataframe))