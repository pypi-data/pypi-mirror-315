#!/usr/bin/env python
# coding: utf-8

import unittest
import pandas as pd
from unittest.mock import patch
from hockey.player.goalie import Goalie

class TestGoalie(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Class setup for all tests"""
        print("Setting up class resources.")

    def setUp(self):
        """Set up before each test"""
        self.goalie = Goalie(2023)  # Example of initializing the Goalie class for 2023

    def tearDown(self):
        """Teardown after each test"""
        print("Tearing down after a test.")

    @classmethod
    def tearDownClass(cls):
        """Class teardown for all tests"""
        print("Tearing down class resources.")

    def test_initialization(self):
        """Test the initialization of the Goalie class"""
        self.assertEqual(self.goalie.year, 2023)
        self.assertIsNone(self.goalie.data)
        self.assertEqual(self.goalie.filename, "goalies2023.csv")

    @patch('pkg_resources.resource_stream')
    def test_load_data_file_not_found(self, mock_resource_stream):
        """Test the load_data method when the file is not found"""
        mock_resource_stream.side_effect = FileNotFoundError
        
        # Attempt to load data with a filename that raises FileNotFoundError
        self.goalie.load_data()

        # Check that the data remains None after the error
        self.assertIsNone(self.goalie.data)

    def test_basic_stats_found(self):
        """Test the basic_stats method when the player data is found"""
        # Mocking player data frame
        self.goalie.data = pd.DataFrame({
            'name': ['tristan jarry'],
            'Team': ['pittsburgh penguins'],
            'W': [30],
            'GP': [50],
            'SV%': [0.910]
        })

        with patch('builtins.print') as mock_print:
            self.goalie.basic_stats('tristan jarry')

            # Check if the correct basic stats are printed
            mock_print.assert_any_call("Name: Tristan jarry")
            mock_print.assert_any_call("Wins: 30")
            mock_print.assert_any_call("Games Played: 50")
           

    def test_basic_stats_not_found(self):
        """Test the basic_stats method when the player is not found"""
        self.goalie.data = pd.DataFrame({
            'name': ['tristan jarry'],
            'Team': ['pittsburgh penguins'],
            'W': [30],
            'GP': [50],
            'SV%': [0.910]
        })

        with patch('builtins.print') as mock_print:
            self.goalie.basic_stats('carey price')

            # Check that the correct message is printed when the player is not found
            mock_print.assert_any_call("Goalie Carey price not found.")

    def test_advanced_stats_found(self):
        """Test the advanced_stats method when the player data is found"""
        # Mocking player data frame
        self.goalie.data = pd.DataFrame({
            'name': ['johnny test'],
            'Team': ['pittsburgh penguins'],
            'GAA': [2.50],
            'SV%': ['0.910'],
            'SO': [5],
            'SV': [1400]
        })

        with patch('builtins.print') as mock_print:
            self.goalie.advanced_stats('johnny test')

            # Check if the correct advanced stats are printed
            mock_print.assert_any_call("Shutouts: 5")
            mock_print.assert_any_call("Total Saves: 1400")
            mock_print.assert_any_call("Save Percentage (SV%): 0.910")

    def test_advanced_stats_not_found(self):
        """Test the advanced_stats method when the player is not found"""
        self.goalie.data = pd.DataFrame({
            'name': ['tristan jarry'],
            'Team': ['pittsburgh penguins'],
            'GAA': [2.50],
            'SV%': [0.910],
            'SO': [5],
            'SV': [1400]
        })

        with patch('builtins.print') as mock_print:
            self.goalie.advanced_stats('carey price')

            # Check that the correct message is printed when the player is not found
            mock_print.assert_any_call("Goalie Carey price not found.")

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)