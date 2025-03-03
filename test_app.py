# ------------------- Imports --------------------

import io
import unittest
import textwrap
from unittest.mock import patch

from app import (
    rotate_left, rotate_right, move_forward, is_valid_coordinates, is_valid_commands,
    Car, Simulation, create_simulation, add_car, restart_program, exit_program, main
)


# ---------- Tests for Helper Functions ----------

class TestHelperFunctions(unittest.TestCase):

    def test_rotate_left(self):
        self.assertEqual(rotate_left("N"), "W")
        self.assertEqual(rotate_left("W"), "S")

    def test_rotate_right(self):
        self.assertEqual(rotate_right("N"), "E")
        self.assertEqual(rotate_right("E"), "S")

    def test_move_forward(self):
        self.assertEqual(move_forward(1, 1, "N", 5, 5), (1, 2))
        self.assertEqual(move_forward(0, 0, "S", 5, 5), (0, 0))

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
        self.car = Car("A", 1, 2, "N", "FFRFFFFRRL")
    
    def test_execute_command(self):
        self.car.execute_command("L", 5, 5)
        self.assertEqual(self.car.direction, "W")
        self.car.execute_command("F", 5, 5)
        self.assertEqual((self.car.x, self.car.y), (0, 2))
    
    def test_car_details(self):
        self.assertIn("A", self.car.car_details())
        self.assertEqual(self.car.car_details(True), f"Car Name: {self.car.name} - Position: ({self.car.x}, {self.car.y}) - Direction: {self.car.direction} - Commands: {''.join(self.car.commands)}")
        self.assertEqual(self.car.car_details(), f"Car Name: {self.car.name} - Position: ({self.car.x}, {self.car.y}) - Direction: {self.car.direction}")

class TestSimulation(unittest.TestCase):

    def setUp(self):
        self.sim = Simulation(5, 5)
    
    def test_add_car(self):
        self.sim.add_car("A", 1, 2, "N", "FFRFFFFRRL")
        self.assertEqual(len(self.sim.cars), 1)
    
    def test_reset(self):
        self.sim.add_car("A", 1, 2, "N", "FFRFFFFRRL")
        self.sim.reset()
        self.assertEqual(len(self.sim.cars), 0)
    
    # def test_run(self):
    #     result = self.sim.run()
    #     self.assertFalse(result)
    #     self.sim.add_car("A", 1, 2, "N", "FFRFFFFRRL")
    #     result = self.sim.run()
    #     self.assertTrue(result)

# --- Integration Test for app.py for Single/Multi Cars ----

class TestIntegrationAddCar(unittest.TestCase):

    @patch("builtins.input", side_effect = ["5 5"])
    def test_create_simulation(self, mock_input):
        sim = create_simulation()
        self.assertEqual(sim.width, 5)
        self.assertEqual(sim.height, 5)
    
    @patch("builtins.input", side_effect = ["5 5", "A", "1 2 N", "FFRFFFFRRL"])
    @patch("sys.stdout", new_callable = io.StringIO)
    def test_add_car(self, mock_stdout, mock_input):
        sim = create_simulation()
        add_car(sim)

        expected_output = textwrap.dedent("""\
        You have created a field of 5 x 5.
           
        Your current list of cars are:
        - Car Name: A - Position: (1, 2) - Direction: N - Commands: FFRFFFFRRL
        """)

        self.assertEqual(len(sim.cars), 1)
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output.strip())
    
    @patch("builtins.input", side_effect = ["5 5", "4"])
    def test_main_exit(self, mock_input):
        with self.assertRaises(SystemExit):
            main()

class TestIntegrationSingleCarSimulation(unittest.TestCase):

    @patch("builtins.input", side_effect = ["A", "1 2 N", "FFRFFFFRRL"])
    @patch("sys.stdout", new_callable = io.StringIO)
    def test_single_car_run(self, mock_stdout, mock_input):
        sim = Simulation(10, 10)
        add_car(sim)
        sim.run()
        
        expected_output = textwrap.dedent("""\
        Your current list of cars are:
        - Car Name: A - Position: (1, 2) - Direction: N - Commands: FFRFFFFRRL

        Your current list of cars are:
        - Car Name: A - Position: (1, 2) - Direction: N

        After simulation, the result is:
        - A, (5, 4) S
        """)

        self.assertEqual(mock_stdout.getvalue().strip(), expected_output.strip())

class TestIntegrationMultipleCarSimulation(unittest.TestCase):

    @patch("builtins.input", side_effect = [
        "A", "1 2 N", "FFRFFFFRRL",
        "B", "7 8 W", "FFLFFFFFFF",
        ])
    @patch("sys.stdout", new_callable = io.StringIO)
    def test_two_car_collision_run(self, mock_stdout, mock_input):
        self.maxDiff = None
        sim = Simulation(10, 10)
        add_car(sim)
        add_car(sim)
        sim.run()
        
        expected_output = textwrap.dedent("""\
        Your current list of cars are:
        - Car Name: A - Position: (1, 2) - Direction: N - Commands: FFRFFFFRRL
                                          
        Your current list of cars are:
        - Car Name: A - Position: (1, 2) - Direction: N - Commands: FFRFFFFRRL
        - Car Name: B - Position: (7, 8) - Direction: W - Commands: FFLFFFFFFF

        Your current list of cars are:
        - Car Name: A - Position: (1, 2) - Direction: N
        - Car Name: B - Position: (7, 8) - Direction: W

        After simulation, the result is:
        - B, collides with A at (5, 4) at step 7.
        - A, collides with B at (5, 4) at step 7.
        """)

        self.assertEqual(mock_stdout.getvalue().strip(), expected_output.strip())

    @patch("builtins.input", side_effect = [
        "A", "1 2 N", "FFRFFFFRRL",
        "B", "7 8 W", "FFLFFFFFFF",
        "C", "5 4 N", "LRLR",
        "D", "0 0 N", "FFF",
        ])
    @patch("sys.stdout", new_callable = io.StringIO)
    def test_four_car_collision_and_success_run(self, mock_stdout, mock_input):
        self.maxDiff = None
        sim = Simulation(10, 10)
        add_car(sim)
        add_car(sim)
        add_car(sim)
        add_car(sim)
        sim.run()
        
        expected_output = textwrap.dedent("""\
        Your current list of cars are:
        - Car Name: A - Position: (1, 2) - Direction: N - Commands: FFRFFFFRRL
                                          
        Your current list of cars are:
        - Car Name: A - Position: (1, 2) - Direction: N - Commands: FFRFFFFRRL
        - Car Name: B - Position: (7, 8) - Direction: W - Commands: FFLFFFFFFF
                                          
        Your current list of cars are:
        - Car Name: A - Position: (1, 2) - Direction: N - Commands: FFRFFFFRRL
        - Car Name: B - Position: (7, 8) - Direction: W - Commands: FFLFFFFFFF
        - Car Name: C - Position: (5, 4) - Direction: N - Commands: LRLR
                                          
        Your current list of cars are:
        - Car Name: A - Position: (1, 2) - Direction: N - Commands: FFRFFFFRRL
        - Car Name: B - Position: (7, 8) - Direction: W - Commands: FFLFFFFFFF
        - Car Name: C - Position: (5, 4) - Direction: N - Commands: LRLR
        - Car Name: D - Position: (0, 0) - Direction: N - Commands: FFF

        Your current list of cars are:
        - Car Name: A - Position: (1, 2) - Direction: N
        - Car Name: B - Position: (7, 8) - Direction: W
        - Car Name: C - Position: (5, 4) - Direction: N
        - Car Name: D - Position: (0, 0) - Direction: N

        After simulation, the result is:
        - A, collides with C at (5, 4) at step 7.
        - C, collides with A at (5, 4) at step 7.
        - B, collides with C, A at (5, 4) at step 7.
        - C, A, collides with B at (5, 4) at step 7.
        - D, (0, 3) N
        """)

        self.assertEqual(mock_stdout.getvalue().strip(), expected_output.strip())

if __name__ == "__main__":
    unittest.main()
