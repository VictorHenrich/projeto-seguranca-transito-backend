from typing import TypeAlias, Collection, List
from argparse import ArgumentParser, _SubParsersAction

from .task import Task
from patterns.command import ICommand


ITask: TypeAlias = ICommand[None]
Tasks: TypeAlias = List[ITask]


class TaskManager:
    def __init__(self, name: str, subparser: _SubParsersAction) -> None:
        self.__argument_parser: ArgumentParser = subparser.add_parser(name)
        self.__name: str = name
        self.__tasks: Tasks = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def subparser(self) -> ArgumentParser:
        return self.__argument_parser

    @property
    def tasks(self) -> Tasks:
        return self.__tasks

    def add_task(self, task: Task):
        self.__tasks.append(task)

        names: Collection[str] = f"-{task.shortname}", f"--{task.name}"

        self.__argument_parser.add_argument(
            *names, help=task.description, action="store_true"
        )

    def execute(self, props: Collection[str]) -> None:
        tasks: Collection[ITask] = [task for task in self.__tasks if task.name in props]

        [task.execute(None) for task in tasks]
