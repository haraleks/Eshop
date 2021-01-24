from abc import ABC, abstractproperty, abstractmethod
from typing import Any

from django.core.mail import EmailMultiAlternatives


class Builder(ABC):

    @abstractproperty
    def email_content(self) -> None:
        pass

    @abstractmethod
    def build_base_email(self) -> None:
        pass

    @abstractmethod
    def build_html_email(self) -> None:
        pass


class Email:

    def __init__(self) -> None:
        self._text_content = []
        self._html_content = []
        self._subject = None
        self._recipient_list = []
        self._from_email = None
        self._attach_file = None

    @property
    def text_content(self):
        return self._text_content

    @text_content.setter
    def text_content(self, email_content):
        self.text_content.append(email_content)

    @property
    def html_content(self):
        return self._html_content

    @html_content.setter
    def html_content(self, html_content):
        self.html_content.append(html_content)

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, subject_text: Any) -> None:
        self._subject = subject_text

    @property
    def recipient_list(self):
        return self._recipient_list

    @recipient_list.setter
    def recipient_list(self, recipient: Any) -> None:
        self._recipient_list.append(recipient)

    @property
    def from_email(self):
        return self._from_email

    @from_email.setter
    def from_email(self, from_email: Any) -> None:
        self._from_email = from_email

    @property
    def attach_file(self):
        return self._attach_file

    @attach_file.setter
    def attach_file(self, attach_file: Any) -> None:
        self._attach_file = attach_file

    def send(self):
        mail = EmailMultiAlternatives(self.subject, self.text_content,
                                      self.from_email, self.recipient_list)
        if self.attach_file:
            mail.attach_file(self.attach_file)
        if self.html_content:
            mail.attach_alternative(self.html_content, "text/html")
        mail.send()


class MailBuilder(Builder):

    def __init__(self, recipient_list,
                 from_email,
                 subject,
                 text,
                 attach_file=None) -> None:
        self._email_content = Email()
        self._recipient_list = recipient_list
        self._from_email = from_email
        self._subject = subject
        self._text = text
        self._attach_file = attach_file
        self.reset()

    def reset(self) -> None:
        self._email_content = Email()

    @property
    def email_content(self) -> Email:
        text_email = self._email_content
        self.reset()
        return text_email

    def build_base_email(self) -> None:
        self._email_content.text_content = self._text
        self._email_content.subject = self._subject
        self._email_content.recipient_list = self._recipient_list
        self._email_content.from_email = self._from_email
        self._email_content.attach_file = self._attach_file

    def build_html_email(self) -> None:
        html_content = f"<p>{self._text}</p>"
        self._email_content.text_content = self._text
        self._email_content.html_content = html_content
        self._email_content.subject = self._subject
        self._email_content.recipient_list = self._recipient_list
        self._email_content.from_email = self._from_email
        self._email_content.attach_file = self._attach_file


class Director:

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> MailBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: MailBuilder) -> None:
        self._builder = builder

    def build_base_email(self) -> None:
        self.builder.build_base_email()

    def build_html_email(self) -> None:
        self.builder.build_html_email()
