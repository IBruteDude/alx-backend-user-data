#!/usr/bin/env python3
""" Module for the filtered logger
"""
from typing import List
import logging
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """
    """
    return separator.join([
        re.sub(
            r'([{}])=(.*)'.format('|'.join(fields)),
            r'\1={}'.format(redaction),
            field)
        for field in message.split(separator)[:-1]])


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError


if __name__ == '__main__':
    fields = ["password", "date_of_birth"]
    messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;"
                "date_of_birth=12/12/1986;",
                "name=bob;email=bob@dylan.com;password=bobbycool;"
                "date_of_birth=03/04/1993;"]

    for message in messages:
        print(filter_datum(fields, 'xxx', message, ';'))
