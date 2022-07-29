import argparse
import shlex

from unittest import TestCase

from upact.cmdline.subcommands.urls import sub_parser

class UrlsCmdlineTests(TestCase):
    
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
        result = self.parser.parse_args(shlex.split("--block www.google.com"))
        self.assertEqual(result.urls_to_block, ["www.google.com"])
        self.assert_empty_playtime(result)

    def test_block_multiple_site(self):
        result = self.parser.parse_args(shlex.split("--block www.google.com google.com"))
        self.assertEqual(result.urls_to_block, ["www.google.com", "google.com"])
        self.assert_empty_playtime(result)

    def test_block_with_playtime_rules(self):
        result = self.parser.parse_args(shlex.split('--block www.google.com google.com --allow="every week" --at-interval 13:00 15:00'))
        self.assertEqual(result.urls_to_block, ["www.google.com", "google.com"])
        self.assertEqual(result.playtime_days,"every week")
        self.assertEqual(result.playtime_hours,[["13:00", "15:00"]])

    def test_block_with_playtime_multiple_hours(self):
        result = self.parser.parse_args(shlex.split('--block www.google.com google.com --allow="every week" --at-interval 13:00 15:00 --at-interval 17:00 19:00'))
        self.assertEqual(result.urls_to_block, ["www.google.com", "google.com"])
        self.assertEqual(result.playtime_days,"every week")
        self.assertEqual(result.playtime_hours,[["13:00", "15:00"], ["17:00", "19:00"]])

    def test_remove(self):
        result = self.parser.parse_args(shlex.split('--remove facebook.com www.facebook.com'))
        self.assertEqual(result.urls_to_remove, ['facebook.com', 'www.facebook.com'])
        self.assertEqual(result.urls_to_block, None)
        self.assert_empty_playtime(result)

    def test_empty_remove_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--remove')))

    def test_remove_with_block_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--block www.google.com --remove www.google.com')))

    def test_remove_with_allow_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--block www.google.com --allow="every week" --remove www.google.com')))

    def test_remove_with_at_interval_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--block www.google.com --allow="every week" --at-interval 19:00 20:00 --remove www.google.com')))

    def test_invalid_allow_str(self):
        self.check_command_fails(
                lambda: self.parser.parse_args(shlex.split('--block www.google.com google.com --allow="alkdjflaksdjf" --at-interval 13:00 15:00 --at-interval 17:00 19:00')))

    def test_invalid_at_interval_single_hour(self):
        self.check_command_fails(
            lambda: self.parser.parse_args(shlex.split('--block www.google.com google.com --allow="every week" --at-interval 17:00')))

    def test_invalid_at_interval_three_hours(self):
        self.check_command_fails(
            lambda: self.parser.parse_args(shlex.split('--block www.google.com google.com --allow="every week" --at-interval 17:00 19:00 20:00')))

    def test_empty_block_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--block')))

    def test_no_block_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--allow="every week"')))

    def test_hour_without_days_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--block facebook.com --at-interval 18:00 20:00')))

    def test_empty_days_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--block www.google.com google.com --allow')))

    def test_empty_hours_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--block www.google.com google.com --allow="every weekend" --at-interval')))

    def test_multiple_days_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--block www.google.com google.com --allow="every weekend" --allow="every year" --playtime_hours 17:00 19:00')))

    def test_listing(self):
        result = self.parser.parse_args(shlex.split('--list'))
        self.assertTrue(result.command is not None)

    def test_listing_and_remove_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--list --remove google.com')))

    def test_listing_and_block_fails(self):
        self.check_command_fails(lambda: self.parser.parse_args(shlex.split('--list --block google.com')))

    def test_function_handler(self):
        result = self.parser.parse_args(shlex.split('--block www.google.com google.com --allow="every week" --at-interval 13:00 15:00 --at-interval 17:00 19:00'))
        result.command(result)

    def test_remove_action_handler(self):
        result = self.parser.parse_args(shlex.split('--remove www.google.com facebook.com'))
        result.command(result)