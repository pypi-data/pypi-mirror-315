# -*- coding: utf-8 -*-

"""
interpreters module
"""

import argparse
import gettext
import logging
import shlex
import sys

from collections.abc import ItemsView
from typing import Callable, Self

from .buffers import History

from . import const

_ = gettext.gettext


CMD_EXIT = "exit"
CMD_HELP = "help"
CMD_HISTORY = "history"

DESC_EXIT = _("Exit the interpreter")  # help meaage for the exit command
DESC_HELP = _("Print help message")  # help message for the help command
DESC_HISTORY = _("Show the command history")  # help meaage for the history command

COMMON_DESCRIPTIONS = {
    CMD_EXIT: DESC_EXIT,
    CMD_HELP: DESC_HELP,
    CMD_HISTORY: DESC_HISTORY,
}

DEBUG_MSG_ARGUMENTS = _("Arguments: %r")
DEBUG_MSG_EXECUTING = _("Executing %r …")

HELP_HELP_TOPIC = _("the help topic")  # help message for help argument TOPIC
HELP_HISTORY_NUMBER = _(  # help message for history argument NUMBER
    "Number of history entries to show (all entries by default)"
)

MSG_HISTORY = _("History:")


class InterpreterExit(Exception):
    """Raised on Interpreter exit"""


class NoSuggestionFound(Exception):
    """Raised if no suggestion could be found for the given line"""


class AmbiguousSuggestionResult(Exception):
    """Raised on ambiguous suggestion"""

    def __init__(self, common_part: str, *suggestions: str) -> None:
        """Contains the common part and a tuple of matching suggestions"""
        self.common_part = common_part
        self.suggestions = suggestions


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
        self.__command_name = command
        self.__desc = desc
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

    def __repr__(self) -> str:
        """String representation"""
        features: list[str] = []
        if self.__callbacks:
            features.append("callbacks")
        #
        if self.__completions:
            features.append("completions")
        #
        if features:
            appendix = f" with {' and '.join(features)}"
        else:
            appendix = ""
        #
        return (
            f"{self.__class__.__name__}"
            f"({self.__command_name!r}, desc={self.__desc!r}){appendix}"
        )

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
    history_type: type[History] = History

    def __init__(self, **kwargs: str) -> None:
        """Initialize the interpreter"""
        self.history: History = self.history_type()
        self.__descriptions: dict[str, str] = dict(COMMON_DESCRIPTIONS) | kwargs

    @property
    def description_items(self) -> ItemsView:
        """Items view of the internal descriptions dict"""
        return self.__descriptions.items()

    @property
    def known_commands(self) -> set[str]:
        """The set of known commands"""
        return set(self.__descriptions)

    def add_command_description(
        self, command_name: str, desc: str = const.EMPTY
    ) -> None:
        """Add a subcommand"""
        self.__descriptions[command_name] = desc

    def execute(self, read_line: str) -> None:
        """Execute the read line and return a Reaction instance"""
        core_line = read_line.strip()
        logging.debug(DEBUG_MSG_EXECUTING, core_line)
        if core_line == self.stopcommand:
            raise InterpreterExit
        #
        self.history.add(read_line)
        if core_line.startswith(CMD_HISTORY):
            self.show_history(start=1, end=-1)
        #

    def show_history(self, start=1, end=-1) -> None:
        """Show the history range"""
        logging.info(MSG_HISTORY)
        for idx, entry in self.history.iter_range(start, end):
            print(f"  [{idx:3d}]  {entry}")
        #

    def suggest(self, line) -> str:
        """Suggest an entry if line matches the beginning of exact one entry
        If line matches two or more beginnings, suggest the
        longest common beginning.
        """
        filtered = sorted(
            {
                suggestion
                for suggestion in self.known_commands
                if suggestion.startswith(line)
            }
        )
        try:
            first_match = filtered[0]
        except IndexError as error:
            raise NoSuggestionFound from error
        #
        if len(filtered) == 1:
            return f"{first_match} "
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
                    except IndexError as exc:
                        raise AmbiguousSuggestionResult(common, *filtered) from exc
                    #
                    continue
                #
                if not entry.startswith(suggestion):
                    raise AmbiguousSuggestionResult(common, *filtered)
                #
            #
            common = suggestion
        #
        raise NoSuggestionFound


class ArgumentBasedInterpreter(BaseInterpreter):
    """argparse based interpreter"""

    def __init__(self, **kwargs) -> None:
        """Initialize the interpreter"""
        super().__init__(**kwargs)
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
        initial_descriptions = list(self.description_items)
        for command_name, desc in initial_descriptions:
            command = self.add_command(command_name, desc=desc)
            if command_name == CMD_HELP:
                command.add_argument(
                    "topic", nargs="?", help=HELP_HELP_TOPIC
                ).add_completions(*self.known_commands).add_callbacks(self.cb_show_help)
            elif command_name == CMD_HISTORY:
                command.add_argument(
                    "-n",
                    "--number",
                    type=int,
                    help=HELP_HISTORY_NUMBER,
                ).add_callbacks(self.cb_show_history)
            #
        #

    def add_command(self, command_name: str, desc: str = const.EMPTY) -> SubCommand:
        """Add a subcommand"""
        super().add_command_description(command_name, desc=desc)
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
        logging.debug(DEBUG_MSG_EXECUTING, read_line)
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
        logging.debug(DEBUG_MSG_ARGUMENTS, arguments)
        self[arguments.command].execute(arguments)
