#!/usr/bin/python3
import os
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class BaseDay:
    def __init__(self, day_number: int):
        self.name = f"day{day_number}"
        self.input = self.read_input()

    def read_input(self):
        file_name = f"{self.name}.txt"
        with open(os.path.join(__location__, "inputs", file_name), 'r', encoding="utf-8") as f:
            return [x.strip() for x in f]

    def part1(self) -> bool:
        return False

    def part2(self) -> bool:
        return False