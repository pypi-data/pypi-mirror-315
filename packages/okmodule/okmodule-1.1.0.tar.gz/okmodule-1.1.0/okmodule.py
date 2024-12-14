# -*- coding: utf-8 -*-
import re
import logging
import subprocess


class Module:

    def name(self):
        return self.__class__.__name__

    def logger(self):
        return logging.getLogger(f'okmodule.{self.name()}')

    def log(self, message, level=logging.INFO, **kwargs):
        self.logger().log(level, message, **kwargs)

    def main(self):
        raise NotImplementedError

    def __call__(self):
        return self.main()

    def __repr__(self):
        return f'<{self.name()} at 0x{id(self):0x}>'


class CommandArgument:
    @staticmethod
    def _tostr(value):
        return value if isinstance(value, str) else str(value)

    def args(self, value):
        raise NotImplementedError


class Argument(CommandArgument):
    def args(self, value):
        return [self._tostr(value)]


class Option(CommandArgument):
    def __init__(self, name):
        self.name = name

    def args(self, value):
        args = []
        if isinstance(value, list) or isinstance(value, tuple):
            for per_value in value:
                args.extend([self.name, self._tostr(per_value)])
        else:
            args.extend([self.name, self._tostr(value)])
        return args


class Flag(CommandArgument):
    def __init__(self, name):
        self.name = name

    def args(self, value):
        return [self.name] if value else []


class Command(Module):
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def path(self):
        return re.sub(r'(?!^)([A-Z]+)', r'-\1', self.name()).lower()  # MyCommand -> my-command

    def args(self):
        args = [self.path()]
        for name, command_argument in self.__class__.__dict__.items():
            if not isinstance(command_argument, CommandArgument):
                continue
            if name not in self.__dict__:
                continue
            value = self.__dict__[name]
            args.extend(command_argument.args(value))
        return args

    def result(self, proc):  # noqa
        return None

    def main(self, env=None, stdout=None, stderr=None):
        args = self.args()
        self.log(f'Running command {" ".join(args)}')
        proc = subprocess.run(args, env=env, stdout=stdout, stderr=stderr, check=True)
        return self.result(proc)

    def __call__(self, env=None, stdout=None, stderr=None):
        return self.main(env, stdout, stderr)
