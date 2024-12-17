# -*- coding: utf-8 -*-

"""
interpreters module
"""

import argparse
import logging
import shlex
import sys

from typing import Callable, Self

from .buffers import History

from . import const


CMD_EXIT = "exit"
CMD_HELP = "help"
CMD_HISTORY = "history"

COMMON_DESCRIPTIONS = {
    CMD_EXIT: "Exit the interpreter",
    CMD_HELP: "Print help message",
    CMD_HISTORY: "Show the command history",
}


class InterpreterExit(Exception):
    """Raised on Interpreter exit"""


class NoSuggestionFound(Exception):
    """Raised if no suggestion could be found for the given line"""


class BaseErrorWithMessage(Exception):
    """Error called with a message"""

    def __init__(self, message: str) -> None:
        """Store the message"""
        self.message = message

    def __str__(self) -> str:
        """String value (the message)"""
        return self.message


class CommandError(BaseErrorWithMessage):
    """Raised if a command encountered an error"""


class PatchedArgparseError(BaseErrorWithMessage):
    """Raised if the PatchedArgumentParser encountered ana error situation"""


class PatchedArgumentParser(argparse.ArgumentParser):
    """argparse.ArgumentParser instances in Python 3.11 and before
    exit with an error in certain cases in spite of
    `exit_on_error=False`.
    This class modifies the behavior of the .error() method
    to raise an exception intead of exiting
    """

    def error(self, message):
        """error(message: string)

        Raises an exception.
        """
        raise PatchedArgparseError(message)


class SubCommand:
    """Object holding all data of a subcommand,
    with chainable add_* methods
    """

    def __init__(
        self,
        command: str,
        subparsers: argparse._SubParsersAction,
        desc: str = const.EMPTY,
    ) -> None:
        """Keep a reference to the created (sub)parser object"""
        self.__parser = subparsers.add_parser(
            command,
            help=desc,
            description=desc,
            add_help=False,
            exit_on_error=False,
        )
        self.__parser.set_defaults(command=command)
        self.__completions: set[str] = set()
        self.__callbacks: list[Callable] = []

    @property
    def parser(self) -> argparse.ArgumentParser:
        """Return the parser"""
        return self.__parser

    def add_argument(self, *args, **kwargs) -> Self:
        """Add arguments to the parser and return a reference to self"""
        self.__parser.add_argument(*args, **kwargs)
        return self

    def add_callbacks(self, *callbacks: Callable) -> Self:
        """Add callback functions and return a reference to self"""
        self.__callbacks.extend(callbacks)
        return self

    def add_completions(self, *completions: str) -> Self:
        """Add completion elements and return a reference to self"""
        self.__completions.update(set(completions))
        return self

    def execute(self, arguments: argparse.Namespace) -> None:
        """Execute all callbacks until exhausted or a callback raises an error"""
        for callback in self.__callbacks:
            try:
                callback(arguments)
            except CommandError as error:
                logging.error(str(error))
                break
            #
        #


class BaseInterpreter:
    """Shell interpreter base class"""

    stopcommand = CMD_EXIT

    def __init__(self, history: History = History()) -> None:
        """Initialize the interpreter"""
        self.history = history
        self.known_commands = {CMD_HISTORY, self.stopcommand}

    def execute(self, read_line: str) -> None:
        """Execute the read line and return a Reaction instance"""
        core_line = read_line.strip()
        logging.debug("Executing %r ...", core_line)
        if core_line == self.stopcommand:
            raise InterpreterExit
        #
        self.history.add(read_line)
        if core_line.startswith(CMD_HISTORY):
            self.show_history(start=1, end=-1)
        #

    def show_history(self, start=1, end=-1) -> None:
        """Show the history range"""
        logging.info("History:")
        for idx, entry in self.history.iter_range(start, end):
            print(f"  [{idx:3d}]  {entry}")
        #

    def suggest(self, line) -> str:
        """Suggest an entry if line matches the beginning of exact one entry
        If line matches two or more beginnings, suggest the
        longest common beginning.
        """
        filtered = {
            suggestion
            for suggestion in self.known_commands
            if suggestion.startswith(line)
        }
        if not filtered:
            raise NoSuggestionFound
        #
        if len(filtered) == 1:
            return f"{filtered.pop()} "
        #
        # Find the longest common match between the remaining suggestions
        common = line
        suggestion = common
        while True:
            pos = len(common)
            for idx, entry in enumerate(filtered):
                if not idx:
                    try:
                        suggestion = f"{common}{entry[pos]}"
                    except IndexError:
                        return common
                    #
                    continue
                #
                if not entry.startswith(suggestion):
                    return common
                #
            #
            common = suggestion
        #
        raise NoSuggestionFound


class ArgumentBasedInterpreter(BaseInterpreter):
    """argparse based interpreter"""

    def __init__(self, history: History = History(), **kwargs) -> None:
        """Initialize the interpreter"""
        super().__init__(history=history)
        self.descriptions = dict(COMMON_DESCRIPTIONS) | kwargs
        self.known_commands = set(self.descriptions)
        if sys.version_info.major == 3 and sys.version_info.minor < 12:
            __parser_class: type[argparse.ArgumentParser] = PatchedArgumentParser
        else:
            __parser_class = argparse.ArgumentParser
        #
        self.__cmd_parser = __parser_class(
            prog="", description=None, add_help=False, exit_on_error=False
        )
        self.__subparsers = self.__cmd_parser.add_subparsers()
        self.__commands: dict[str, SubCommand] = {}
        for command_name, desc in self.descriptions.items():
            command = self.add_command(command_name, desc=desc)
            if command_name == CMD_HELP:
                command.add_argument(
                    "topic", nargs="?", help="the help topic"
                ).add_completions(*self.known_commands).add_callbacks(self.cb_show_help)
            elif command_name == CMD_HISTORY:
                command.add_argument(
                    "-n",
                    "--number",
                    type=int,
                    help="Number of history entries to show (all entries by default)",
                ).add_callbacks(self.cb_show_history)
            #
        #

    def add_command(self, command_name: str, desc: str = const.EMPTY) -> SubCommand:
        """Add a subcommand"""
        subcommand = SubCommand(command_name, self.__subparsers, desc=desc)
        self.__commands[command_name] = subcommand
        return subcommand

    def cb_show_help(self, arguments: argparse.Namespace) -> None:
        """Callback function for showing help"""
        try:
            parser = self[arguments.topic].parser
        except KeyError:
            self.__cmd_parser.print_help()
        else:
            parser.print_help()
        #

    def cb_show_history(self, arguments: argparse.Namespace) -> None:
        """Callback function for showing help"""
        if arguments.number:
            start = -arguments.number
        else:
            start = 1
        #
        super().show_history(start=start)

    def __getitem__(self, command_name: str) -> SubCommand:
        r"""Return the subcommand for _command\_name_"""
        return self.__commands[command_name]

    def execute(self, read_line: str) -> None:
        """Execute the read line and dispatch
        according to the parsed arguments
        """
        logging.debug("Executing %r …", read_line)
        try:
            arguments = self.__cmd_parser.parse_args(shlex.split(read_line))
        except (argparse.ArgumentError, PatchedArgparseError) as error:
            logging.error(str(error))
            self.history.add(read_line)
            return
        #
        if arguments.command == self.stopcommand:
            raise InterpreterExit
        #
        self.history.add(read_line)
        logging.debug("Arguments: %r", arguments)
        self[arguments.command].execute(arguments)
