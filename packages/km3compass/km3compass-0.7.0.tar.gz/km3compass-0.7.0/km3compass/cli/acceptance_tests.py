#!/usr/bin/env python3
"""
Command line tool to perform acceptance-test evaluation of compass.
The input file can contains multiple DOMs.

Usage:
    compass_accepTest FILENAME [-d]
    compass_accepTest FILENAME --self-calib [-d]
    compass_accepTest FILENAME --json-calib JSON_FILE [-d]
    compass_accepTest (-h | --help)
    compass_accepTest --version

Options:
    FILENAME                CSK file containing the compass data
    --self-calib            Toggle self calibration, using sphere fit, instead of
                            reading DB
    --json-calib JSON_FILE  Use calibration provided in JSON_FILE
    -d                      Toggle debug information plots
    -h --help               Show this screen.

"""

from docopt import docopt
import km3compass as kc
import matplotlib.pyplot as plt
import pandas as pd


def compass_accepTest(
    filename="", debug=False, self_calibration=False, json_calib=None
):
    reader = kc.readerCSK(filename)
    results = None
    df = None
    if debug:
        kc.plot_raw_results(reader.df, title="Raw data")

    for modID in reader.module_IDs:
        print("-" * 10 + " Process module {} ".format(modID) + "-" * 10)
        calib = None
        if self_calibration:
            calib = kc.calib_self_sphere(reader, modID)
            if debug:
                calib.plot_results()

        elif json_calib:
            calibration = kc.calibration_object.from_json(json_calib)
            calib = kc.calibration_module(
                reader, modID, calibration, fill_information_from_DB=False
            )

        else:
            calib = kc.calib_DB(reader, modID)

        if debug:
            calib.print_calibration()

        try:
            accept = kc.acceptance_test(calib, modID)
            accept.plot_results()
            df = pd.concat((df, accept.df))
            results = pd.concat(
                (results, pd.DataFrame(accept.residuals, index=[modID]))
            )
        except Exception as E:
            print(E)
            print("Continue to next module")
        print()

    if debug:
        kc.plot_raw_results(df, title="After calibration and weight aligment")
    print("-" * 10 + " Summary " + "-" * 10)
    print(results.set_index("module ID"))


def cli_compass_accepTest():
    args = docopt(__doc__, version=kc.version)
    filename = args["FILENAME"]
    debug = args["-d"]
    self_calibration = args["--self-calib"]
    json_calib = args["--json-calib"]
    compass_accepTest(
        filename, debug, self_calibration=self_calibration, json_calib=json_calib
    )
    plt.show()
