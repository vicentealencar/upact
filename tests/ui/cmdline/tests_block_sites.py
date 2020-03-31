import argparse
import shlex

from unittest import TestCase

from ulysses.ui.cmdline.block_sites import sub_parser

class BlockSitesTests(TestCase):
    
    def check_command_fails(self, command):
        try:
            command()
            assert False
        except SystemExit as e:
            assert True

    def setUp(self):
        self.main_parser = argparse.ArgumentParser()
        self.subparsers = self.main_parser.add_subparsers()
        self.parser = sub_parser(self.subparsers)

    def assert_empty_playtime(self, parsed):
        self.assertEqual(parsed.playtime_days, None)
        self.assertEqual(parsed.playtime_hours, None)

    def test_block_single_site(self):
        result = self.parser.parse_args(shlex.split("--add www.google.com"))
        self.assertEqual(result.add, ["www.google.com"])
        self.assert_empty_playtime(result)

    def test_block_multiple_site(self):
        result = self.parser.parse_args(shlex.split("--add www.google.com google.com"))
        self.assertEqual(result.add, ["www.google.com", "google.com"])
        self.assert_empty_playtime(result)

    def test_block_with_playtime(self):
        result = self.parser.parse_args(shlex.split('--add www.google.com google.com --playtime_days="every week" --playtime_hours 13:00 15:00'))
        self.assertEqual(result.add, ["www.google.com", "google.com"])
        self.assertEqual(result.playtime_days,"every week")
        self.assertEqual(result.playtime_hours,[["13:00", "15:00"]])

    def test_block_with_playtime_multiple_hours(self):
        result = self.parser.parse_args(shlex.split('--add www.google.com google.com --playtime_days="every week" --playtime_hours 13:00 15:00 --playtime_hours 17:00 19:00'))
        self.assertEqual(result.add, ["www.google.com", "google.com"])
        self.assertEqual(result.playtime_days,"every week")
        self.assertEqual(result.playtime_hours,[["13:00", "15:00"], ["17:00", "19:00"]])

    def test_remove(self):
        result = self.parser.parse_args(shlex.split('--remove facebook.com www.facebook.com'))
        self.assertEqual(result.remove, ['facebook.com', 'www.facebook.com'])
        self.assertEqual(result.add, None)
        self.assert_empty_playtime(result)

    def test_empty_remove_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--remove')))

    def test_remove_with_add_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--add www.google.com --remove www.google.com')))

    def test_remove_with_playtime_days_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--add www.google.com --playtime_days="every week" --remove www.google.com')))

    def test_remove_with_playtime_hours_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--add www.google.com --playtime_days="every week" --playtime_hours 19:00 20:00 --remove www.google.com')))

    def test_invalid_playtime_days_str(self):
        self.check_command_fails(
            lambda: self.parser.parse_args(shlex.split('--add www.google.com google.com --playtime_days="alkdjflaksdjf" --playtime_hours 13:00 15:00 --playtime_hours 17:00 19:00')))

    def test_invalid_playtime_hours_single_hour(self):
        self.check_command_fails(
            lambda: self.parser.parse_args(shlex.split('--add www.google.com google.com --playtime_days="every week" --playtime_hours 17:00')))

    def test_invalid_playtime_hours_three_hours(self):
        self.check_command_fails(
            lambda: self.parser.parse_args(shlex.split('--add www.google.com google.com --playtime_days="every week" --playtime_hours 17:00 19:00 20:00')))

    def test_empty_add_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--add')))

    def test_no_add_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--playtime_days="every week"')))

    def test_hour_without_days_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--add facebook.com --playtime_hours 18:00 20:00')))

    def test_empty_days_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--add www.google.com google.com --playtime_days')))

    def test_empty_hours_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--add www.google.com google.com --playtime_days="every weekend" --playtime_hours')))

    def test_multiple_days_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--add www.google.com google.com --playtime_days="every weekend" --playtime_days="every year" --playtime_hours 17:00 19:00')))
