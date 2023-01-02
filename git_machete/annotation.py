import re
from typing import Callable

from git_machete import utils


class Qualifiers:
    rebase: bool
    push: bool

    def __init__(self, annotation: str):
        self._annotation = annotation
        self._annotation_without_qualifiers = annotation
        self._rebase_text = ''
        self._push_text = ''
        self.rebase = True
        self.push = True

        match_pattern: Callable[[str], str] = lambda text: f'.*\\b{text}=no\\b.*'
        sub_pattern: Callable[[str], str] = lambda text: f'[ ]?{text}=no[ ]?'

        rebase_match = re.match(match_pattern('rebase'), annotation)
        if rebase_match:
            self.rebase = False
            self._rebase_text = 'rebase=no'
            self._annotation_without_qualifiers = re.sub(sub_pattern('rebase'), ' ', self._annotation_without_qualifiers)

        push_match = re.match(match_pattern('push'), annotation)
        if push_match:
            self.push = False
            self._push_text = 'push=no'
            self._annotation_without_qualifiers = re.sub(sub_pattern('push'), ' ', self._annotation_without_qualifiers)

    def get_annotation_text_without_qualifiers(self) -> str:
        return self._annotation_without_qualifiers.strip()

    def get_qualifiers_text(self) -> str:
        return f'{self._rebase_text.strip()} {self._push_text.strip()}'.replace('  ', ' ').strip()


class Annotation:
    text: str
    text_without_qualifiers: str
    qualifiers_text: str
    qualifiers: Qualifiers

    def __init__(self, text: str):
        self.text = text
        self.qualifiers = Qualifiers(text)
        self.text_without_qualifiers = self.qualifiers.get_annotation_text_without_qualifiers()
        self.qualifiers_text = self.qualifiers.get_qualifiers_text()

    def get_formatted_text(self) -> str:
        annotation_text = f"  {utils.dim(self.text_without_qualifiers)}"
        if self.qualifiers_text != '':
            annotation_text += ' ' if self.text_without_qualifiers != '' else ''
            annotation_text += utils.dim(utils.underline(s=self.qualifiers_text))
        return annotation_text