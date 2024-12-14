# Copyright Contributors to the Packit project.
# SPDX-License-Identifier: MIT

import copy
import datetime
import getpass
import os
import pwd
import re
import shutil
import subprocess
from typing import List, Optional, Union, overload

from specfile.exceptions import SpecfileException
from specfile.formatter import formatted
from specfile.macros import Macros
from specfile.sections import Section
from specfile.types import SupportsIndex
from specfile.utils import EVR, UserList

WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
MONTHS = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


class ChangelogEntry:
    """
    Class that represents a changelog entry. Changelog entry consists of
    a header line starting with _*_, followed by timestamp, author and optional
    extra text (usually EVR), and one or more content lines.

    Attributes:
        header: Header of the entry.
        content: List of lines forming the content of the entry.
    """

    def __init__(
        self,
        header: str,
        content: List[str],
        following_lines: Optional[List[str]] = None,
    ) -> None:
        """
        Initializes a changelog entry object.

        Args:
            header: Header of the entry.
            content: List of lines forming the content of the entry.
            following_lines: Extra lines that follow the entry.
        """
        self.header = header
        self.content = content.copy()
        self._following_lines = (
            following_lines.copy() if following_lines is not None else []
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChangelogEntry):
            return NotImplemented
        return (
            self.header == other.header
            and self.content == other.content
            and self._following_lines == other._following_lines
        )

    def __str__(self) -> str:
        return f"{self.header}\n" + "\n".join(self.content) + "\n"

    @formatted
    def __repr__(self) -> str:
        return f"ChangelogEntry({self.header!r}, {self.content!r}, {self._following_lines!r})"

    @property
    def evr(self) -> Optional[str]:
        """EVR (epoch, version, release) of the entry."""
        m = re.match(
            r"""
            ^.*
            \s+                       # preceding whitespace
            ((?P<sb>\[)|(?P<rb>\())?  # optional opening bracket
            (?P<evr>(\d+:)?\S+-\S+?)  # EVR
            (?(sb)\]|(?(rb)\)))       # matching closing bracket
            :?                        # optional colon
            \s*                       # optional following whitespace
            $
            """,
            self.header,
            re.VERBOSE,
        )
        if not m:
            return None
        return m.group("evr")

    @property
    def extended_timestamp(self) -> bool:
        """Whether the timestamp present in the entry header is extended (date and time)."""
        weekdays = "|".join(WEEKDAYS)
        months = "|".join(MONTHS)
        m = re.search(
            rf"""
            ({weekdays})     # weekday
            [ ]
            ({months})       # month
            [ ]+
            ([12]?\d|3[01])  # day of month
            [ ]
            ([01]\d|2[0-3])  # hour
            :
            ([0-5]\d)        # minute
            :
            ([0-5]\d)        # second
            [ ]
            \S+              # timezone
            [ ]
            \d{{4}}          # year
            """,
            self.header,
            re.VERBOSE,
        )
        return m is not None

    @property
    def day_of_month_padding(self) -> str:
        """Padding of day of month in the entry header timestamp"""
        weekdays = "|".join(WEEKDAYS)
        months = "|".join(MONTHS)
        m = re.search(
            rf"""
            ({weekdays})                 # weekday
            [ ]
            ({months})                   # month
            [ ]
            (?P<wsp>[ ]*)                # optional whitespace padding
            ((?P<zp>0)?\d|[12]\d|3[01])  # possibly zero-padded day of month
            """,
            self.header,
            re.VERBOSE,
        )
        if not m:
            return ""
        return m.group("wsp") + (m.group("zp") or "")

    @classmethod
    def assemble(
        cls,
        timestamp: Union[datetime.date, datetime.datetime],
        author: str,
        content: List[str],
        evr: Optional[str] = None,
        day_of_month_padding: str = "0",
        append_newline: bool = True,
    ) -> "ChangelogEntry":
        """
        Assembles a changelog entry.

        Args:
            timestamp: Timestamp of the entry.
                Supply `datetime` rather than `date` for extended format.
            author: Author of the entry.
            content: List of lines forming the content of the entry.
            evr: EVR (epoch, version, release) of the entry.
            day_of_month_padding: Padding to apply to day of month in the timestamp.
            append_newline: Whether the entry should be followed by an empty line.

        Returns:
            New instance of `ChangelogEntry` class.
        """
        weekday = WEEKDAYS[timestamp.weekday()]
        month = MONTHS[timestamp.month - 1]
        header = f"* {weekday} {month}"
        if day_of_month_padding.endswith("0"):
            header += f" {day_of_month_padding[:-1]}{timestamp.day:02}"
        else:
            header += f" {day_of_month_padding}{timestamp.day}"
        if isinstance(timestamp, datetime.datetime):
            # extended format
            if not timestamp.tzinfo:
                timestamp = timestamp.replace(tzinfo=datetime.timezone.utc)
            header += f" {timestamp:%H:%M:%S %Z}"
        header += f" {timestamp:%Y} {author}"
        if evr is not None:
            header += f" - {evr}"
        return cls(header, content, [""] if append_newline else None)


class Changelog(UserList[ChangelogEntry]):
    """
    Class that represents a changelog. It behaves like a list of changelog entries,
    ordered from bottom to top - the top (newest) entry has index _-1_, the bottom
    (oldest) one has index _0_.

    Attributes:
        data: List of individual entries.
    """

    def __init__(
        self,
        data: Optional[List[ChangelogEntry]] = None,
        predecessor: Optional[List[str]] = None,
    ) -> None:
        """
        Initializes a changelog object.

        Args:
            data: List of individual changelog entries.
            predecessor: List of lines at the beginning of a section
                that can't be parsed into changelog entries.
        """
        super().__init__()
        if data is not None:
            self.data = data.copy()
        self._predecessor = predecessor.copy() if predecessor is not None else []

    def __str__(self) -> str:
        return "\n".join(str(i) for i in reversed(self.data))

    @formatted
    def __repr__(self) -> str:
        return f"Changelog({self.data!r}, {self._predecessor!r})"

    @overload
    def __getitem__(self, i: SupportsIndex) -> ChangelogEntry:
        pass

    @overload
    def __getitem__(self, i: slice) -> "Changelog":
        pass

    def __getitem__(self, i):
        if isinstance(i, slice):
            return Changelog(self.data[i], self._predecessor)
        else:
            return self.data[i]

    def __delitem__(self, i: Union[SupportsIndex, slice]) -> None:
        def delete(index):
            following_lines = self.data[index]._following_lines.copy()
            del self.data[index]
            if index < len(self.data):
                self.data[index]._following_lines.extend(following_lines[1:])
            else:
                self._predecessor.extend(following_lines[1:])

        if isinstance(i, slice):
            for index in reversed(range(len(self.data))[i]):
                delete(index)
        else:
            delete(i)

    def copy(self) -> "Changelog":
        return copy.copy(self)

    def filter(
        self, since: Optional[str] = None, until: Optional[str] = None
    ) -> "Changelog":
        """
        Filters changelog entries with EVR between since and until.

        Args:
            since: Optional lower bound. If specified, entries with EVR higher
                than or equal to this will be included.
            until: Optional upper bound. If specified, entries with EVR lower
                than or equal to this will be included.

        Returns:
            Filtered changelog.
        """

        def parse_evr(s):
            try:
                return EVR.from_string(s)
            except SpecfileException:
                return EVR(version="0")

        if since is None:
            start_index = 0
        else:
            start_index = next(
                (
                    i
                    for i, e in enumerate(self.data)
                    if parse_evr(e.evr) >= parse_evr(since)
                ),
                len(self.data) + 1,
            )
        if until is None:
            end_index = len(self.data) + 1
        else:
            end_index = next(
                (
                    i + 1
                    for i, e in reversed(list(enumerate(self.data)))
                    if parse_evr(e.evr) <= parse_evr(until)
                ),
                0,
            )
        return self[start_index:end_index]

    @classmethod
    def parse(cls, section: Section) -> "Changelog":
        """
        Parses a `%changelog` section.

        Args:
            section: Section to parse.

        Returns:
            New instance of `Changelog` class.
        """

        def extract_following_lines(content: List[str]) -> List[str]:
            following_lines: List[str] = []
            while content and not content[-1].strip():
                following_lines.insert(0, content.pop())
            return following_lines

        data: List[ChangelogEntry] = []
        predecessor = []
        header = None
        content: List[str] = []
        for line in section:
            if line.startswith("*"):
                if header is None or "".join(content).strip():
                    if header:
                        following_lines = extract_following_lines(content)
                        data.insert(0, ChangelogEntry(header, content, following_lines))
                    header = line
                    content = []
                else:
                    content.append(line)
            elif header:
                content.append(line)
            else:
                predecessor.append(line)
        if header:
            following_lines = extract_following_lines(content)
            data.insert(0, ChangelogEntry(header, content, following_lines))
        return cls(data, predecessor)

    def get_raw_section_data(self) -> List[str]:
        """
        Reconstructs section data from changelog.

        Returns:
            List of lines forming the reconstructed section data.
        """
        result = self._predecessor.copy()
        for entry in reversed(self.data):
            result.append(entry.header)
            result.extend(entry.content)
            result.extend(entry._following_lines)
        return result


def _getent_name() -> str:
    username = getpass.getuser()
    pwd_struct = pwd.getpwnam(username)
    # Use the plain username if the name field is empty
    return pwd_struct.pw_gecos or username


def guess_packager() -> str:
    """
    Guesses the name and e-mail of a packager to use for changelog entries.
    This function uses logic similar to `rpmdev-packager` utility.

    The following places are searched for this value (in this order):

    - `$RPM_PACKAGER` environment variable
    - `%packager` macro
    - git config
    - Unix username

    Returns:
        A string to use for the changelog entry author.
        If nothing was detected, an empty string is returned.
    """
    if "RPM_PACKAGER" in os.environ:
        return os.environ["RPM_PACKAGER"]

    packager = Macros.expand("%packager")
    if packager != "%packager":
        return packager

    email: str = ""
    fullname: str = ""

    if shutil.which("git"):
        email = subprocess.run(
            ["git", "config", "user.email"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        ).stdout.strip()
        fullname = subprocess.run(
            ["git", "config", "user.name"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        ).stdout.strip()
    if not fullname:
        fullname = _getent_name()

    if fullname and email:
        return f"{fullname} <{email}>"
    return email or fullname
