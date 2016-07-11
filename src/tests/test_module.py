#! usr/bin/env python3

from src.process_payments import VenmoPayment
from src.process_payments import parse_payment_input
from src.rolling_median import PaymentGraph

class TestVenmoPayment(object):

    def test_payment(self):
        payment = VenmoPayment('Jamie-Korn', 'Jordan-Gruber', '2016-04-07T03:33:19Z')
        assert payment.target == 'Jamie-Korn'
        assert payment.actor == 'Jordan-Gruber'
        assert payment.timestamp == 1459999999

    def test_dict_parser(self):
        payment_dict = {'target': 'Jamie-Korn', 'created_time': '2016-04-07T03:33:19Z', 'actor': 'Jordan-Gruber'}
        created_time, target, actor = parse_payment_input(payment_dict)
        assert created_time == '2016-04-07T03:33:19Z'
        assert target == 'Jamie-Korn'
        assert actor == 'Jordan-Gruber'

class TestBuildingVenmoGraph(object):

    def setUp(self):
        self.payment_graph = PaymentGraph()

    def test_building_venmo_graph(self):

        # add first payment from example, populating the graph
        self.payment_graph.update_graph(VenmoPayment('Jamie-Korn', 'Jordan-Gruber', '2016-04-07T03:33:19Z'))
        assert sorted(self.payment_graph.G.nodes()) == ['Jamie-Korn', 'Jordan-Gruber']
        assert len(self.payment_graph.G.edges()) == 1
        assert self.payment_graph.calculate_median_degree() == '1.00'

        # add second payment, adding another node and edge
        self.payment_graph.update_graph(VenmoPayment('Jamie-Korn', 'Maryann-Berry', '2016-04-07T03:33:19Z'))
        assert sorted(self.payment_graph.G.nodes()) == ['Jamie-Korn', 'Jordan-Gruber', 'Maryann-Berry']
        assert len(self.payment_graph.G.edges()) == 2
        assert self.payment_graph.calculate_median_degree() == '1.00'

        # add third example payment, now the median degree must be calculated with an even number of edges
        self.payment_graph.update_graph(VenmoPayment('Maryann-Berry', 'Ying-Mo', '2016-04-07T03:33:19Z'))
        assert sorted(self.payment_graph.G.nodes()) == ['Jamie-Korn', 'Jordan-Gruber', 'Maryann-Berry', 'Ying-Mo']
        assert len(self.payment_graph.G.edges()) == 3
        assert self.payment_graph.calculate_median_degree() == '1.50'

        # add fourth example payment, which adds a new edge but no new nodes
        self.payment_graph.update_graph(VenmoPayment('Ying-Mo', 'Jamie-Korn', '2016-04-07T03:34:18Z'))
        assert sorted(self.payment_graph.G.nodes()) == ['Jamie-Korn', 'Jordan-Gruber', 'Maryann-Berry', 'Ying-Mo']
        assert len(self.payment_graph.G.edges()) == 4
        assert self.payment_graph.calculate_median_degree() == '2.00'

        # add five example payment, which evicts the edges from the first three payemnts
        self.payment_graph.update_graph(VenmoPayment('Maddie-Franklin', 'Maryann-Berry', '2016-04-07T03:34:58Z'))
        assert sorted(self.payment_graph.G.nodes()) == ['Jamie-Korn', 'Maddie-Franklin', 'Maryann-Berry', 'Ying-Mo']
        assert len(self.payment_graph.G.edges()) == 2
        assert self.payment_graph.calculate_median_degree() == '1.00'

        # add sixth payment, which arrives out of order but still within the 60 second window
        self.payment_graph.update_graph(VenmoPayment('Ying-Mo', 'Maryann-Berry', '2016-04-07T03:34:00Z'))
        assert sorted(self.payment_graph.G.nodes()) == ['Jamie-Korn', 'Maddie-Franklin', 'Maryann-Berry', 'Ying-Mo']
        assert len(self.payment_graph.G.edges()) == 3
        assert self.payment_graph.calculate_median_degree() == '1.50'

        # add seventh payment, which is way too old and does not affect the graph
        self.payment_graph.update_graph(VenmoPayment('Rebecca-Waychunas', 'Natalie-Piserchio', '2016-04-07T03:31:18Z'))
        assert sorted(self.payment_graph.G.nodes()) == ['Jamie-Korn', 'Maddie-Franklin', 'Maryann-Berry', 'Ying-Mo']
        assert len(self.payment_graph.G.edges()) == 3
        assert self.payment_graph.calculate_median_degree() == '1.50'

        # add eighth payment, sets new window removing edge btw Maryann and Ying
        self.payment_graph.update_graph(VenmoPayment('Connor-Liebman', 'Nick-Shirreffs', '2016-04-07T03:35:02Z'))
        assert sorted(self.payment_graph.G.nodes()) == ['Connor-Liebman','Jamie-Korn', 'Maddie-Franklin',
                                                        'Maryann-Berry', 'Nick-Shirreffs', 'Ying-Mo']
        assert len(self.payment_graph.G.edges()) == 3
        assert self.payment_graph.calculate_median_degree() == '1.00'