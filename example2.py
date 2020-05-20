import os
from glob import glob
from spellpy import spell
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta

if __name__ == '__main__':
    input_dir = './data'
    output_dir = './result'
    log_format = '<Date> <Time>,<Content>'
    tau = 0.5

    parser = spell.LogParser(indir=input_dir, outdir=output_dir,
                             log_format=log_format, tau=tau)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for pwd in glob(input_dir + '/testdevo.log'):
        log_name = os.path.basename(pwd)
        parser.parse(log_name)

    # let's create a dictionary to save the constant sequences parsed by Spell
    eventId_dict = {}
    eventId = pd.read_csv(output_dir + '/testdevo.log_templates.csv', usecols=['EventId'], engine='python')
    eventId = np.array(eventId)
    for i in range(len(eventId)):
        eventId_dict[eventId[i][0]] = i

    # for this dataset we group the logs for a session of 30 seconds of activity.
    # let's create a dictionary that takes as keys the sessions, and as values the sequence of the constant message that appear in that window time of 30 seconds

    sessions_dict = {}
    time = pd.read_csv(output_dir + '/testdevo.log_structured.csv', usecols=['Time'], engine='python')
    time = np.array(time)
    event = pd.read_csv(output_dir + '/testdevo.log_structured.csv', usecols=['EventId'], engine='python')
    event = np.array(event)
    FMT = '%H:%M:%S.%f'
    d = timedelta(seconds=30)
    count = 0
    key = 0
    sessions_dict[0] = [eventId_dict[event[0][0]]]  # we set as starting time that one of the first log message.
    for i in range(1, len(time)):
        tdelta = datetime.strptime(time[i][0], FMT) - datetime.strptime(time[count][0], FMT)
        if tdelta < d:
            sessions_dict[key].append(eventId_dict[event[i][0]])
        else:
            count = i
            key += 1
            sessions_dict[key] = [eventId_dict[event[i][0]]]
    with open('trainingdevo.txt', 'w') as f:
        for key in sessions_dict.keys():
            f.write("%s\n" % str(sessions_dict[key])[1:-1])
