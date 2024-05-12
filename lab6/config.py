import json
import os
import logging

STANDARD_FILE_PATH = "lab6/config.json"

class Configuration:    
    def __init__(self, web_server_name = "Apache", ip_address = "192.168.0.1", logging_level="INFO", number_of_lines=10, return_code = 200):
        self.web_server_name = web_server_name
        self.ip_address = ip_address
        self.logging_level = logging_level
        self.number_of_lines = number_of_lines
        self.return_code = return_code
    
    def get_from_input(self):
        self.web_server_name = input("Enter web server name: ")
        self.ip_address = input("Enter IP address: ")
        logging_level = input("Enter logging level: ").upper()
        self.check_logging_level(logging_level)
        self.logging_level = logging_level
        self.number_of_lines = input("Enter number of lines: ")
        self.return_code = input("Enter return code: ")


    def save_as_json(self, file_path = STANDARD_FILE_PATH):
        with open(file_path, 'w') as file:
            json.dump(self.__dict__, file)

    def load_from_json(self, file_path = STANDARD_FILE_PATH):
        if not os.path.exists(file_path):
            logging.error("File config.json does not exist")
            raise FileNotFoundError()
        
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                logging.error("File is not a proper Json file")
                raise ValueError()

            default_values = self.__dict__
            if "logging_level" in data:
                self.check_logging_level(data["logging_level"])

            for key in data:
                if data[key] is None:
                    logging.info(f"Value of {key} is None, using default value")
                default_values[key] = data[key]
            self.__dict__ = default_values  
    
    def check_logging_level(self, logging_level):
        default_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        assert logging_level in default_levels, "Logging level is not valid"
    
    def __str__(self):
        return f"Web server name: {self.web_server_name}\n 
        IP address: {self.ip_address}\n 
        Logging level: {self.logging_level}\n 
        Number of lines: {self.number_of_lines}\n 
        Return code: {self.return_code}"


def main():
    logging.basicConfig(level=logging.INFO)
    config = Configuration().load_from_json()
    print(config)

if __name__ == "__main__":
    main()