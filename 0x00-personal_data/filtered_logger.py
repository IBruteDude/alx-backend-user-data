#!/usr/bin/env python3
""" Module for the filtered logger
"""
from typing import List
import logging
import re
import os
import mysql.connector.connection


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Filter selecten data fields from a message
    """
    return re.sub(r'({})=(.*?){}'.format('|'.join(fields), separator),
                  r'\1={}{}'.format(redaction, separator), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialise the redacted fields of the formatter
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Redact the selected fields from the LogRecord
        """
        redacted_message = filter_datum(
            self.fields, self.REDACTION,
            record.getMessage(), self.SEPARATOR
        )

        return self.FORMAT % {
            'name': record.name,
            'levelname': record.levelname,
            'asctime': self.formatTime(record),
            'message': '; '.join(redacted_message.split(';'))}


# user_data = [line for line in csv.reader(open("user_data.csv"))]
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """ Create a 'Logger' object with the RedactingFormatter stream handler
    """
    logger = logging.Logger("user_data", logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Create a 'MySQLConnection' object from environment variables
    """
    config = {
        'user': os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        'password': os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        'host': os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        'database': os.getenv('PERSONAL_DATA_DB_NAME')
    }
    con = None
    while con is None:
        try:
            con = mysql.connector.connection.MySQLConnection(**config)
        except mysql.connector.Error as e:
            print(e.with_traceback())
    return con


def main():
    """ The main entry point for the program
    """
    con = get_db()
    while not con.is_connected():
        con.connect()
    cur = con.cursor()
    cur.execute('SHOW COLUMNS FROM users;')
    colnames = next(zip(*cur.fetchall()))

    cur.execute('SELECT * FROM users;')
    rows = cur.fetchall()
    logger = get_logger()
    for row in rows:
        msg = ''.join([f'{k}={v};' for k, v in (zip(colnames, row))])
        logger.info(msg)
    

if __name__ == '__main__':
    main()
    # fields = ["password", "date_of_birth"]
    # messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;"
    #             "date_of_birth=12/12/1986;",
    #             "name=bob;email=bob@dylan.com;password=bobbycool;"
    #             "date_of_birth=03/04/1993;"]

    # for msg in messages:
    #     print(filter_datum(fields, 'xxx', msg, ';'))

    # #############################################################

    # msg = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
    # log_record = logging.LogRecord("my_logger", logging.INFO,
    #                                os.getcwd(), 56, msg, None, None)
    # formatter = RedactingFormatter(fields=["email", "ssn", "password"])
    # print(formatter.format(log_record))

    # #############################################################

    # db = get_db()
    # cursor = db.cursor()
    # cursor.execute("SELECT COUNT(*) FROM users;")
    # for row in cursor:
    #     print(row[0])
    # cursor.close()
    # db.close()
