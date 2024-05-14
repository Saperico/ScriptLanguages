import re
import logging

file_path = "lab7\lab.config"
logging.basicConfig(level=logging.INFO)
class Configuration:
    def __init__(self):
        self.log_file = "INFO"
        self.display = {}

    def recognize_header(self, log_line):
        return re.match("[[a-zA-Z]*]",log_line) is not None

    def recognize_value(self, log_line):
        return re.match("[a-zA-Z]*=.+",log_line) is not None

    def match_headers(self, log_line):
        log_line = log_line[1:-1]
        switcher = {
            "LogFile" : self.set_log_file,
            "Config" : self.set_logging_config,
            "Display" : self.add_to_display
        }
        return switcher.get(log_line, "Invalid header")
    
    def add_to_display(self, log_line):
        log_line = log_line.split("=")
        self.display[log_line[0]] = log_line[1]

    def set_log_file(self, log_line):
        self.log_file = log_line

    def set_logging_config(self, log_line):
        logging.basicConfig(level=log_line)

    def open_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.readlines()    
        
    def run(self):
        file = self.open_file(file_path)
        header = None
        for line in file:
            line = line.strip()
            if self.recognize_header(line):
                header = self.match_headers(line)
            elif self.recognize_value(line):
                header(line)


config = Configuration()
config.run()
    
    