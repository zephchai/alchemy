#!/usr/bin/env python
"""
Alchemy system is a tool to load the different configuration files for the
softwares. This allows different sites, projects, and others the flexibility
to have their own settings.
Alchemy system reads configuration file in hierarchical way and overwrites
the variables along the way.
If the value of a variable is a dictionary, the value in the dictionary
will be updated instead of replaced. LIMITATION: One level down only!
ALL the config files should be named in this manner.
<tool>.all.<project>.<sequence>.<shot>.json
<tool>.<site>.<project>.<sequence>.<shot>.json
<tool>.<dept>.<project>.<sequence>.<shot>.json
<tool>.<user>.<project>.<sequence>.<shot>.json

"""

__author__ = "zeph"
__date__ = "2016/04/17"
__version__ = "0.1.0"

import os
import sys
import logging
import json
import re

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


def _setup_logger(func):
    """ Decorator to set up the logger for this module
    """
    def wrapper(*args, **kwargs):
        # Logging setup
        global logger
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logger.addHandler(NullHandler())
        return func(*args, **kwargs)
    return wrapper

class Alchemist(object):
    def __init__(self):
        module_dir = os.path.dirname(__file__)
        configFile = os.path.join(module_dir, "config.json")
        with open(configFile, "r") as f:
            self.config = json.load(f)

    def load(self, tool):
        """ Main loading function. Use this to load config file
            ARGS: 
                tool(string): name of the tool config
            RETURN: 
                (dictionary): key and value in the config file
        """
        config_files = self._get_files(tool)

        if len(config_files) == 0:
            print('WARNING: No json config found for ' + tool)
            return {}

        result = {}
        # load json files
        for config in config_files:
            with open(config) as f:
                data = json.load(f)

                # Cannot simply update. Value that are dictionary
                # should be updated instead of replace
                for key, val in data.items():
                    if type(val) == dict and key in result:
                        result[key].update(val)
                    else:
                        result[key] = val
        return result


    def _get_files(self, tool):
        """ Use the path variable to find all the config file
            ARG: 
                tool: name of the tool's config to load
            RETURN: 
                (list): json files
        """
        result = [] 
        configFolder = os.path.join(self.config["alc_path"], tool)
        # add the most basic json file
        result.append(os.path.join(configFolder, tool+".json"))

        for pattern in self.config["load_pattern"]:
            filePath = os.path.join(configFolder, os.path.expandvars(pattern))
            if os.path.exists(filePath):
                result.append(filePath)
        
        return result

"""
@_setup_logger
def load(tool):
    ''' Main loading function. Use this to load config file
        RETURN: dictionary of variables and values
        ARG: tool - name of the tool
    '''
    if not os.getenv('ALC_PATH'):
        print('CRITICAL ERROR: Environment variable ALC_PATH is not set. \
            Please set it to the conf folder')
        return

    jsons = _get_files(tool)

    if len(jsons) == 0:
        print('WARNING: No json config found for ' + tool)
        logger.warn('No json config found for ' + tool)
        return {}

    logger.debug('Starting loading of config file')
    result = {}
    # load json files
    for json_file in jsons:
        with open(json_file) as f:
            data = json.load(f)
            logger.debug('Values in ' + json_file)
            logger.debug(data)
            # Cannot simply update. Value that are dictionary
            # should be updated instead of replace
            for key, val in data.items():
                if type(val) == dict and key in result:
                    result[key].update(val)
                else:
                    result[key] = val
    return result


@_setup_logger
def load_env(tool):
    ''' Load the "env" key in the config file.
        Variables in different files will not be overwritten as opposed to
        the load() function above. It will be called sequentially.
        keyword marked with $, for eg. $SOME_VAR will be replaced by existing
        env variable.
        The env variable in the json file should be a list of list with the
        inner list containing 2 strings, env variable name and value.
        eg. env: [["env1", "some string value"], ["env2", "another value"]]
        RETURN: NULL
        ARG: tool - name of the tool
    '''
    if not os.getenv('ALC_PATH'):
        print('CRITICAL ERROR: Environment variable ALC_PATH is not set. \
            Please set it to the conf folder')
        return

    jsons = _get_files(tool)

    if len(jsons) == 0:
        print('WARNING: No json config found for ' + tool)
        logger.warn('No json config found for ' + tool)
        return {}

    logger.debug('Starting loading of config file')
    result = {}
    # load json files
    for json_file in jsons:
        with open(json_file) as f:
            data = json.load(f)
            envs = data.get("env", [])
            logger.debug('Env variables in ' + json_file)
            logger.debug(envs)
            for env in envs:
                os.environ[env[0]] = os.path.expandvars(env[1]).replace(
                    '/', os.sep)
"""
