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
    traces = [[{"concept:name" : e, "org:resource" : "actor"} for e in events_list] 
            for events_list, _ in events_lists]


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
                xes.Attribute(type="string", key="org:resource", value=event["org:resource"]),
            xes.Attribute(type="string", key="lifecycle:transition", value=event["lifecycle:transition"])
            ]
            t.add_event(e)
        log.add_trace(t)

    open("example.xes", "w").write(str(log))


def gen_xes_log_dev(events_lists):
    traces = [([{"concept:name" : e, "org:resource" : str(d), "lifecycle:transition" : "complete"} for e in events_list], d) for events_list, d in events_lists]

    startTime = datetime.datetime.now(datetime.timezone.utc)

    log = xes.Log()
    for i, (trace, deviance) in enumerate(traces):
        currentTime = startTime
        t = gen_trace(trace, deviance)

        t.add_attribute(xes.Attribute(type="string", key="concept:name", value="trace_" + str(i)))
        log.add_trace(t)
            
    log.add_global_event_attribute(xes.Attribute(type="date", key="time:timestamp", value=startTime.astimezone().isoformat()))

    open("multi.xes", "w").write(str(log))




"""
Real basic log generation
"""

def gen_trace(trace, deviant):
    startTime = datetime.datetime.now(datetime.timezone.utc)

    currentTime = startTime
    t = xes.Trace()
    for i, event in enumerate(trace):
        if (i == len(trace)-1):
            if deviant:
                currentTime = startTime + datetime.timedelta(minutes = 150)
            else:
                currentTime = startTime + datetime.timedelta(minutes = 10)

        e = xes.Event()
        e.attributes = [
            xes.Attribute(type="date",   key="time:timestamp", value=currentTime.astimezone().isoformat()),
            xes.Attribute(type="string", key="concept:name", value=event["concept:name"]),
            xes.Attribute(type="string", key="org:resource", value=event["org:resource"]),
            xes.Attribute(type="string", key="lifecycle:transition", value=event["lifecycle:transition"])
        ]
        t.add_event(e)

    return t



def generate_alphabet(length=20):
    return ["activity_" + str(i+1) for i in range(length)]



def gen_set_deviance_mining_log(activities_count=20):
    # process is deviant if there are several activities included, each activity takes 2x the time then
    alphabet = generate_alphabet(activities_count)

    deviant = alphabet[:]
    random.shuffle(deviant)

    # pick a set of activities
    causes = random.sample(deviant, 3)

    inp_logs = []
    
    # remove the cause from non-deviant trace
    non_deviant = [x for x in deviant if x not in causes]
    
    # non deviant even when only one missing
    for c in causes:
        for _ in range(6):
            inp_logs.append(([x for x in deviant if x != c], False))     
     
    for _ in range(10):
        inp_logs.append((non_deviant, False))

    for _ in range(3):
        inp_logs.append((deviant, True))


    gen_xes_log_dev(inp_logs)


def gen_multiple_log(activities_count=20):
    # process is deviant if there are several activities included, each activity takes 2x the time then
    alphabet = generate_alphabet(activities_count)

    deviant = alphabet[:]
    random.shuffle(deviant)

    # pick a set of activities
    causes = random.sample(deviant, 3)

    inp_logs = []
    print(causes) 
    # remove the cause from non-deviant trace
    
    for _ in range(2000):
        # pick one cause and remove it
        cause = random.choice(causes)
        inp_logs.append(([x for x in deviant if x != cause], False))

    for _ in range(40):
        inp_logs.append((deviant, True))


    random.shuffle(inp_logs)
    gen_xes_log_dev(inp_logs)


def gen_deviance_mining_log(activities_count=20):
    # Generates xes logs for deviance mining research purposes
    alphabet = generate_alphabet(activities_count)
    
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
        inp_logs.append((non_deviant, False))

    # 2 deviant
    for _ in range(2):
        inp_logs.append((deviant, True))



    gen_xes_log(inp_logs, random_act)    



def generate_synthetic_log(activities=None):
    pass


def main():
    # TODO: read from console
    #   generate_synthetic_log(bpmn_model_1)
    #gen_deviance_mining_log()
    #gen_set_deviance_mining_log()
    gen_multiple_log()

if __name__ == "__main__":
    main()


