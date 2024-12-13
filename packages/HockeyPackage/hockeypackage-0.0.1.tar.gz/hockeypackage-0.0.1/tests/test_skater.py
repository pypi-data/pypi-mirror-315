#!/usr/bin/env python
# coding: utf-8

import unittest
import pandas as pd
from unittest.mock import patch
from hockey.player.skater import Skater

class TestSkater(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Class setup for all tests"""
        print("Setting up class resources.")

    def setUp(self):
        """Set up before each test"""
        self.skater = Skater(2023)  # Example of initializing the Skater class for 2023

    def tearDown(self):
        """Teardown after each test"""
        print("Tearing down after a test.")

    @classmethod
    def tearDownClass(cls):
        """Class teardown for all tests"""
        print("Tearing down class resources.")

    def test_initialization(self):
        """Test the initialization of the Skater class"""
        self.assertEqual(self.skater.year, 2023)
        self.assertIsNone(self.skater.data)
        self.assertEqual(self.skater.filename, "skaters2023.csv")

    @patch('pkg_resources.resource_stream')
    def test_load_data_file_not_found(self, mock_resource_stream):
        """Test the load_data method when the file is not found"""
        mock_resource_stream.side_effect = FileNotFoundError
        
        # Attempt to load data with a filename that raises FileNotFoundError
        self.skater.load_data()

        # Check that the data remains None after the error
        self.assertIsNone(self.skater.data)

    def test_basic_stats_found(self):
        """Test the basic_stats method when the player data is found"""
        # Mocking player data frame
        self.skater.data = pd.DataFrame({
            'name': ['evander kane'],
            'team': ['san jose sharks'],
            'position': ['left wing'],
            'I_F_goals': [15],
            'I_F_points': [30]
        })

        with patch('builtins.print') as mock_print:
            self.skater.basic_stats('evander kane')

            # Check if the correct basic stats are printed
            mock_print.assert_any_call("Name: Evander kane")
            mock_print.assert_any_call("Goals: 15")
            mock_print.assert_any_call("Points: 30")

    def test_basic_stats_not_found(self):
        """Test the basic_stats method when the player is not found"""
        self.skater.data = pd.DataFrame({
            'name': ['evander kane'],
            'team': ['san jose sharks'],
            'position': ['left wing'],
            'I_F_goals': [15],
            'I_F_points': [30]
        })

        with patch('builtins.print') as mock_print:
            self.skater.basic_stats('connor mcdavid')

            # Check that the correct message is printed when the player is not found
            mock_print.assert_any_call("Player Connor mcdavid not found.")

    def test_advanced_stats_found(self):
        """Test the advanced_stats method when the player data is found"""
        # Mocking player data frame
        self.skater.data = pd.DataFrame({
            'name': ['evander kane'],
            'team': ['san jose sharks'],
            'position': ['left wing'],
            'onIce_corsiPercentage': [55.5],
            'I_F_xGoals': [12.5],
            'onIce_fenwickPercentage': [50.5]
        })

        with patch('builtins.print') as mock_print:
            self.skater.advanced_stats('evander kane')

            # Check if the correct advanced stats are printed
            mock_print.assert_any_call("Corsi Percentage: 55.5")
            mock_print.assert_any_call("Expected Goals: 12.5")
            mock_print.assert_any_call("Fenwick Percentage: 50.5")

    def test_advanced_stats_not_found(self):
        """Test the advanced_stats method when the player is not found"""
        self.skater.data = pd.DataFrame({
            'name': ['evander kane'],
            'team': ['san jose sharks'],
            'position': ['left wing'],
            'onIce_corsiPercentage': [55.5],
            'I_F_xGoals': [12.5],
            'onIce_fenwickPercentage': [50.5]
        })

        with patch('builtins.print') as mock_print:
            self.skater.advanced_stats('connor mcdavid')

            # Check that the correct message is printed when the player is not found
            mock_print.assert_any_call("Player Connor mcdavid not found.")

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)