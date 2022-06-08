import logging
import re
import jsonstat
from data_model.main_logger import logger
from data_model.jsonutil import JsonUtil as util
from urllib.request import urlopen
import json
import os
from pathlib import Path

import time
import signal

class UrlBuilder:

    @staticmethod
    # Checks if the input URL works correctly
    def check_input(input_url, input_str):
        logger.info("UrlBuilder || Executing module [check_input]")
        flag_url = False
        json_data = None
        try:
            response = urlopen(input_url)
            json_data = json.loads(response.read())
            if json_data is not None:
                print("URL " + input_str + " working")
                logger.info("UrlBuilder || URL " + input_str + " working")
                flag_url = True

        except Exception as e:
            exception_message = 'UrlBuilder || Module [check_input], URL ' + input_str + " not working" + str(e)
            logger.debug(exception_message)
            print("URL " + input_str + " not working")

        return flag_url, json_data

    @staticmethod
    # Checks if there's a nult parameter in the config file and if it matches the allowed format
    def check_nult(nult):
        logger.info("UrlBuilder || Executing module [check_nult]")
        flag_nult = False
        if nult == '':
            logger.debug("UrlBuilder || No nult parameter")
            print("no nult")
        else:
            if util.check_int(nult):
                logger.info("UrlBuilder || Nult parameter valid, format: integer")
                print("nult valid")
                flag_nult = True
            else:
                logger.debug("UrlBuilder || Nult format invalid")
                print("nult invalid")
        return flag_nult

    # Checks if there's a date parameter in the config file and if it matches the allowed formats
    def check_date(date):
        logger.info("UrlBuilder || Executing module [check_date]")
        flag_date = False
        if date == '':
            logger.debug("UrlBuilder || Module [check_date], No date parameter")
            print("no date")
        else:
            base_pattern = r"[0-9]{4}[0-1]{1}[0-9]{1}[0-3]{1}[0-9]{1}"
            pattern1 = r"\b" + base_pattern + r"\Z"
            matcher1 = re.compile(pattern1)
            pattern2 = r"\b" + base_pattern + r"[:]" + base_pattern + r"\Z"
            matcher2 = re.compile(pattern2)
            pattern3 = r"\b" + base_pattern + r"(&" + base_pattern + r")+" + r"\Z"
            matcher3 = re.compile(pattern3)

            if matcher3.match(date):
                logger.info("UrlBuilder || Date parameter valid, format: YYYYMMDD&YYYYMMDD")
                print("Format YYYYMMDD&YYYYMMDD")
                flag_date = True
            elif matcher2.match(date):
                logger.info("UrlBuilder || Date parameter valid, format: YYYYMMDD:YYYYMMDD")
                print("Format YYYYMMDD:YYYYMMDD")
                flag_date = True
            elif matcher1.match(date):
                logger.info("UrlBuilder || Date parameter valid, format: YYYYMMDD")
                print("Format YYYYMMDD")
                flag_date = True
            else:
                exception_message = 'UrlBuilder || Module [check_date], Date parameter format invalid'
                logger.debug(exception_message)
                print("Format invalid")
        return flag_date

    @staticmethod
    # Builds the URL for retrieving the JSON based on the config file parameters
    def build_url2(target, language, date: str = None, nult: int = None):
        logger.info("UrlBuilder2 || Executing module [build_url]")
        base_url = "https://servicios.ine.es/wstempus/jsstat/"
        data_type = "DATASET"
        flag_extraparams = False

        # URL base building
        unparameterized_url = base_url + language + "/" + data_type + "/" + target
        print("Unparametrized is;",unparameterized_url)
        url = unparameterized_url
        flag_working = True

        if date is not None:
            flag_extraparams = True
            url = url + "?date=" + date

        if nult is not None:
            flag_extraparams = True
            if type(nult) is int:
                nult= str(nult)
            url = url + "?nult=" + nult

        if flag_extraparams:
            flag_working, json_data = UrlBuilder.check_input(url, "parameterized")
            info_message = "The URL is: " + url
            logger.info(info_message)
            print(url)

            if not flag_working:
                logger.debug("UrlBuilder || Retrying url with forcefully unparameterized url")
                flag_working, json_data = UrlBuilder.check_input(unparameterized_url, "forcefully unparameterized")
                info_message = "The URL is: " + url
                logger.info(info_message)
                if flag_working:
                    logger.debug("UrlBuilder || Error in parameter, forcing unparameterized url")
                if not flag_working:
                    logger.debug("UrlBuilder || Error in url basic definition")

        if not flag_extraparams:
            flag_working = UrlBuilder.check_input(unparameterized_url, "unparameterized")
            info_message = "UrlBuilder || The URL is: " + unparameterized_url
            logger.info(info_message)
            url = unparameterized_url
            if flag_working:
                logger.info("UrlBuilder || Basic URL definition successful")
            if not flag_working:
                logger.debug("UrlBuilder || Error in url basic definition")

        if flag_working:
            file_name = util.file_name_builder(target, language, date, nult)
            UrlBuilder.create_cache_file(json_data, file_name)
            #get path of cache folder in parrent directory
            cache_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "cache"))
            path = cache_path + "/" + file_name + ".json"
            json_stat_data = jsonstat.from_file(path)
        return flag_working, json_stat_data

    @staticmethod
    def create_cache_file(json_data, file_name):
        if not os.path.exists("cache"):
            os.makedirs("cache")
        with open('cache/' + file_name +'.json', 'w') as outfile:
            json.dump(json_data, outfile, indent=4)

    @staticmethod
    # Builds the URL for retrieving the JSON based on the config file parameters
    def build_url(yaml_data):
        logger.info("UrlBuilder || Executing module [build_url]")
        base_url = "https://servicios.ine.es/wstempus/jsstat/"
        data_type = "DATASET"
        flag_extraparams = False

        language, input_table, nult, date = util.read_yaml_parameters(yaml_data)

        # URL base building
        unparameterized_url = base_url + language + "/" + data_type + "/" + input_table
        url = unparameterized_url
        flag_working = True

        if UrlBuilder.check_nult(nult):
            flag_extraparams = True
            url = url + "?nult=" + nult

        if UrlBuilder.check_date(date):
            flag_extraparams = True
            url = url + "?date=" + date

        if flag_extraparams:
            flag_working = UrlBuilder.check_input(url, "parameterized")
            info_message = "The URL is: " + url
            logger.info(info_message)
            print(url)

            if not flag_working:
                logger.debug("UrlBuilder || Retrying url with forcefully unparameterized url")
                flag_working = UrlBuilder.check_input(unparameterized_url, "forcefully unparameterized")
                info_message = "The URL is: " + url
                logger.info(info_message)
                if flag_working:
                    logger.debug("UrlBuilder || Error in parameter, forcing unparameterized url")
                if not flag_working:
                    logger.debug("UrlBuilder || Error in url basic definition")

        if not flag_extraparams:
            flag_working = UrlBuilder.check_input(unparameterized_url, "unparameterized")
            info_message = "UrlBuilder || The URL is: " + unparameterized_url
            logger.info(info_message)
            url = unparameterized_url
            if flag_working:
                logger.info("UrlBuilder || Basic URL definition successful")
            if not flag_working:
                logger.debug("UrlBuilder || Error in url basic definition")


        return flag_working, url