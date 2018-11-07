"""
Main program for synthetic log generator for BPM area.

Generates .xes files

@author Joonas Puura

"""
from scenarios.simple import SingleActivityScenario

LOGS_FOLDER = "logs/"


def parse_input():
    pass


if __name__ == "__main__":
    #parse_input()

    open(LOGS_FOLDER + "single1.xes", "w").write(str(SingleActivityScenario.single_activity_extra_1()))