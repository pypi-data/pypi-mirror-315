#!/usr/bin/env python3
"""
Command line interface to generate calibration with km3compass

Usage:
    generate_calibration --upi UPI --ellipsoid-fit CSK [--json JSON_FILE --jpp JPP_FILE --display --username USERNAME --location LOCATION]
    generate_calibration --upi UPI --dummy-calibration [--json JSON_FILE --jpp JPP_FILE --display --username USERNAME --location LOCATION]
    generate_calibration --upi UPI --inverted-X [--json JSON_FILE --jpp JPP_FILE --display --username USERNAME --location LOCATION]
    generate_calibration (-h | --help)
    generate_calibration --version

Options:
    --upi UPI             Compass UPI
    --json JSON_FILE      Output a json file in JSON_FILE 
    --jpp JPP_FILE        Output a jpp-formated file in JPP_FILE
    --display             Print the calibration in humand-readable format
    --dummy-calibration   Produce a dummy calibration
    --inverted-X          Produce a X inverted version of the latest calibration in the DB
    --ellipsoid-fit CSK   Calibration produced from an ellipsoid fit of the given CSK file
    --username USERNAME   DB username to be used for e.g. json test session production
    --location LOCATION   Location OID to be used for e.g. json test session production
    -h --help             Show this screen.

Example:
    generate_calibration --upi 3.4.3.4/AHRS/1.69
"""

from docopt import docopt
import km3compass as kc
import pandas as pd
import km3db
import numpy as np


def generate_calibration(
    compass_UPI,
    json_file=None,
    jpp_file=None,
    ellipsoid_fit=None,
    dummy_calibration=False,
    inverted_x_calibration=False,
    display=False,
    username=None,
    location=None,
):
    compass_SN = int(compass_UPI.split(".")[-1])
    calibration = None
    if dummy_calibration:
        calibration = kc.calibration_object(
            compass_UPI=compass_UPI,
            compass_SN=compass_SN,
            source=f"km3compass-{kc.version}/generate_calibration",
        )
        calibration.set("type", kc.CALIBRATION_TYPE_UNITY)

    elif inverted_x_calibration:
        calibration = kc.calibration_DB_agent().get_calibration(compass_SN)
        calibration_type = calibration.get("type")
        if calibration_type != kc.CALIBRATION_TYPE_V3:
            raise NotImplementedError(
                f"Inverted X calibration only work from {kc.CALIBRATION_TYPE_V3} ! {calibration_type} found in DB."
            )
        calibration.set("type", kc.CALIBRATION_TYPE_V3_INVERTED_X)

        H_rotation_matrix = calibration.get("H_rot")
        A_rotation_matrix = calibration.get("A_rot")
        indices_to_invert = [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)]
        for i, j in indices_to_invert:
            H_rotation_matrix[i, j] *= -1
            A_rotation_matrix[i, j] *= -1
        calibration.set("H_rot", H_rotation_matrix)
        calibration.set("A_rot", A_rotation_matrix)

    elif ellipsoid_fit:
        reader = kc.readerCSK(ellipsoid_fit)
        cal = kc.calibration_ellipsoid_fit(
            reader, compass_SN=compass_SN, compass_UPI=compass_UPI
        )
        calibration = cal.calibration
        cal.perform_checks()

    else:
        raise NotImplementedError("No mode provided.")

    if json_file:
        print(f"Export calibration to json in {json_file} ")
        calibration.to_json(
            filename=json_file,
            with_test_session=True,
            username=username,
            location=location,
        )

    if jpp_file:
        print(f"Export calibration to jpp format in {jpp_file} ")
        calibration.to_jpp(filename=jpp_file)

    if display:
        print(calibration)


def main():
    args = docopt(__doc__, version=kc.version)
    dummy_calibration = args["--dummy-calibration"]
    inverted_x_calibration = args["--inverted-X"]
    ellipsoid_fit = args["--ellipsoid-fit"]
    compass_UPI = args["--upi"]
    json_file = args["--json"]
    jpp_file = args["--jpp"]
    display = args["--display"]
    username = args["--username"]
    location = args["--location"]

    generate_calibration(
        compass_UPI,
        dummy_calibration=dummy_calibration,
        inverted_x_calibration=inverted_x_calibration,
        json_file=json_file,
        jpp_file=jpp_file,
        display=display,
        ellipsoid_fit=ellipsoid_fit,
        username=username,
        location=location,
    )


if __name__ == "__main__":
    main()
