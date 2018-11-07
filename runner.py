import subprocess
import os
from multiprocessing.dummy import Pool as ThreadPool, Lock


JAR_NAME = "GoSwift.jar" # Jar file to run
OUTPUT_FOLDER = "output/" # Where to put output files


## All parameters to run the program with
PARAMETERS = [
    ("--coverageThreshold 5 --featureType Individual --minimumSupport 0.1 --encodingType Frequency --logFile logs/single1.xes --setThreshold 0.1", "individual_simple_1.json"),
   # ("--coverageThreshold 5 --featureType Set --minimumSupport 0.1 --encodingType Frequency --logFile logs/single1.xes --setThreshold 0.1", "set_simple_1.json"), # Really slow!
    ("--coverageThreshold 5 --featureType Sequence --minimumSupport 0.1 --patternType MRA --encodingType Frequency --logFile logs/single1.xes", "sequence_MRA_simple_1.json"),
    ("--coverageThreshold 5 --featureType Sequence --minimumSupport 0.1 --patternType MR --encodingType Frequency --logFile logs/single1.xes", "sequence_MR_simple_1.json"),
    ("--coverageThreshold 5 --featureType Sequence --minimumSupport 0.1 --patternType TRA --encodingType Frequency --logFile logs/single1.xes", "sequence TRA_simple_1.json"),
    ("--coverageThreshold 5 --featureType Sequence --minimumSupport 0.1 --patternType TR --encodingType Frequency --logFile logs/single1.xes", "sequence_TR_simple_1.json"),

]

def create_call_params(paramString, outputFile=None):
    params = paramString.split()
    if outputFile:
        params.append("--output")
        params.append(OUTPUT_FOLDER + outputFile)
    return params


lock = Lock()


def call_params(paramString, file):
    """
    Function to call java subprocess
    :param paramString:
    :param file:
    :return:
    """
    with lock:
        print("Started working on {}".format(file))
    parameters = create_call_params(paramString, file)
    subprocess.call(['java', '-jar', JAR_NAME] + parameters, stdout=FNULL, stderr=open("error_" + file, "w"))  # blocking
    with lock:
        print("Done with {}".format(file))

if __name__ == "__main__":

    FNULL = open(os.devnull, 'w') # To write output to devnull, we dont care about it

    # Work in parallel, 4 workers in pool
    pool = ThreadPool(4)

    ## Share work with pool workers
    results = pool.starmap(call_params, PARAMETERS)

    pool.close()
    pool.join()