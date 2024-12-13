#!/usr/bin/env python
# coding: utf-8

import unittest
import pandas as pd
from unittest.mock import patch
from hockey.player.player import Player

class TestPlayer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Class setup for all tests"""
        print("Setting up class resources.")
    
    def setUp(self):
        """Set up before each test"""
        self.player = Player(2023)  #set up with example year 

    def tearDown(self):
        """Teardown after each test"""
        print("Tearing down after a test.")

    @classmethod
    def tearDownClass(cls):
        """Class teardown for all tests"""
        print("Tearing down class resources.")
    
    def test_initialization(self):
        """Test the initialization of the Player class"""
        self.assertEqual(self.player.year, 2023)
        self.assertIsNone(self.player.data)
    
    @patch('pkg_resources.resource_stream')
    def test_load_data_file_not_found(self, mock_resource_stream):
        """Test the load_data method when the file is not found"""
        mock_resource_stream.side_effect = FileNotFoundError
        
        # Attempt to load data with a filename that raises FileNotFoundError
        self.player.filename = "skaters2023.csv"
        self.player.load_data('skaters2023.csv')

        # Check that the data remains None after the error
        self.assertIsNone(self.player.data)

    def test_get_player_data_found(self):
        """Test the _get_player_data method when player data is found"""
        # Mocking a player data frame
        self.player.data = pd.DataFrame({
            'name': ['evander kane'],
            'team': ['san jose sharks'],
            'position': ['left wing'],
            'I_F_goals': [15],
            'I_F_points': [30]
        })

        player_data = self.player._get_player_data('evander kane')

        # Check if the correct player data is returned
        self.assertIsNotNone(player_data)
        self.assertEqual(player_data['name'], 'evander kane')
        self.assertEqual(player_data['team'], 'san jose sharks')
        self.assertEqual(player_data['I_F_goals'], 15)

    def test_get_player_data_not_found(self):
        """Test the _get_player_data method when player data is not found"""
        self.player.data = pd.DataFrame({
            'name': ['evander kane'],
            'team': ['san jose sharks'],
            'position': ['left wing'],
            'I_F_goals': [15],
            'I_F_points': [30]
        })

        player_data = self.player._get_player_data('connor mcdavid')

        # Check that no data is returned for a non-existent player
        self.assertIsNone(player_data)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)