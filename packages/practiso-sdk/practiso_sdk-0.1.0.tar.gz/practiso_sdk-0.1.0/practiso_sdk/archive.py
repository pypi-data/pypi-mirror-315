import xml.etree.ElementTree as Xml
from datetime import datetime, UTC
from typing import Callable, Any

NAMESPACE = 'http://schema.zhufucdev.com/practiso'


def _get_attribute_safe(element: Xml.Element, attr_name: str, convert: Callable[[str], Any] | None = None) -> Any:
    if attr_name not in element.attrib:
        raise TypeError(f'Missing attribute {attr_name} in tag {element.tag}')
    if convert:
        return convert(element.attrib[attr_name])
    else:
        return element.attrib[attr_name]


def _get_simple_tag_name(element: Xml.Element):
    rb = element.tag.index('}')
    if rb < 0:
        return element.tag
    else:
        return element.tag[rb + 1:]


def _namespace_extended(tag: str):
    return '{' + NAMESPACE + '}' + tag


class ArchiveFrame:
    """
    Abstraction of supported frames.
    """

    def append_to_element(self, element: Xml.Element):
        pass

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'ArchiveFrame':
        tag_name = _get_simple_tag_name(element)
        if tag_name == 'text':
            return Text.parse_xml_element(element)
        elif tag_name == 'image':
            return Image.parse_xml_element(element)
        elif tag_name == 'options':
            return Options.parse_xml_element(element)

    def __hash__(self):
        raise RuntimeError(f'Unimplemented method __hash__ for {type(self).__name__}')


class Text(ArchiveFrame):
    """
    Abstraction of a text frame.
    """
    content: str

    def __init__(self, content: str):
        self.content = content

    def append_to_element(self, element: Xml.Element):
        sub = Xml.SubElement(element, 'text')
        sub.text = self.content

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'Text':
        if _get_simple_tag_name(element) != 'text':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')

        return Text(element.text)

    def __hash__(self):
        return hash(self.content) * 31

    def __eq__(self, other):
        return isinstance(other, Text) and other.content == self.content


class Image(ArchiveFrame):
    """
    Abstraction of an image frame.
    """
    filename: str
    width: int
    height: int
    alt_text: str | None

    def __init__(self, filename: str, width: int, height: int, alt_text: str | None = None):
        self.filename = filename
        self.width = width
        self.height = height
        self.alt_text = alt_text

    def append_to_element(self, element: Xml.Element):
        sub = Xml.SubElement(element, 'image',
                             attrib={'src': self.filename, 'width': str(self.width), 'height': str(self.height)})
        if self.alt_text:
            sub.attrib['alt'] = self.alt_text

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'Image':
        if _get_simple_tag_name(element) != 'image':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')

        return Image(
            filename=_get_attribute_safe(element, 'src'),
            width=_get_attribute_safe(element, 'width', int),
            height=_get_attribute_safe(element, 'height', int),
            alt_text=element.attrib['alt'] if 'alt' in element.attrib else None
        )

    def __hash__(self):
        return hash(self.alt_text) * 31 + hash(self.filename) * 31 + hash(self.width * 31 + self.height) * 31

    def __eq__(self, other):
        return isinstance(other, Image) and other.width == self.width \
            and other.height == self.height \
            and other.filename == self.filename \
            and other.alt_text == self.alt_text


class OptionItem:
    """
    Abstraction of a selectable option item.
    """
    is_key: bool
    """
    True if this option is one of or the only correct ones.
    """
    priority: int
    """
    How this option is ranked. Options with the same priority
    will be shuffled randomly, while ones of higher priority (smaller value)
    will be ranked ascent.
    """
    content: ArchiveFrame

    def __init__(self, content: ArchiveFrame, is_key: bool = False, priority: int = 0):
        self.content = content
        self.is_key = is_key
        self.priority = priority

    def append_to_element(self, element: Xml.Element):
        sub = Xml.SubElement(element, 'item', attrib={'priority': str(self.priority)})
        if self.is_key:
            sub.attrib['key'] = 'true'
        self.content.append_to_element(sub)

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'OptionItem':
        if _get_simple_tag_name(element) != 'item':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')
        if len(element) != 1:
            raise TypeError(f'Unexpected {len(element)} children tag')

        return OptionItem(
            content=ArchiveFrame.parse_xml_element(element[0]),
            is_key='key' in element.attrib and element.attrib['key'] == 'true',
            priority=_get_attribute_safe(element, 'priority', int)
        )

    def __hash__(self):
        return hash(self.is_key) * 31 + self.priority * 31 + hash(self.content)

    def __eq__(self, other):
        return isinstance(other, OptionItem) and other.content == self.content \
            and other.is_key == self.is_key \
            and other.priority == self.priority


class Options(ArchiveFrame):
    """
    Abstraction of an options frame, composed of OptionItem.
    """
    content: set[OptionItem]
    name: str | None

    def __init__(self, content: set[OptionItem] | list[OptionItem], name: str | None = None):
        self.content = content if isinstance(content, set) else set(content)
        self.name = name

    def append_to_element(self, element: Xml.Element):
        sub = Xml.SubElement(element, 'options')
        for item in self.content:
            item.append_to_element(sub)

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'ArchiveFrame':
        if _get_simple_tag_name(element) != 'options':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')

        return Options(
            content=list(OptionItem.parse_xml_element(e) for e in element if _get_simple_tag_name(e) == 'item'),
            name=element.attrib['name'] if 'name' in element.attrib else None
        )

    def __hash__(self):
        return hash(self.content) * 31 + hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Options) \
            and other.content == self.content \
            and other.name == self.name


class Dimension:
    """
    What knowledge point a question is related to and how much so.
    """
    name: str
    __intensity: float

    @property
    def intensity(self):
        """
        How much the knowledge is related to a question,
        ranging in (0, 1].
        :return: Length of the vector representing the relativity in this dimension.
        """
        return self.__intensity

    @intensity.setter
    def intensity(self, value: float):
        if value > 1 or value <= 0:
            raise ValueError('intensity must fall in range of (0, 1]')
        self.__intensity = value

    def append_to_element(self, element: Xml.Element):
        sub = Xml.SubElement(element, 'dimension', attrib={'name': self.name})
        sub.text = str(self.intensity)

    def __init__(self, name: str, intensity: float):
        self.name = name
        self.intensity = intensity

    def __hash__(self):
        return hash(self.name) * 31 + hash(self.__intensity)

    def __eq__(self, other):
        return isinstance(other, Dimension) \
            and other.name == self.name \
            and other.__intensity == self.__intensity

    def __repr__(self):
        return f'({self.name}, {self.intensity})'

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'Dimension':
        if _get_simple_tag_name(element) != 'dimension':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')

        return Dimension(
            name=_get_attribute_safe(element, 'name'),
            intensity=float(element.text)
        )


class Quiz:
    """
    Basic unit of a Practiso session representing a question.
    A quiz is composed of an array of frames, where each either
    presents the question itself or the answerable fields.
    This only affects how the user sees the question and how the system
    handles the answers and recommendations, not how the user interacts
    with the interface.
    """
    name: str | None
    creation_time: datetime
    modification_time: datetime | None
    frames: list[ArchiveFrame]
    dimensions: set[Dimension]

    def __init__(self, frames: list[ArchiveFrame], dimensions: set[Dimension] | list[Dimension],
                 name: str | None, creation_time: datetime | None = None, modification_time: datetime | None = None):
        self.name = name
        self.creation_time = creation_time if creation_time is not None else datetime.now(UTC)
        self.modification_time = modification_time
        self.frames = frames
        self.dimensions = dimensions if isinstance(dimensions, set) else set(dimensions)

    def append_to_element(self, element: Xml.Element):
        sub = Xml.SubElement(element, 'quiz',
                             attrib={'creation': self.creation_time.isoformat()})
        if self.name:
            sub.attrib['name'] = self.name
        if self.modification_time:
            sub.attrib['modification'] = self.modification_time.isoformat()

        frames_element = Xml.SubElement(sub, 'frames')
        for frame in self.frames:
            frame.append_to_element(frames_element)

        for dimension in self.dimensions:
            dimension.append_to_element(sub)

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'Quiz':
        if _get_simple_tag_name(element) != 'quiz':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')

        frames_iter = (e for e in element if _get_simple_tag_name(e) == 'frames')
        try:
            frames_element = next(frames_iter)
        except StopIteration:
            raise TypeError('Expected one frames child, got none')

        try:
            next(frames_iter)
            raise TypeError('Unexpected multi-frames-children tag')
        except StopIteration:
            pass

        return Quiz(
            name=element.attrib['name'] if 'name' in element.attrib else None,
            creation_time=_get_attribute_safe(element, 'creation', datetime.fromisoformat),
            modification_time=datetime.fromisoformat(
                element.attrib['modification']) if 'modification' in element.attrib else None,
            dimensions=list(Dimension.parse_xml_element(e) for e in element if _get_simple_tag_name(e) == 'dimension'),
            frames=list(ArchiveFrame.parse_xml_element(e) for e in frames_element)
        )

    def __eq__(self, other):
        return isinstance(other, Quiz) and other.name == self.name \
            and other.creation_time == self.creation_time \
            and other.modification_time == self.modification_time \
            and other.frames == self.frames \
            and other.dimensions == self.dimensions


class QuizContainer:
    """
    Derivation from a snapshot of the database, removing unnecessary items
    (i.e. reducing SQL relations to direct object composition)
    and is enough to be imported to reconstruct the meaningful part.

    Note: binary resources such as images are not included.
    """
    creation_time: datetime
    content: list[Quiz]

    def __init__(self, content: list[Quiz], creation_time: datetime | None = None):
        self.content = content
        self.creation_time = creation_time if creation_time is not None else datetime.now(UTC)

    def to_xml_element(self) -> Xml.Element:
        """
        Convert to an XML hierarchy.
        :return: XML hierarchy where the root element represents the archive.
        """
        doc = Xml.Element('archive', attrib={'xmlns': NAMESPACE,
                                             'creation': self.creation_time.isoformat()})
        for quiz in self.content:
            quiz.append_to_element(doc)
        return doc

    def to_bytes(self) -> bytes:
        """
        Convert to a byte array, which once gzipped is ready
        to be imported by Practiso.
        :return: A byte array representing the archive.
        """
        ele = self.to_xml_element()
        return Xml.tostring(ele, xml_declaration=True, encoding='utf-8')

    def __eq__(self, other):
        return isinstance(other, QuizContainer) \
            and other.content == self.content \
            and other.creation_time == self.creation_time

    @staticmethod
    def parse_xml_element(element: Xml.Element) -> 'QuizContainer':
        """
        Convert an XML hierarchy to a comprehensible quiz composite.
        :param element: The XML hierarchy to be parsed.
        :return: The quiz composite.
        """
        if _get_simple_tag_name(element) != 'archive':
            raise TypeError(f'Unexpected tag {_get_simple_tag_name(element)}')

        return QuizContainer(
            creation_time=_get_attribute_safe(element, 'creation', datetime.fromisoformat),
            content=list(Quiz.parse_xml_element(e) for e in element if _get_simple_tag_name(e) == 'quiz')
        )


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

    def build(self) -> 'QuizContainer':
        """
        Call it a day.
        """
        return QuizContainer(self.__quizzes, self.__creation_time)
