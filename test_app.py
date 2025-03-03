# ------------------- Imports --------------------

import unittest
from unittest.mock import patch

from app import (
    rotate_left, rotate_right, move_forward, is_valid_coordinates, is_valid_commands,
    Car, Simulation, create_simulation, add_car, main
)


# ---------- Tests for Helper Functions ----------

class TestHelperFunctions(unittest.TestCase):

    def test_rotate_left(self):
        self.assertEqual(rotate_left('N'), 'W')
        self.assertEqual(rotate_left('W'), 'S')

    def test_rotate_right(self):
        self.assertEqual(rotate_right('N'), 'E')
        self.assertEqual(rotate_right('E'), 'S')

    def test_move_forward(self):
        self.assertEqual(move_forward(1, 1, 'N', 5, 5), (1, 2))
        self.assertEqual(move_forward(0, 0, 'S', 5, 5), (0, 0))

    def test_is_valid_coordinates(self):
        self.assertTrue(is_valid_coordinates("3", "4"))
        self.assertFalse(is_valid_coordinates("-1", "4"))
    
    def test_is_valid_commands(self):
        self.assertTrue(is_valid_commands("LRF"))
        self.assertFalse(is_valid_commands("LRFX"))
        self.assertFalse(is_valid_commands("L R F"))


# -------------- Tests for Classes ---------------

class TestCar(unittest.TestCase):

    def setUp(self):
        self.car = Car("TestCar", 1, 1, 'N', "LRF")
    
    def test_execute_command(self):
        self.car.execute_command('L', 5, 5)
        self.assertEqual(self.car.direction, 'W')
        self.car.execute_command('F', 5, 5)
        self.assertEqual((self.car.x, self.car.y), (0, 1))
    
    def test_car_details(self):
        self.assertIn("TestCar", self.car.car_details())
        self.assertEqual(self.car.car_details(True), f"Car Name: {self.car.name} - Position: ({self.car.x}, {self.car.y}) - Direction: {self.car.direction} - Commands: {"".join(self.car.commands)}")
        self.assertEqual(self.car.car_details(), f"Car Name: {self.car.name} - Position: ({self.car.x}, {self.car.y}) - Direction: {self.car.direction}")

class TestSimulation(unittest.TestCase):

    def setUp(self):
        self.sim = Simulation(5, 5)
    
    def test_add_car(self):
        self.sim.add_car("Car1", 2, 2, 'N', "LRF")
        self.assertEqual(len(self.sim.cars), 1)
    
    def test_reset(self):
        self.sim.add_car("Car1", 2, 2, 'N', "LRF")
        self.sim.reset()
        self.assertEqual(len(self.sim.cars), 0)
    
    def test_run(self):
        self.sim.add_car("Car1", 2, 2, 'N', "F")
        result = self.sim.run()
        self.assertTrue(result)

# --- Integration Test for app.py for Classes ----

class TestIntegration(unittest.TestCase):
    @patch('builtins.input', side_effect=['5 5'])
    def test_create_simulation(self, mock_input):
        sim = create_simulation()
        self.assertEqual(sim.width, 5)
        self.assertEqual(sim.height, 5)
    
    @patch('builtins.input', side_effect=['Car1', '1 1 N', 'LRF'])
    def test_add_car(self, mock_input):
        sim = Simulation(5, 5)
        add_car(sim)
        self.assertEqual(len(sim.cars), 1)
    
    @patch('builtins.input', side_effect=['5 5', '4', ''])
    def test_main_exit(self, mock_input):
        with self.assertRaises(SystemExit):
            main()

if __name__ == "__main__":
    unittest.main()
