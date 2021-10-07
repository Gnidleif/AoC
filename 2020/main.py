#!/usr/bin/python3
from os import read
from sys import flags
from typing import Generator
from base_day import BaseDay
import time
import re
from copy import deepcopy


class Challenge:
    def __init__(self):
        self.days = [
            Day1(),
            Day2(),
            Day3(),
            Day4(),
            Day5(),
            Day6(),
            Day7(),
            Day8(),
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
            self.total_ms += float(time1) + float(time2)
            yield f"{d.name}: part1[{time1}ms]({res1}) | part2[{time2}ms]({res2})"


class Day8(BaseDay):
    def __init__(self, read_file=True):
        super(Day8, self).__init__(day_number=8, read_file=read_file)
        self.code = [dict(zip(["cmd", "val"], line.split(' ')))
                     for line in self.input]

    def part1(self):
        visited = set()
        i, acc = 0, 0
        while i not in visited:
            visited.add(i)
            cmd = self.code[i]["cmd"]
            val = int(self.code[i]["val"])
            i += val if cmd == "jmp" else 1
            if cmd == "acc":
                acc += val

        return acc

    def part2(self):
        original = [node.copy() for node in self.code]
        for i in range(len(self.code)):
            cmd = self.code[i]["cmd"]
            if cmd == "acc":
                continue

            self.code[i]["cmd"] = "jmp" if cmd == "nop" else "nop"
            is_infinite = False
            visited = set()
            idx, acc = 0, 0
            while idx < len(self.code):
                if idx in visited:
                    is_infinite = True
                    break
                visited.add(idx)
                cmd = self.code[idx]["cmd"]
                val = int(self.code[idx]["val"])
                idx += val if cmd == "jmp" else 1
                if cmd == "acc":
                    acc += val
            if not is_infinite:
                return acc
            self.code = [node.copy() for node in original]
        return 0


class Day7(BaseDay):
    def __init__(self, read_file=True):
        super(Day7, self).__init__(day_number=7, read_file=read_file)
        key_rgx = re.compile(r"[a-z]+\s[a-z]+")
        val_rgx = re.compile(r"(\d+)\s([a-z]+\s[a-z]+)")
        self.bag_map = {}
        for line in self.input:
            key = key_rgx.match(line).group(0)
            self.bag_map[key] = [{"amount": int(m[0]), "color": m[1]}
                                 for m in val_rgx.findall(line)]
        self.my_bag = "shiny gold"

    def contains_one(self, key) -> bool:
        if len(self.bag_map[key]) == 0:
            return False
        colors = [line["color"] for line in self.bag_map[key]]
        if len(colors) == 0:
            return False
        if self.my_bag in colors:
            return True
        for color in colors:
            if self.contains_one(color):
                return True
        return False

    def part1(self) -> int:
        count = 0
        for key in self.bag_map:
            if self.contains_one(key):
                count += 1
        return count

    def count_bags(self, key) -> int:
        count = 0
        if len(self.bag_map[key]) == 0:
            return count

        for bag in self.bag_map[key]:
            count += bag["amount"] + \
                self.count_bags(bag["color"]) * bag["amount"]

        return count

    def part2(self) -> int:
        count = self.count_bags(self.my_bag)
        return count


class Day6(BaseDay):
    def __init__(self, read_file=True):
        super(Day6, self).__init__(day_number=6, read_file=read_file)
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
    def __init__(self, read_file=True):
        super(Day5, self).__init__(day_number=5, read_file=read_file)
        self.binary = ["".join(["0" if char in ["F", "L"]
                               else "1" for char in line]) for line in self.input]

    def get_seat_id(self, code):
        row = int(code[: 7], 2)
        col = int(code[7:], 2)
        return (8 * row) + col

    def part1(self) -> int:
        top = 0
        for code in self.binary:
            seat_id = self.get_seat_id(code)
            if seat_id > top:
                top = seat_id
        return top

    def part2(self):
        last_seat = 0
        for code in sorted(self.binary):
            seat_id = self.get_seat_id(code)
            if last_seat > 0 and seat_id != (last_seat + 1):
                return seat_id - 1
            last_seat = seat_id


class Day4(BaseDay):
    def __init__(self, read_file=True):
        super(Day4, self).__init__(day_number=4, read_file=read_file)
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
        main_rgx = re.compile(
            r"(byr:\d{4})|(iyr:\d{4})|(eyr:\d{4})|(hgt:[\w\d]+)|(hcl:#[a-f\d]{6})|(ecl:\w{3})|(pid:\b\d{9}\b)|(cid)")
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
    def __init__(self, read_file=True):
        super(Day3, self).__init__(day_number=3, read_file=read_file)
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
    def __init__(self, read_file=True):
        super(Day2, self).__init__(day_number=2, read_file=read_file)
        rgx = re.compile(r"^(\d+)-(\d+)\s(\w):\s(\w+)$",
                         flags=re.MULTILINE | re.IGNORECASE)
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
    def __init__(self, read_file=True):
        super(Day1, self).__init__(day_number=1, read_file=read_file)
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


def run(_: list()) -> bool:
    c = Challenge()
    for y in c.run():
        print(y)
    print(f"run done! total time: {c.total_ms:.3f}ms")

    return False


if __name__ == "__main__":
    import sys
    run(sys.argv[1:])
