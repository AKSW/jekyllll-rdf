#!/usr/bin/env python3
import sys
import os
import subprocess
import logging
import yaml
import math
import time
import shutil

logger = logging.getLogger('quit-eval')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
ch.setFormatter(formatter)

def setupRuns(number, destinationPath, configFile='_config.yml'):
    setup = []
    stream = open(configFile, 'r')
    data = yaml.load(stream)

    if not data['jekyll_rdf']['restriction_file']:
        raise Exception("The configuration needs to specify a restriction_file.")

    try:
        os.mkdir(destinationPath)
    except FileExistsError as e:
        pass

    with open(data['jekyll_rdf']['restriction_file'], 'r') as resourceFileStream:
        resources = list(resourceFileStream)
        numberOfResources = len(resources)
        logger.debug(numberOfResources)
        resourceSliceSize = int(math.ceil(numberOfResources/number))

        for runNumber in range(0, number):
            logger.debug(runNumber)
            runConfig = data

            runDestinationPath = os.path.join(destinationPath, 'run' + str(runNumber))
            runConfigFile = os.path.join(destinationPath, '_config' + str(runNumber) + ".yml")
            runRestrictionFile = os.path.join(destinationPath, 'resources' + str(runNumber) + ".txt")

            with open(runRestrictionFile, 'w') as outfile:
                printResources = resources[resourceSliceSize*runNumber:resourceSliceSize*(runNumber+1)]
                outfile.write("".join(printResources))
                logger.debug(printResources)

            runConfig['jekyll_rdf']['restriction_file'] = runRestrictionFile

            with open(runConfigFile, 'w') as outfile:
                yaml.dump(runConfig, outfile)
            setup.append({"destination": runDestinationPath, "config": runConfigFile})
    return setup

def runAll(setup):
    for runCfg in setup:
        runCfg["process"] = run(runCfg["destination"], runCfg["config"])
    logger.debug("started")
    for runCfg in setup:
        logger.debug(str(runCfg["process"].pid))
        while runCfg["process"].poll() is None:
            logger.debug("wait for " + str(runCfg["process"].pid))
            time.sleep(1)
    logger.debug("done")

def run(destinationDir, configFile):
    command = ["bundle", "exec", "jekyll", "build", "--config", configFile, "--destination", destinationDir]
    logger.debug(" ".join(command))
    process = subprocess.Popen(command, cwd=os.getcwd())
    return process

    # process.kill()

def collect(setup):
    sources = []
    for runCfg in setup:
        sources.append(runCfg["destination"] + "/")

    logger.debug(["rsync", "-a"] + sources + ["_multisite/"])
    shutil.rmtree('_multisite')
    process = subprocess.Popen(["rsync", "-a"] + sources + ["_multisite/"], cwd=os.getcwd())
    while process.poll() is None:
        logger.debug("wait for rsync " + str(runCfg["process"].pid))
        time.sleep(1)

if __name__ == '__main__':

    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    if (len(sys.argv) < 3):
        logger.error("You need to specify a number of threads and destinationPath")
        sys.exit(1)

    numThreads = int(sys.argv[1])
    destinationPath = sys.argv[2]
    configFile = sys.argv[3]
    if configFile == None:
        configFile = "_config.yml"
    if not destinationPath[0] == "_":
        logger.warning("The destination path '{}' does not start with an underscore '_' this can be dangerous.".format(destinationPath))
    setup = setupRuns(numThreads, destinationPath, configFile)
    logger.debug(setup)
    runAll(setup)
    collect(setup)
