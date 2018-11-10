"""
Main program for synthetic log generator for BPM area.

Generates .xes files

@author Joonas Puura

"""
from scenarios.simple import SingleActivityScenario, ActivitySetScenario

LOGS_FOLDER = "logs/"


def parse_input():
    pass


if __name__ == "__main__":
    #parse_input()
    open(LOGS_FOLDER + "single_extra_1.xes", "w").write(str(SingleActivityScenario.single_activity_extra_1()))
    open(LOGS_FOLDER + "single_missing_1.xes", "w").write(str(SingleActivityScenario.single_activity_missing_1()))
    open(LOGS_FOLDER + "activity_set_co_occur.xes", "w").write(str(ActivitySetScenario.activity_set_co_occur()))
