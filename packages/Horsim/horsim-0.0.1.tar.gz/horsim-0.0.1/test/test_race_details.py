# test_race_details.py

import unittest
from datetime import timedelta
from datetime import datetime
from horse_race_simulator.race_data.race_details import DelayedRace

class TestRace(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Setting up resources for the entire TestRace class")
        cls.today_date = datetime.now()
        cls.today_date_str = datetime.now().strftime("%Y-%m-%d")
          
        cls.venue_names = ["Pony Speedway", "Canter Canyon", "Saddle Summit", "Dusty Lanes", "Gallop Galley", "Riders Run"]
        cls.venue_distances = [1000, 1200, 1600, 1800, 2200, 2400]
        cls.weather_conditions = ["Sunny", "Overcast", "Rainy", "Snowy"]

    @classmethod
    def tearDownClass(cls):
        print("Tearing down shared resources.")
        cls.today_date = None
        cls.today_date_str = None
        cls.venue_names = None
        cls.weather_conditions = None

    def setUp(self):
        print("Setting up testcase.")
        self.num_horses = 10
        self.race = DelayedRace(num_horses = self.num_horses)

    def tearDown(self):
        print("Tearing down testcase.")
        self.num_horses = None
        self.race = None
    
    def test_constructor(self): # To check default values
        print("Running test_constructor")
        # Check member variables during the initialization of DelayedRace
        self.assertIsNotNone(self.race.track)
        self.assertIn(self.race.venue, self.venue_names) # check if venue name is in list
        self.assertIn(self.race.distance, self.venue_distances) # check if venue distance is in list
        self.assertIn(self.race.weather, self.weather_conditions) # check if weather is in list

        current_date = (self.today_date + timedelta(days=self.race.delay_days)).strftime("%Y-%m-%d")
        self.assertEqual(self.race.date, current_date)
        self.assertGreater(self.race.prize, 4999)
        self.assertLessEqual(self.race.prize, 25000)
        self.assertEqual(self.race.num_horses, self.num_horses)
        self.assertIsNotNone(self.race.race_id)
        self.assertEqual(len(self.race.horses), self.num_horses)

        delay_days = 3
        self.assertEqual(self.race.delay_days, delay_days)

    def test_set_delayed_date(self):
        print("Running test_set_delayed_date")
        # Check values of delay_days and date before calling the set_delayed_date function
        delay_days = 3
        current_date = self.today_date + timedelta(days=delay_days)
        current_date_str = current_date.strftime("%Y-%m-%d")
        self.assertEqual(self.race.date, current_date_str)
        self.assertEqual(self.race.delay_days, delay_days)
        delay_days = 5
        self.race.delay_days = delay_days
        self.race.set_delayed_date()
        # Check values of delay_days and date after calling the set_delayed_date function
        new_date_str = (current_date + timedelta(days=(delay_days))).strftime("%Y-%m-%d")
        self.assertEqual(self.race.date, new_date_str)
        self.assertEqual(self.race.delay_days, delay_days)

    def test_set_date(self):
        print("Running test_set_date")
        # Check values before calling the function
        self.assertNotEqual(self.race.date, self.today_date_str, "It should not match today's date since set_delayed_date was called in the constructor.")
        self.race.set_date(self.today_date_str)
        # Check values after calling the function
        self.assertEqual(self.race.date, self.today_date_str)

    def test_get_race_info(self): # extra test, just making sure no exception raised when printing info
        print("Running test_get_race_info")
        self.race.get_race_info() 

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)