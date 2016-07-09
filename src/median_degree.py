#! usr/bin/ienv python3

import numpy as np
import networkx as nx
from itertools import combinations


class PaymentGraph():
    """Initialize an empty graph structure built with networkx package.

    Parameters
    ----------
    max_elapse : (default=60) time window a tweet must fall within to be added to graph.

    Methods
    -------
    calculate_average_degree : returns average degree of graph
    update_graph : algorithm that determines when to add/remove hastags from the graph

    Attributes
    ----------
    G : networkx Graph() instance
        See: https://networkx.github.io/documentation/latest/
    """

    def __init__(self, max_elapse=60):
        self.max_elapse = max_elapse
        self.max_timestamp = 0
        self.new_max_time = False
        self.G = nx.Graph()

    def _add_edges(self, hashtags, timestamp):
        """Form edges of graph from combinations of hashtags.
        Include timestamp from relevant tweet as an edge attribute.

        Parameters
        ----------
        hashtags : {set} of hashtags contained in tweet.
        timestamp : {int} timestamp of tweet.
        """

        # Since graph is undirected, combinations of hashtags is sufficient.
        # Ex: hashtags = ('A', 'B', 'C'), combinations = ('AB', 'AC', 'BC')
        for hash1, hash2 in combinations(hashtags, 2):
            self.G.add_edge(hash1, hash2, timestamp=timestamp)
            # print("Edges: {} \n".format(self.G.edges(data=True)))

        return None

    def _update_max_timestamp(self, new_timestamp):
        """Compare incoming timestamp to previous max.
        If incoming timestamp is greater (i.e. later) than previous max,
        make it's timestamp the new maximum.

        Parameters
        ----------
        new_timestamp : {int} timestamp of incoming tweet.

        Returns
        -------
        max_timestamp : {int} timestamp of the newest tweet.
            (not necessarily the most recently processed one)

        Notes
        -----
        Update class instance variable {bool} new_max_time to True
        if the max_timestamp is updated. Use to not check for old
        nodes/edges if the max_timestamp was not updated.
        """

        self.new_max_time = False

        if new_timestamp > self.max_timestamp:  # if setting new max

            self.max_timestamp = new_timestamp
            self.new_max_time = True

        return self.max_timestamp

    def _check_too_old(self, timestamp):
        """Check if timestamp on tweet is greater than 60 secs from max.

        Returns
        -------
        {bool} True or False
        """

        # if incoming timestamp is no greater than 60 secs from max
        if self.max_timestamp - timestamp > self.max_elapse:
            return True
        else:
            return False

    def _remove_expired_edges(self, max_timestamp):
        """Remove edges from the graph that are greater than 60 from max timestamp.

        Parameters
        ----------
        max_timestamp : {int} timestamp of the newest tweet.
            (not necessarily the most recently processed one)
        """

        timestamps = nx.get_edge_attributes(self.G, 'timestamp')
        # Ex: timestamps = {('Apache', 'Spark'): 1459207450, ('Spark', 'Storm'): 1459207452}
        for n, t in timestamps.items():

            if (max_timestamp - t) > self.max_elapse:
                # print("Removing edge between {}".format(n))
                self.G.remove_edge(n[0], n[1])

        return None

    def update_graph(self, tweet):
        """Add and/or removes nodes & edges to the graph as new tweets
        are processed.

        Parameters
        ----------
        tweet : instance of FormatTweet class

        Notes
        -----
        Algorithm to update graph proceeds as follows:
            1) Update timestamp to latest.
            2) If timestamp is updated, look to remove old node/edges from graph.
            3) If tweet has hashtags and is not too old, add its node/edges to graph.
        """

        print("incoming tweet: {} {}".format(tweet.hashtags, tweet.timestamp))

        # determine if timestamp of tweet is latest
        self.max_timestamp = self._update_max_timestamp(tweet.timestamp)
        # print("Max timestamp: {}".format(self.max_timestamp))

        if self.new_max_time:
            # remove edges that fall outside the 60 second window
            self._remove_expired_edges(self.max_timestamp)

            # remove nodes with degree 0
            self.G.remove_nodes_from(nx.isolates(self.G))

        if tweet.hashtags:  # if tweet contained more than 1 hashtag

            # determine if tweet is older than 60 seconds of max timestamp
            too_old = self._check_too_old(tweet.timestamp)
            # print("Too old?: {}".format(too_old))

            if not too_old:

                # add nodes to graph
                self.G.add_nodes_from(tweet.hashtags)

                # add edges to graph
                self._add_edges(tweet.hashtags, tweet.timestamp)

                # print("nodes: {}".format(self.G.nodes()))
                # print("edges: {}".format(self.G.edges()))

            else:
                pass

        else:
            pass

        return None

    def calculate_median_degree(self, ):
        """Calculate the average degree of each node in the graph.

        Returns
        -------
        average_degree : {float} truncated to 2 decimals of the average degree
            of each node. Returns 0.00 if there is no graph.
        """

        if self.G:

            # Get a {list} of the degree of each node in the graph
            degree_list = list(self.G.degree().values())

            # avg degree is sum of each node's degree / total No. of nodes
            average_degree = (sum(degree_list)) / self.G.number_of_nodes()

            return "{:.2f}".format(average_degree)

        else:  # if no nodes/edges, return 0

            return "{:.2f}".format(0.00)