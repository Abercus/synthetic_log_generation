"""
This file describes testing scenarios
"""
from common import create_xes_log, generate_activity_names, generate_trace_names, TimestampGenerator, LogGenerator
from random import shuffle

"""
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
"""





class SingleActivityScenario:

    @staticmethod
    def single_activity_missing_1():
        """
        One activity missing causes the traces to be deviant
        :return:
        """
        return None


    @staticmethod
    def single_activity_extra_1():
        """
        Addition of one activity causes the trace to be deviant
        :return:
        """
        log = LogGenerator()

        activity_count = 15
        nr_non_deviant = 100
        nr_deviant = 100


        activity_names = generate_activity_names(activity_count)
        trace_names = generate_trace_names(nr_deviant + nr_non_deviant)

        added_in_deviant = activity_names[5] # remove event with activity name

        for i in range(nr_non_deviant + nr_deviant): #
            trace = {}
            trace["deviant"] = i >= nr_non_deviant
            trace["name"] = trace_names[i]
            events = []
            timestamp_generator = TimestampGenerator()

            for j in range(activity_count):
                # dont add activity in non-deviant cases
                if not trace["deviant"] and activity_names[j] == added_in_deviant:
                    continue
                event = {}
                event["org:resource"] = "todo"
                event["lifecycle:transition"] = "COMPLETE"
                event["concept:name"] = activity_names[j]
                events.append(event)

            # shuffle events
            shuffle(events)
            # add timestamsp
            for event in events:
                event["timestamp"] = timestamp_generator.get_next_timestamp().astimezone().isoformat()

            trace["events"] = events

            log.add_trace(trace)


        return log.convert_to_xes()




class ActivitySetScenario:

    @staticmethod
    def activity_set_extra_1():
        """
        A set of activities occurring together causes the trace to be deviant
        :return:
        """
        return None


class SequenceScenario:

    @staticmethod
    def sequence_extra_1():
        return None