
from src.process_payments import VenmoPayment
from nose.tools import ok_


class TestVenmoPayment(object):

    def test_payment(self):
        payment = VenmoPayment('Jamie-Korn', 'Jordan-Gruber', '2016-04-07T03:33:19Z')
        ok_(payment.target == 'Jamie-Korn')
        ok_(payment.actor == 'Jordan-Gruber')
        ok_(payment.timestamp == 1459999999)