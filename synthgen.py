#!/usr/bin/python


"""
Simple synthetic XES log generation for process mining. 
Features for generating following kind of synthetic logs:
    - Deviants
        - Based on time or other features ... Ex, choose an activity or set of activities to be missing from the log.
        - For testing different kind of algorithms, ex. Sequences, individual and sets.


Generation models:
    Markov models, (bpmn models)
"""

import xes
import random
import datetime

"""
Markov Model
It is a good way to model process flow.. We can have different models for deviant and non-deviant cases

"""

class MM:
    def __init__(self):
        pass



class MM_node:
    def __init__(self):
        pass




def gen_xes_log(events_lists, deviant):
    traces = [[{"concept:name" : e, "org:resource" : "actor"} for e in events_list] for events_list in events_lists]


    startTime = datetime.datetime.now()


    log = xes.Log()
    for trace in traces:
        currentTime = startTime
        t = xes.Trace()
        for i, event in enumerate(trace):
            if event["concept:name"] == deviant:
                currentTime += datetime.timedelta(minutes = 60)
            else:
                currentTime += datetime.timedelta(minutes = 5)

            e = xes.Event()
            e.attributes = [
                xes.Attribute(type="date",   key="time:timestamp", value=currentTime.isoformat()),
                xes.Attribute(type="string", key="concept:name", value=event["concept:name"]),
                xes.Attribute(type="string", key="org:resource", value=event["org:resource"])
            ]
            t.add_event(e)
        log.add_trace(t)
    log.classifiers = [
            xes.Classifier(name="org:resource", keys="org:resource"),
            xes.Classifier(name="concept:name", keys="concept:name")
            ]

    open("example.xes", "w").write(str(log))

"""
Real basic log generation


"""

def gen_deviance_mining_log(activities_count=20):
    # Generates xes logs for deviance mining research purposes
    alphabet = [str(i) for i in range(activities_count)]
    
    # straightforward
    deviant = alphabet[:]
    random.shuffle(deviant)

    # Pick one activity and delete it
    random_act = random.choice(deviant)
    non_deviant = deviant[:]
    non_deviant.remove(random_act)

    # therefore deviant one has this one extra activity

    # time taken by activity is 30 min, all othera activities 5 min

    inp_logs = []
    # 10 non deviant
    for _ in range(10):
        inp_logs.append(non_deviant)

    # 2 deviant
    for _ in range(2):
        inp_logs.append(deviant)



    gen_xes_log(inp_logs, random_act)    



def generate_synthetic_log(activities=None):
    pass


def main():
    # TODO: read from console
    #   generate_synthetic_log(bpmn_model_1)
    gen_deviance_mining_log()



if __name__ == "__main__":
    main()


