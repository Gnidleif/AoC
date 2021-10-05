#!/usr/bin/python3
from typing import Generator
from base_day import BaseDay
import time
import re

class Challenge:
    def __init__(self):
        self.days = [
            Day1(),
            Day2(),
            Day3(),
            Day4(),
            Day5(),
            Day6(),
        ]
        self.total_ms = 0

    def timedCall(self, callback) -> tuple():
        tick = time.perf_counter() * 1000
        retVal = callback()
        tock = time.perf_counter() * 1000

        return (retVal, f"{tock-tick:.3f}")

    def run(self) -> Generator[str, None, None]:
        for d in self.days:
            res1, time1 = self.timedCall(d.part1)
            res2, time2 = self.timedCall(d.part2)
            self.total_ms += time1 + time2
            yield f"{d.name}: part1[{time1}ms]({res1}) | part2[{time2}ms]({res2})"

def run(_: list()) -> bool:
    for y in Challenge().run():
        print(y)

    return False

class Day6(BaseDay):
    def __init__(self):
        super(Day6, self).__init__(day_number=6)
        self.groups = (" ".join(self.input)).split("  ")

    def part1(self) -> int:
        return sum([len(set(line.replace(" ", ""))) for line in self.groups])

    def part2(self) -> int:
        count = 0
        for line in self.groups:
            num_people = len(line.split(" "))
            letters = set(line.replace(" ", ""))
            for chr in letters:
                ans_count = line.count(chr)
                if ans_count == num_people:
                    count += 1

        return count

class Day5(BaseDay):
    def __init__(self):
        super(Day5, self).__init__(day_number=5)
        self.codes = [(["0" if y == "F" else "1" for y in x[:7]], ["0" if y == "L" else "1" for y in x[7:]]) for x in self.input]

    def part1(self) -> int:
        def iterate_code(line, upper):
            lower = 0
            for code in line:
                split = round((upper - lower) / 2)
                if code == "1":
                    lower += split
                else:
                    upper -= split
            return upper if line[-1] == "1" else lower

        seat_ids = []
        for line in self.codes:
            row = iterate_code(line[0], 127)
            col = iterate_code(line[1], 7)
            seat_ids.append((row * 8) + col)

        return max(seat_ids)

class Day4(BaseDay):
    def __init__(self):
        super(Day4, self).__init__(day_number=4)
        self.lines = (" ".join(self.input)).split("  ")

    def part1(self) -> int:
        count = 0
        rgx = re.compile(r"byr|iyr|eyr|hgt|hcl|ecl|pid|cid")
        for line in self.lines:
            result = re.findall(rgx, line)
            if len(result) == 8 or (len(result) == 7 and "cid" not in result):
                count += 1
        return count

    def part2(self) -> int:
        ecls_rgx = re.compile(r"amb|blu|brn|gry|grn|hzl|oth")
        main_rgx = re.compile(r"(byr:\d{4})|(iyr:\d{4})|(eyr:\d{4})|(hgt:[\w\d]+)|(hcl:#[a-f\d]{6})|(ecl:\w{3})|(pid:\b\d{9}\b)|(cid)")
        excluded = set(["hcl", "pid", "cid"])
        validate = {
            "byr": lambda x: 1920 <= int(x) <= 2002,
            "iyr": lambda x: 2010 <= int(x) <= 2020,
            "eyr": lambda x: 2020 <= int(x) <= 2030,
            "hgt": lambda x: len(x[:-2]) > 0 and ((59 <= int(x[:-2]) <= 76 and x[-2:] == "in") or (150 <= int(x[:-2]) <= 193 and x[-2:] == "cm")),
            "ecl": lambda x: ecls_rgx.match(x),
        }
        count = 0
        for line in self.lines:
            info = ["".join(x) for x in re.findall(main_rgx, line)]
            valid = set()
            for subs in info:
                key, val = subs[:3], subs[4:]
                if key in valid:
                    break
                if key not in excluded and not (len(val) > 0 and validate[key](val)):
                    break
                valid.add(key)
            if len(valid) == 8 or (len(valid) == 7 and "cid" not in valid):
                count += 1
        return count

class Day3(BaseDay):
    def __init__(self):
        super(Day3, self).__init__(day_number=3)
        self.height = len(self.input)
        self.width = len(self.input[0])

    def part1(self, dx=3, dy=1) -> int:
        count = 0
        pos = (0, 0)
        while pos[1] < self.height:
            if self.input[pos[1]][pos[0] % self.width] == "#":
                count += 1
            pos = (pos[0] + dx, pos[1] + dy)
        return count

    def part2(self) -> int:
        return self.part1(1, 1) * self.part1() * self.part1(5, 1) * self.part1(7, 1) * self.part1(1, 2)

class Day2(BaseDay):
    def __init__(self):
        super(Day2, self).__init__(day_number=2)
        rgx = re.compile(r"^(\d+)-(\d+)\s(\w):\s(\w+)$", flags=re.MULTILINE|re.IGNORECASE)
        self.lines = [rgx.split(x)[1:-1] for x in self.input]

    def part1(self) -> int:
        result = 0
        for line in self.lines:
            _min = int(line[0])
            _max = int(line[1])
            _chr = line[2]
            _str = line[3]
            _cnt = _str.count(_chr)
            if _min <= _cnt <= _max:
                result += 1
        return result

    def part2(self) -> int:
        result = 0
        for line in self.lines:
            _min = int(line[0]) - 1
            _max = int(line[1]) - 1
            _chr = line[2]
            _str = line[3]
            _tst = set([_str[_min], _str[_max]])
            if len(_tst) == 2 and _chr in _tst:
                result += 1
        return result

class Day1(BaseDay):
    def __init__(self):
        super(Day1, self).__init__(day_number=1)
        self.nums = [int(x) for x in self.input]
        self.set_nums = set(self.nums)

    def part1(self) -> int:
        for num in self.nums:
            if 2020 - num in self.set_nums:
                return num * (2020 - num)

    def part2(self) -> int:
        for num in self.nums:
            for num2 in self.nums:
                if (2020 - num - num2) in self.set_nums:
                    return num * (2020 - num - num2) * num2

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])