"""
Common methods for creation of xes log and traces


"""

import xes
import datetime


class LogGenerator:

    def __init__(self, traces=None):
        if not traces:
            self.traces = []
        else:
            self.traces = traces

    def add_trace(self, trace):
        self.traces.append(trace)

    def convert_to_xes(self):
        log = create_xes_log()

        for trace in self.traces:
            xes_trace = create_xes_trace(trace)
            log.add_trace(xes_trace)


        return log


class TimestampGenerator:

    def __init__(self):
        self.currentTime = datetime.datetime.now(datetime.timezone.utc)


    def get_next_timestamp(self):
        return_timestamp = self.currentTime
        self.currentTime = self.currentTime + datetime.timedelta(minutes=10)
        return return_timestamp


"""
Trace consists of

a dictionary with arguments with one being a list of dictionaries

Timestamp has to be in iso format
{
"name" : name,
"deviant" : Boolean
"events" : [
    {"timestamp" : timestamp ..,
    "name" : name,
    "resource" : resource,
    "lifecycle" : lifecycle},
    {},
    {}...
    ]

}

Outputs xes.Trace class object consisting of such structure
"""
def create_xes_trace(trace_dict):
    xes_trace = xes.Trace()


    ## Add trace metadata
    trace_name = trace_dict["name"]
    deviant = trace_dict["deviant"]

    xes_trace.add_attribute(xes.Attribute(type="string", key="concept:name", value=trace_name))
    xes_trace.add_attribute(xes.Attribute(type="int", key="Label", value=str(1) if deviant else str(0)))

    ## Add events
    events = trace_dict["events"]
    for event in events:
        event_timestamp = event["timestamp"]
        event_name = event["concept:name"]
        event_resource = event["org:resource"]
        event_lifecycle = event["lifecycle:transition"]


        xes_event = xes.Event()
        xes_event.attributes = [
            xes.Attribute(type="date",   key="time:timestamp", value=event_timestamp),
            xes.Attribute(type="string", key="concept:name", value=event_name),
            xes.Attribute(type="string", key="org:resource", value=event_resource),
            xes.Attribute(type="string", key="lifecycle:transition", value=event_lifecycle)
        ]
        xes_trace.add_event(xes_event)
    return xes_trace


"""
Function to create xes log with following global attributes:
Label and Date
"""
def create_xes_log():
    xes_log = xes.Log()
    # Add log attributes
    xes_log.add_global_event_attribute(xes.Attribute(type="date", key="time:timestamp", value=datetime.datetime.now().astimezone().isoformat()))
    xes_log.add_global_trace_attributes(xes.Attribute(type="int", key="Label", value="0")) # For deviant, nondeviant case.
    return xes_log


def create_log_from_trace_dicts(traces):
    log = create_xes_log()
    for trace in traces:
        log.add_trace(create_xes_trace(trace))

    return log


def generate_activity_names(count):
    return ["activity_" + str(i + 1) for i in range(count)]

def generate_trace_names(count):
    return ["trace_" + str(i + 1) for i in range(count)]

def generate_event_timestamps(count):
    timestamps = []
    startTime = datetime.datetime.now(datetime.timezone.utc)
    timestamps.append(startTime)
    for _ in range(count-1):
        currentTime = startTime + datetime.timedelta(minutes=10)
        timestamps.append(currentTime)

    return timestamps