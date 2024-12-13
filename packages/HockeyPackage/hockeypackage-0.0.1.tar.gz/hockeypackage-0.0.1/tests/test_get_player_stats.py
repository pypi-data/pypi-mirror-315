#!/usr/bin/env python
# coding: utf-8

import unittest
from unittest.mock import patch
from hockey.player.get_player_stats import get_player_stats  
from hockey.player.skater import Skater
from hockey.player.goalie import Goalie

class TestGetUserInput(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Class setup for all tests"""
        print("Setting up class resources.")
    
    def setUp(self):
        """Set up before each test"""
        print("Setting up for a test.")

    def tearDown(self):
        """Teardown after each test"""
        print("Tearing down after a test.")

    @classmethod
    def tearDownClass(cls):
        """Class teardown for all tests"""
        print("Tearing down class resources.")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_player_stats_skater(self, mock_print, mock_input):
        """Test the get_player_stats function for a skater (Evander Kane)."""
        # Mock the user inputs for year, player type, player name, and stats type
        mock_input.side_effect = ['2020', 'skater', 'evander kane', 'basic']
        
        # Call the function with mocked inputs
        get_player_stats()

        mock_print.assert_any_call("Position: L")
        mock_print.assert_any_call("Team: S.J")

        # Assert that player data is not None and matches expected output
        self.assertIsNotNone(mock_print, "Player data should not be None")  
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_player_stats_goalie(self, mock_print, mock_input):
        """Test the get_player_stats function for a goalie (Tristan Jarry)."""
        # Mock the user inputs for goalie stats
        mock_input.side_effect = ['2021', 'goalie', 'tristan jarry', 'advanced']
        
        # Call the function with mocked inputs
        get_player_stats()

        # Check that advanced goalie stats are printed 
        
        mock_print.assert_any_call("Save Percentage (SV%): 0.909")       
        mock_print.assert_any_call("Shutouts: 2")  
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_player_stats_invalid_player_type(self, mock_print, mock_input):
        """Test for invalid player type input."""
        # Simulating user inputs with invalid player type
        mock_input.side_effect = ['2020', 'defender']
        # Call the function with mocked inputs
        get_player_stats()

        # Check for the invalid player type message
        mock_print.assert_any_call("Invalid player type. Please enter either 'skater' or 'goalie'.")

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
