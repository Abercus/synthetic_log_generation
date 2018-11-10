import subprocess
import os
from multiprocessing.dummy import Pool as ThreadPool, Lock
import time
import atexit

JAR_NAME = "GoSwift.jar"  # Jar file to run
OUTPUT_FOLDER = "outputlogs/"  # Where to put output files
INPUT_FOLDER = "logs/"  # Where input logs are located

## All parameters to run the program with.

## Usually uses all input_params on all logs. So len(input_logs) * len(input_params) runs

input_logs = ["activity_set_co_occur.xes", "single_extra_1.xes", "single_missing_1.xes"]
input_params = [
    (
        "--coverageThreshold 5 --featureType Individual --minimumSupport 0.1 --encodingType Frequency", "Individual"),
    (
        "--coverageThreshold 5 --featureType Sequence --minimumSupport 0.1 --patternType MRA --encodingType Frequency",
        "Sequence_MRA"),
    (
        "--coverageThreshold 5 --featureType Sequence --minimumSupport 0.1 --patternType MR --encodingType Frequency",
        "Sequence_MR"),
    (
        "--coverageThreshold 5 --featureType Sequence --minimumSupport 0.1 --patternType TRA --encodingType Frequency",
        "Sequence_TRA"
    ),
    (
        "--coverageThreshold 5 --featureType Sequence --minimumSupport 0.1 --patternType TR --encodingType Frequency",
        "Sequence_TR"
    ),
  #  (
  #      "--coverageThreshold 5 --featureType Set --minimumSupport 0.1 --encodingType Frequency --setThreshold 0.1",
  #      "Set"
  #  ),

]


def create_output_filename(input_log, name):
    """
    Create output json file name corresponding to the trial parameters
    :param input_log: input log filenae
    :param name: name of the trial
    :return:
    """
    prefix = input_log
    if (input_log.endswith(".xes")):
        prefix = prefix[:prefix.find(".xes")]

    filename = prefix + "_" + name + ".json"

    return filename

def create_call_params(paramString, inputFile=None, outputFile=None):
    params = paramString.split()

    if outputFile:
        params.append("--outputFile")
        params.append(OUTPUT_FOLDER + outputFile)
    if inputFile:
        params.append("--logFile")
        params.append(INPUT_FOLDER + inputFile)

    return params


lock = Lock()


def call_params(paramString, inputFile, outputFile):
    """
    Function to call java subprocess
    TODO: Send sigkill when host process (this one dies) to also kill the subprocess calls
    :param paramString:
    :param inputFile:
    :return:
    """

    with lock:
        print("Started working on {}".format(inputFile))
    parameters = create_call_params(paramString, inputFile, outputFile)

    print(parameters)
    subprocess.call(['java', '-jar', JAR_NAME] + parameters, stdout=FNULL,
                    stderr=open("errorlogs/error_" + inputFile, "w"))  # blocking
    with lock:
        print("Done with {}".format(str(parameters)))


# True if parallel, false if not.
PARALLEL = False

if __name__ == "__main__":
    FNULL = open(os.devnull, 'w')  # To write output to devnull, we dont care about it
    if PARALLEL:
        pass # need to solve writing intermediate results into different files, currently there are accesses to same files
   #     # Work in parallel, 4 workers in pool
   #     pool = ThreadPool(4)
   #     ## Share work with pool workers
   #     results = pool.starmap(call_params, PARAMETERS)
   #     pool.close()
   #     pool.join()
    else:
        for inputFile in input_logs:
            for paramString, name in input_params:
                outputFilename = create_output_filename(inputFile, name)
                tic = time.time()
                call_params(paramString, inputFile, outputFilename)
                toc = time.time()
                print("Time taken {0:.3f} seconds".format(toc - tic))
    # Print list of errors.
