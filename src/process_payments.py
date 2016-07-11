#!/usr/bin/env python3

import json
import argparse
from os import path
from calendar import timegm
from time import strptime
from rolling_median import PaymentGraph


class VenmoPayment(object):
    """ Formats tweet text to correct format to be added to the payment graph.

        timestamp : {int} timestamp of {str} "created_at" attribute of tweet
            See: http://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python

        hashtags : {set} of hashtags to be added to hashtag graph. Taken from {list}
            of hashtags from original tweet. Requires two or more hashtags per tweet,
            else is empty set.
    """

    def __init__(self, target, actor, created_time):
        """Format payment fields.

        Parameters
        ----------

        created_time : {str} of datetime information
        hashtags: {list} containing hashtags mentioned in tweet
        """
        self.timestamp = created_time.replace('T',' ').rstrip('Z')
        self.timestamp = timegm(strptime(self.timestamp, "%Y-%m-%d %H:%M:%S"))
        # no formatting/validation done to target or actor fields
        self.target = target
        self.actor = actor

def parse_payment_input(payment_dict):

    created_time = payment_dict["created_time"]
    target = payment_dict["target"]
    actor = payment_dict["actor"]

    return created_time, target, actor



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Specify input and output file path')
    parser.add_argument('-i','--input_file', help='The input txt file path')
    parser.add_argument('-o','--output_file', help='The output txt file path')
    args = parser.parse_args()

    if args.input_file: # custom input file argument specified
        input_file = args.input_file
        assert path.isfile(input_file), "Check the input file exists and try again."
        input_file_path = path.abspath(input_file)
    else: # run venmo-trans.txt file in venmo_input
        input_file_path = path.abspath(path.join('venmo_input', 'venmo-trans.txt'))

    if args.output_file:  # custom output file argument specified
        output_file = args.output_file
        assert path.isfile(output_file), "Check the output file exists and try again."
        output_file_path = path.abspath(output_file)
    else:  # run venmo-trans.txt file in venmo_input
        output_file_path = path.abspath(path.join('venmo_output', 'output.txt'))

    # open output file
    output = open(path.abspath(output_file_path), 'w')

    # initialize PaymentGraph instance (from median_degree.py)
    payment_graph = PaymentGraph()

    # read in tweets from input file
    with open(input_file_path, 'r') as input_file:
        for payment in input_file:
            #print("Processing: {}".format(payment))
            try:  # In case of an error

                payment_dict = json.loads(payment)  # load json to python dict

                # capture the created_time, target, and actor fields
                created_time, target, actor = parse_payment_input(payment_dict)

                # format payment to be added to payment graph
                new_payment = VenmoPayment(target, actor, created_time)

                # add payment to graph
                payment_graph.update_graph(new_payment)

                # calculated average degree of updated graph
                median_degree = payment_graph.calculate_median_degree()
                #print("median_degree: {}\n".format(median_degree))

                # write average degree to output txt file
                output.write("{}\n".format(median_degree))

            except Exception as e:

                pass  # just letting it go

    output.close()