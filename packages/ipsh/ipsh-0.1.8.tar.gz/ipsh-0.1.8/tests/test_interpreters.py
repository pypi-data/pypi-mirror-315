# -*- coding: utf-8 -*-

"""
test the ipsh.interpreters module
"""

import argparse
import io
import logging

from unittest import TestCase

from unittest.mock import patch

from ipsh import interpreters

from . import commons as tc


class TheCount:
    """Simple counting class"""

    def __init__(self, initial_value: int = 0) -> None:
        """Initialize the internal value"""
        self.__value: int = initial_value

    @property
    def value(self) -> int:
        """Return the internal value"""
        return self.__value

    def up(self, arguments: argparse.Namespace) -> None:
        """Add the arguments.number value"""
        if arguments.command != "add":
            raise ValueError("wrong method")
        #
        self.__value += arguments.number

    def down(self, arguments: argparse.Namespace) -> None:
        """Subtract the arguments.number value"""
        if arguments.command != "subtract":
            raise ValueError("wrong method")
        #
        self.__value -= arguments.number


class BaseInterpreter(TestCase):
    """Test the BaseInterpreter class"""

    def setUp(self):
        """Fixture: screen mock"""
        self.screen = tc.ScreenMock()

    def test_init_props(self) -> None:
        """__init__() method and properties"""
        self.screen.clear()
        base = interpreters.BaseInterpreter()
        self.assertSetEqual(
            base.known_commands, {interpreters.CMD_EXIT, interpreters.CMD_HISTORY}
        )

    def test_execute_history(self) -> None:
        """.execute() and .history() methods"""
        self.screen.clear()
        commands = ("abc", "defg", "hijk", interpreters.CMD_HISTORY)
        with patch("ipsh.interpreters.print", new=self.screen.print):
            base = interpreters.BaseInterpreter()
            for single_command in commands:
                base.execute(single_command)
            #
            self.assertEqual(len(base.history), 5)
            self.assertListEqual(
                self.screen.lines,
                [
                    "  [  1]  abc",
                    "  [  2]  defg",
                    "  [  3]  hijk",
                    "  [  4]  history",
                    "",
                ],
            )
            self.screen.clear()
            base.show_history(2, -2)
            self.assertListEqual(
                self.screen.lines,
                [
                    "  [  2]  defg",
                    "  [  3]  hijk",
                    "",
                ],
            )
        #

    def test_suggest(self) -> None:
        """.suggest() method"""
        self.screen.clear()
        base = interpreters.BaseInterpreter()
        for start, suggestion in (
            ("e", f"{interpreters.CMD_EXIT} "),
            ("h", f"{interpreters.CMD_HISTORY} "),
        ):
            with self.subTest("suggestion", start=start):
                self.assertEqual(base.suggest(start), suggestion)
            #
        #
        with self.subTest("No suggestion"):
            self.assertRaises(
                interpreters.NoSuggestionFound,
                base.suggest,
                "guaranteed-no-suggestion-available",
            )
        #


class ArgumentBasedInterpreter(TestCase):
    """Test the ArgumentBasedInterpreter"""

    def test_combined(self) -> None:
        """cross-method tests"""
        count = TheCount(initial_value=7)
        abi = interpreters.ArgumentBasedInterpreter()
        abi.add_command("add", desc="add a value").add_argument(
            "-n",
            "--number",
            type=int,
            help="the value to be added (default: %(default)s)",
            default=1,
        ).add_callbacks(count.up)
        abi.add_command("subtract", desc="subtract a value").add_argument(
            "-n",
            "--number",
            type=int,
            help="the value to be subtracted (default: %(default)s)",
            default=1,
        ).add_callbacks(count.down)
        # Test the callback mechanism
        for line, expected_value in (
            ("add", 8),
            ("add -n 8", 16),
            ("add --number -9", 7),
            ("subtract -n 10", -3),
        ):
            with self.subTest("execute", line=line, expected_value=expected_value):
                abi.execute(line)
                self.assertEqual(count.value, expected_value)
            #
        #
        screen = tc.ScreenMock()
        with patch("ipsh.interpreters.print", new=screen.print):
            with self.subTest("partial history"):
                abi.execute("history -n 3")
                self.assertListEqual(
                    screen.lines,
                    [
                        "  [  3]  add --number -9",
                        "  [  4]  subtract -n 10",
                        "  [  5]  history -n 3",
                        "",
                    ],
                )
            #
            screen.clear()
            with self.subTest("full history"):
                abi.execute("history")
                self.assertListEqual(
                    screen.lines,
                    [
                        "  [  1]  add",
                        "  [  2]  add -n 8",
                        "  [  3]  add --number -9",
                        "  [  4]  subtract -n 10",
                        "  [  5]  history -n 3",
                        "  [  6]  history",
                        "",
                    ],
                )
            #
        #
        with self.subTest("exit"):
            self.assertRaises(interpreters.InterpreterExit, abi.execute, "exit")
        #
        invalid_command = "totally-unknown-command"
        with self.assertLogs(logging.getLogger(), level=logging.ERROR) as log_cm:
            abi.execute(invalid_command)
        #
        with self.subTest(invalid_command):
            self.assertIn(
                "argument {exit,help,history,add,subtract}: invalid choice:"
                f" {invalid_command!r} (choose from",
                log_cm.output[-1],
            )
        #
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            abi.execute("help")
            with self.subTest("help (all)"):
                self.assertTrue(
                    mock_stdout.getvalue().startswith(
                        "usage: {exit,help,history,add,subtract} ..."
                    )
                )
            #
        #
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            abi.execute("help add")
            with self.subTest("help (command)"):
                self.assertTrue(
                    mock_stdout.getvalue().startswith("usage:  add [-n NUMBER]")
                )
            #
        #
