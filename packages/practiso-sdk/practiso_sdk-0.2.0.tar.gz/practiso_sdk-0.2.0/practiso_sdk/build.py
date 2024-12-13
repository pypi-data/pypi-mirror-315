import asyncio
from datetime import datetime, UTC
from typing import Any

from practiso_sdk.archive import Quiz, ArchiveFrame, OptionItem, Text, Image, Options, QuizContainer, Dimension


class VectorizeAgent:
    async def get_dimensions(self, quiz: Quiz) -> set[Dimension]:
        pass


class DefaultVectorizeAgent(VectorizeAgent):
    default: set[Dimension]

    def __init__(self, default: set[Dimension] | list[Dimension]):
        self.default = default if isinstance(default, set) else set(default)

    async def get_dimensions(self, quiz: Quiz) -> set[Dimension]:
        return self.default


class Builder:
    """
    Utility class to build an archive.
    """
    __quizzes: list[Quiz] = list()
    __creation_time: datetime
    __staging_stack: list[Quiz | ArchiveFrame | OptionItem] = list()

    def __init__(self, creation_time: datetime | None = None):
        self.__creation_time = creation_time if creation_time else datetime.now(UTC)

    def begin_quiz(self, name: str | None = None, creation_time: datetime | None = None,
                   modification_time: datetime | None = None) -> 'Builder':
        """
        Begin a quiz, which is added after end_quiz is called.
        """
        self.__staging_stack.append(Quiz(list(), set(), name, creation_time, modification_time))
        return self

    def end_quiz(self) -> 'Builder':
        """
        Add the previously begun quiz to the resulting archive.
        """
        self.__quizzes.append(self.__pop_staged_stack_safe([Quiz]))
        return self

    def __get_staged_peak_safe(self, t: list[type]) -> Any:
        e = self.__staging_stack[-1]
        if not any(isinstance(e, x) for x in t):
            p1 = ', '.join(x.__name__ for x in t[:-1])
            p2 = t[-1].__name__
            raise TypeError(f'Begin a {p1} or {p2} first' if p1 else f'Begin a {p2} first')
        return e

    def __pop_staged_stack_safe(self, t: list[type]) -> Any:
        e = self.__get_staged_peak_safe(t)
        self.__staging_stack.pop()
        return e

    def add_text(self, content: str) -> 'Builder':
        """
        Add a text frame directly into the current quiz / option.
        """
        peak = self.__get_staged_peak_safe([Quiz, OptionItem])
        if isinstance(peak, Quiz):
            peak.frames.append(Text(content))
        elif isinstance(peak, OptionItem):
            peak.content = Text(content)
        return self

    def begin_image(self, alt_text: str | None = None) -> 'Builder':
        """
        Begin an image frame, which is added to the current quiz / option
        after calling end_image.
        """
        self.__staging_stack.append(Image('', 0, 0, alt_text))
        return self

    def attach_image_file(self, filename: str) -> 'Builder':
        """
        Copies a file into the staging resource buffer
        :param filename: the filename in local system
        """
        # TODO(copy from filename to internal buffer)
        self.__get_staged_peak_safe([Image]).filename = filename
        return self

    def end_image(self) -> 'Builder':
        """
        Add the previously begun image frame into the current
        quiz / option.
        """
        image = self.__pop_staged_stack_safe([Image])
        peak = self.__get_staged_peak_safe([Quiz, OptionItem])
        if isinstance(peak, Quiz):
            peak.frames.append(image)
        elif isinstance(peak, OptionItem):
            peak.content = image
        return self

    def begin_options(self, name: str | None = None) -> 'Builder':
        """
        Begin an options frame, which is added to the current quiz
        after end_options is called.
        :param name: caption of the frame
        """
        self.__staging_stack.append(Options(set(), name))
        return self

    def end_options(self) -> 'Builder':
        """
        Add the options frame previously begun to the current quiz.
        """
        e = self.__pop_staged_stack_safe([Options])
        self.__get_staged_peak_safe([Quiz]).frames.append(e)
        return self

    def begin_option(self, is_key: bool = False, priority: int = 0) -> 'Builder':
        """
        Begin an option item, which is added to the current options frame
        after end_option is called.
        :param is_key: True if the option is considered one of or the only answer
        :param priority: how this option should be sorted when a Practiso session begins
        :return:
        """
        self.__staging_stack.append(OptionItem(ArchiveFrame(), is_key, priority))
        return self

    def end_option(self) -> 'Builder':
        """
        Add the previously begun option to the current options frame.
        """
        e: OptionItem = self.__pop_staged_stack_safe([OptionItem])
        if type(e) == ArchiveFrame:
            raise ValueError('Empty option item')

        self.__get_staged_peak_safe([Options]).content.add(e)

        return self

    async def build(self, vectorizer: VectorizeAgent | None = None) -> 'QuizContainer':
        """
        Call it a day.
        :param vectorizer: The agent used to determine what dimensions are the quizzes respectively falls into.
        :return: The archive.
        """

        if vectorizer is not None:
            async def update_dimensions(quiz: Quiz):
                quiz.dimensions = await vectorizer.get_dimensions(quiz)

            await asyncio.gather(*(update_dimensions(quiz) for quiz in self.__quizzes))

        return QuizContainer(self.__quizzes, self.__creation_time)
