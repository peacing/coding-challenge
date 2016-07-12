#! usr/bin/env python3

import networkx as nx
import statistics

class PaymentGraph(object):
    """Initialize an empty graph structure built with networkx package.

    Parameters
    ----------
    max_elapse : (default=60) time window a payment must fall within to be added to graph.

    Methods
    -------
    calculate_median_degree : returns median degree of graph
    update_graph : contains algorithm that determines when to add/remove hastags from the graph

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

    def _add_edges(self, target, actor, timestamp):
        """Adds edges to graph connecting the two parties involved in a payment.
        The timestamp is associated to the edge as an edge attribute.

        Parameters
        ----------
        target : {str} name of the payment target
        target : {str} name of the payment actor
        timestamp : {int} timestamp of payment.
        """

        self.G.add_edge(target, actor, timestamp=timestamp)
            # print("Edges: {} \n".format(self.G.edges(data=True)))

        return None

    def _update_max_timestamp(self, new_timestamp):
        """Compare incoming timestamp to previous max.
        If incoming timestamp is greater (i.e. later) than previous max,
        make it's timestamp the new maximum.

        Parameters
        ----------
        new_timestamp : {int} timestamp of incoming payment.

        Returns
        -------
        max_timestamp : {int} timestamp of the newest payment.
            (not necessarily the most recently processed one)

        Notes
        -----
        Update class instance variable {bool} new_max_time to True
        if the max_timestamp is updated. Allows for skipping to check for old
        nodes/edges if the max_timestamp was not updated.
        """

        self.new_max_time = False

        if new_timestamp > self.max_timestamp:  # if setting new max
            self.max_timestamp = new_timestamp
            self.new_max_time = True

        return self.max_timestamp

    def _check_too_old(self, timestamp):
        """Check if timestamp on payment is greater than 60 secs from max.

        Returns
        -------
        {bool} True or False
        """
        # if incoming timestamp is no greater than 60 secs from max
        if (self.max_timestamp - timestamp > self.max_elapse):
            return True
        else:
            return False

    def _remove_expired_edges(self, max_timestamp):
        """Remove edges from the graph that are greater than 60 from max timestamp.

        Parameters
        ----------
        max_timestamp : {int} timestamp of the latest payment.
            (not necessarily the most recently processed one)
        """

        timestamps = nx.get_edge_attributes(self.G, 'timestamp')

        for n, t in timestamps.items():
            if (max_timestamp - t) > self.max_elapse:
                self.G.remove_edge(n[0], n[1])

        return None

    def update_graph(self, payment):
        """Add and/or removes nodes & edges to the graph as new payments are processed.

        Parameters
        ----------
        payment : instance of VenmoPayment class

        Notes
        -----
        Algorithm to update graph works as follows:
            1) Update timestamp to latest.
            2) If timestamp is updated, look to remove old node/edges from graph.
            3) If payment is not too old, add its nodes/edges to graph.
        """
        #print("incoming payment: {} {} {}".format(payment.target, payment.actor, payment.timestamp))
        # determine if timestamp of payment is latest
        self.max_timestamp = self._update_max_timestamp(payment.timestamp)

        if self.new_max_time:
            # remove edges that fall outside the 60 second window
            self._remove_expired_edges(self.max_timestamp)

            # remove nodes with degree 0
            self.G.remove_nodes_from(nx.isolates(self.G))

        # determine if payment is older than 60 seconds of max timestamp
        too_old = self._check_too_old(payment.timestamp)

        if not too_old:

            # add nodes to graph
            self.G.add_nodes_from(list((payment.target, payment.actor)))

            # add edges to graph
            self._add_edges(payment.target, payment.actor, payment.timestamp)

        else:
            pass

        return None

    def calculate_median_degree(self,):
        """Calculate the median degree of each node in the graph.

        Returns
        -------
        median_degree : {float} truncated to 2 decimals of the median degree
            of graph. Returns 0.00 if there is no graph.
        """

        if self.G: # if graph exists

            # Get a {list} of the degree of each node in the graph
            degree_list = list(self.G.degree().values())
            # use statistics builtin method median to calculate median
            median_degree = statistics.median(degree_list)

            return "{:.2f}".format(median_degree)

        else:  # if no nodes/edges, return 0

            return "{:.2f}".format(0.00)