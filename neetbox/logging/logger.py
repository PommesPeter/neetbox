# -*- coding: utf-8 -*-
#
# Author: GavinGong aka VisualDust
# URL:    https://gong.host
# Date:   20230315

import functools
import os
from datetime import date, datetime
from enum import Enum
from inspect import isclass, iscoroutinefunction, isgeneratorfunction
from random import randint
from typing import Any, Optional

from rich.panel import Panel

from neetbox.core import Registry
from neetbox.logging._writer import (
    FileLogWriter,
    JsonLogWriter,
    consoleLogWriter,
    webSocketLogWriter,
)
from neetbox.logging.formatting import LogStyle, colored_text, styled_text
from neetbox.utils import formatting
from neetbox.utils.framing import get_caller_identity_traceback


class LogLevel(Enum):
    ALL = 4
    DEBUG = 3
    INFO = 2
    WARNING = 1
    ERROR = 0

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value


__WHOM_2_LOGGER = Registry("__LOGGERS")

_GLOBAL_LOG_LEVEL = LogLevel.INFO


def set_log_level(level: LogLevel):
    if type(level) is str:
        level = {
            "ALL": LogLevel.ALL,
            "DEBUG": LogLevel.DEBUG,
            "INFO": LogLevel.INFO,
            "WARNING": LogLevel.WARNING,
            "ERROR": LogLevel.ERROR,
        }[level]
    if type(level) is int:
        assert level >= 0 and level <= 3
        level = LogLevel(level)
    global _GLOBAL_LOG_LEVEL
    _GLOBAL_LOG_LEVEL = level


class Logger:
    def __init__(self, whom, style: Optional[LogStyle] = None):
        self.whom: Any = whom
        self.style: Optional[LogStyle] = style
        # default writing to console and ws
        self.console_writer = consoleLogWriter
        self.ws_writer = webSocketLogWriter
        self.file_writer = None

    def __call__(self, whom: Any = None, style: Optional[LogStyle] = None) -> "Logger":
        if whom is None:
            return DEFAULT_LOGGER
        if whom in __WHOM_2_LOGGER:
            return __WHOM_2_LOGGER[whom]
        __WHOM_2_LOGGER[whom] = Logger(whom=whom, style=style)
        return __WHOM_2_LOGGER[whom]

    def _write(self, raw_msg):
        # perform log
        if into_stdout:
            rprint(
                _prefix
                + _datetime
                + _style.split_char_cmd * min(len(_datetime), 1)
                + styled_text(_whom, style=_style)
                + _style.split_char_cmd * min(len(_whom), 1),
                _pure_str_message,
            )
        if into_file and self.file_writer:
            self.file_writer.write(
                _prefix
                + _datetime
                + _style.split_char_txt * min(len(_datetime), 1)
                + _whom
                + _style.split_char_txt * min(len(_whom), 1)
                + _pure_str_message
                + "\n"
            )

    def log(
        self,
        *content,
        prefix: Optional[str] = None,
        datetime_format: Optional[str] = None,
        with_identifier: Optional[bool] = None,
        with_datetime: Optional[bool] = None,
        skip_writers: Optional[list[str]] = None,
        traceback=2,
    ):
        _caller_identity = get_caller_identity_traceback(traceback=traceback)

        # getting style
        _style = self.style

        # converting args into a single string
        _pure_str_message = ""
        for msg in content:
            _pure_str_message += str(msg) + " "

        return self

    def ok(self, *message, flag="OK"):
        if _GLOBAL_LOG_LEVEL >= LogLevel.INFO:
            self.log(
                *message,
                prefix=f"[{colored_text(flag, 'green')}]",
                into_file=False,
                traceback=3,
            )
            self.log(*message, prefix=flag, into_stdout=False, traceback=3)
        return self

    def debug(self, *message, flag="DEBUG"):
        if _GLOBAL_LOG_LEVEL >= LogLevel.DEBUG:
            self.log(
                *message,
                prefix=f"[{colored_text(flag, 'cyan')}]",
                into_file=False,
                traceback=3,
            )
            self.log(*message, prefix=flag, into_stdout=False, traceback=3)
        return self

    def info(self, *message, flag="INFO"):
        if _GLOBAL_LOG_LEVEL >= LogLevel.INFO:
            self.log(
                *message,
                prefix=f"[{colored_text(flag, 'white')}]",
                into_file=False,
                traceback=3,
            )
            self.log(*message, prefix=flag, into_stdout=False, traceback=3)
        return self

    def warn(self, *message, flag="WARNING"):
        if _GLOBAL_LOG_LEVEL >= LogLevel.WARNING:
            self.log(
                *message,
                prefix=f"[{colored_text(flag, 'yellow')}]",
                into_file=False,
                traceback=3,
            )
            self.log(*message, prefix=flag, into_stdout=False, traceback=3)
        return self

    def err(self, err, flag="ERROR", reraise=False):
        if type(err) is not Exception:
            err = RuntimeError(str(err))
        if _GLOBAL_LOG_LEVEL >= LogLevel.ERROR:
            self.log(
                str(err),
                prefix=f"[{colored_text(flag,'red')}]",
                into_file=False,
                traceback=3,
            )
            self.log(str(err), prefix=flag, into_stdout=False, traceback=3)
        if reraise:
            raise err
        return self

    def mention(self, func):
        @functools.wraps(func)
        def with_logging(*args, **kwargs):
            self.log(f"Currently running: {func.__name__}", traceback=3)
            return func(*args, **kwargs)

        return with_logging

    def banner(self, text, font: Optional[str] = None):
        from pyfiglet import Figlet, FigletFont

        builtin_font_list = [
            "ansiregular",
            "ansishadow",
            "isometrixc2",
            "nscripts",
            "nvscript",
        ]
        if not font:
            font = builtin_font_list[randint(0, len(builtin_font_list)) - 1]

        if font not in FigletFont.getFonts():
            if font in builtin_font_list:  # builtin but not installed
                module_path = os.path.dirname(__file__)
                FigletFont.installFonts(f"{module_path}/flfs/{font}.flf")
            else:  # path?
                assert os.path.isfile(
                    font
                ), "The provided font is not a fontname or a font file path."
                file_name = os.path.basename(font)
                file = os.path.splitext(file_name)
                if file[0] not in FigletFont.getFonts():  # no installed file match the file name
                    try:
                        self.info(f"{file[0]} is not installed. Trying to install as a fontfile.")
                        FigletFont.installFonts(f"res/flfs/{font}.flf")
                    except Exception:
                        self.err("Could not install font {font}. Fallback to default.")
                        font = None
                else:
                    font = file[0]
        f = Figlet(font)
        rendered_text = f.renderText(text)
        rprint(Panel.fit(f"{rendered_text}", border_style="green"))
        return self

    def skip_lines(self, line_cnt=1):
        """Let the logger log some empty lines

        Args:
            line_cnt (int, optional): how many empty line. Defaults to 1.

        Returns:
            _Logger : the logger instance itself
        """
        self.log("\n" * line_cnt, with_datetime=False, with_identifier=False)
        return self

    def log_txt_file(self, file):
        if isinstance(file, str):
            file = open(file)
        context = ""
        for line in file.readlines():
            context += line
        self.log(context, with_datetime=False, with_identifier=False)
        return self

    def set_log_dir(self, path, independent=False):
        if not path:
            self._bind_file(None)
            return self
        if not path:
            self._bind_file(None)
            return self
        if os.path.isfile(path):
            raise Exception("Target path is not a directory.")
        if not os.path.exists(path):
            DEFAULT_LOGGER.info(f"Directory {path} not found, trying to create.")
            try:
                os.makedirs(path)
            except Exception:
                DEFAULT_LOGGER.err(f"Failed when trying to create directory {path}")
                raise Exception(f"Failed when trying to create directory {path}")
        log_file_name = ""
        if independent:
            log_file_name += self.whom
        log_file_name += str(date.today()) + ".log"
        self._bind_file(os.path.join(path, log_file_name))
        return self

    def _bind_file(self, path):
        if not path:
            self.file_writer = None
            return self
        self.file_writer = FileLogWriter(path=path)
        return self

    def file_bend(self) -> bool:
        return self.file_writer is not None


DEFAULT_LOGGER = Logger(None)
