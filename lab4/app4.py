from datetime import datetime
import logging


class Log:
    def __init__(self, ip, time, address, code, bytes_send, transfer_time):
        self.ip = ip
        self.time = time
        self.address = address
        self.code = code
        self.bytes_send = bytes_send
        self.transfer_time = transfer_time
    
    def __str__(self):
        return f"{self.ip} {self.time} {self.address} {self.code} {self.bytes_send} {self.transfer_time}"
    
    def __repr__(self):
        return f"Log({self.ip}, {self.time}, {self.address}, {self.code}, {self.bytes_send}, {self.transfer_time})"

def string_to_datetime(string):
    date = string.split('/')
    day = int(date[0])
    month = get_month_from_name(date[1])
    time = date[2].split(':')
    year = int(time[0])
    hour = int(time[1])
    minute = int(time[2])
    second = int(time[3])
    return datetime(year, month, day, hour, minute, second)

def get_month_from_name(month_name):
    months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }
    return months[month_name]    

def read_line(line):
    args = line.split()
    ip = args[0]
    time = string_to_datetime(args[1])
    address = args[2]
    code = int(args[3])
    bytes_send = int(args[4])
    transfer_time = float(args[5])
    return Log(ip, time, address, code, bytes_send, transfer_time)


def read_file(file_path):
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            logs.append(read_line(line))
    return logs


def print_logs_between_dates(logs, start_date: datetime, end_date : datetime):
    if(start_date > end_date):
        logging.error("Start date is after end date")
    else:
        for log in logs:
            if log.time >= start_date and log.time <= end_date:
                print(log)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logs = read_file("lab4\log.txt")
    print_logs_between_dates(logs, datetime(2020, 10, 18, 4, 0, 0), datetime(2020, 10, 18, 4, 55, 1))
    print_logs_between_dates(logs, datetime(2020, 10, 18, 4, 55, 1), datetime(2020, 10, 18, 4, 0, 0))

#https://docs.python.org/3/library/ipaddress.html

#https://docs.python.org/3/library/datetime.html