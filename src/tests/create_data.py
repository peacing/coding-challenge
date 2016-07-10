#import datetime
#from src.process_payments import FormatPayment

#import networkx as nx


class TestInputFileData(object):
    """
    Class to create test data for testing input file date
    """
    def __init__(self):
        """
        actor = Jordan - Gruber, target = Jamie - Korn, created_time: 2016 - 04 - 07
        T03:33:19
        Z
        actor = Maryann - Berry, target = Jamie - Korn, created_time: 2016 - 04 - 07
        T03:33:19
        Z
        actor = Ying - Mo, target = Maryann - Berry, created_time: 2016 - 04 - 07
        T03:33:19
        Z
        actor = Jamie - Korn, target = Ying - Mo, created_time: 2016 - 04 - 07
        T03:34:18
        Z
        actor = Maryann - Berry, target = Maddie - Franklin, created_time: 2016 - 04 - 07
        T03:34:58
        Z
        actor = Maryann - Berry, target = Ying - Mo, created_time: 2016 - 04 - 07
        T03:34:00
        Z
        actor = Natalie - Piserchio, target = Rebecca - Waychunas, created_time: 2016 - 04 - 07
        T03:31:18
        Z
        actor = Nick - Shirreffs, target = Connor - Liebman, created_time: 2016 - 04 - 07
        T03:35:02
        Z
        """
        self.input_file_data = {"created_time": "2016-04-07T03:33:19Z", "target": "Jamie-Korn",
                                "actor": "Jordan-Gruber"}

        self.single_input= {"created_time": "2016-04-07T03:33:19Z", "target": "Jamie-Korn",
                                "actor": "Jordan-Gruber"}