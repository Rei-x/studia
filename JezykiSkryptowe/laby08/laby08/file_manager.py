from datetime import date
from laby08.log_parser import ApacheLog


class FileManager:
    def __init__(self, lines_per_page=100):
        self.lines_per_page = lines_per_page
        self.file_lines = []
        self.filtered_lines = []
        self.current_page = 0
        self.total_pages = 0

    def load_log_file(self, file_path: str):
        with open(file_path, "r") as file:
            self.file_lines = file.readlines()
            self.filtered_lines = self.file_lines
            self.total_pages = (len(self.file_lines) - 1) // self.lines_per_page + 1
            self.current_page = 0

    def apply_date_filter(self, from_date: date, to_date: date):
        self.filtered_lines = [
            line
            for line in self.file_lines
            if from_date <= ApacheLog.from_log(line).timestamp.date() <= to_date
        ]
        self.total_pages = (len(self.filtered_lines) - 1) // self.lines_per_page + 1
        self.current_page = 0

    def get_page_lines(self):
        start_index = self.current_page * self.lines_per_page
        end_index = start_index + self.lines_per_page
        return self.filtered_lines[start_index:end_index]

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            return True
        return False

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            return True
        return False
