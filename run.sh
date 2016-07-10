#!/usr/bin/env bash

# this is the run script for running the rolling_median calculation with a python file

# I'll execute my programs, with the input directory venmo_input and output the files in the directory venmo_output

 python ./src/process_payments.py --input_file ./venmo_input/venmo-trans.txt --output_file ./venmo_output/output.txt


