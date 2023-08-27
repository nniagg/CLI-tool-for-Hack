from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class Assembler:
    dest_map = {
        "": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111",
    }
    comp_map = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "M": "1110000",
        "!D": "0001101",
        "!A": "0110001",
        "!M": "1110001",
        "-D": "0001111",
        "-A": "0110011",
        "-M": "1110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "M+1": "1110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "M-1": "1110010",
        "D+A": "0000010",
        "D+M": "1000010",
        "D-A": "0010011",
        "D-M": "1010011",
        "A-D": "0000111",
        "M-D": "1000111",
        "D&A": "0000000",
        "D&M": "1000000",
        "D|A": "0010101",
        "D|M": "1010101",
    }
    jump_map = {
        "": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }
    symbol_map = {
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "SCREEN": 16384,
        "KBD": 24576,
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
    }
    var_addr = 16

    @classmethod
    def create(cls) -> Assembler:
        return cls()

    def assemble(self, assembly: Iterable[str]) -> Iterable[str]:
        res = []
        new_label_addr = 0
        for line in assembly:
            line = self.line_correction(line)
            if len(line) < 2:
                continue
            if line[0] == "(":
                self.symbol_map[line[1 : len(line) - 1]] = new_label_addr
            else:
                new_label_addr += 1

        for line in assembly:
            line = self.line_correction(line)
            if len(line) < 2:
                continue
            else:
                tmp = self.translateLine(line)
                if tmp != "-1":
                    res.append(tmp)
        return res

    def line_correction(self, line: str) -> str:
        line = line.partition("/")[0]
        line = line.strip()
        return line

    def translateLine(self, line: str) -> str:
        if line[0] == "(":
            return "-1"
        if line[0] == "@":
            return self.Ainstr(line)
        else:
            return self.Cinstr(line)

    def Ainstr(self, line: str) -> str:
        substr = line[1:]
        if substr.isdecimal():
            res = int(substr)
        elif substr not in self.symbol_map:
            self.symbol_map[substr] = self.var_addr
            res = self.var_addr
            self.var_addr += 1
        else:
            res = self.symbol_map[substr]
        return "{0:016b}".format(res)

    def Cinstr(self, line: str) -> str:
        res = "111" + self.comp(line) + self.dest(line) + self.jump(line)
        return res

    def comp(self, line: str) -> str:
        if "=" in line:
            tmp = line.partition("=")[2]
            return self.comp_map[tmp]
        return self.comp_map[line.partition(";")[0]]

    def dest(self, line: str) -> str:
        res = ""
        if "=" in line:
            res = line.partition("=")[0]
        return self.dest_map[res]

    def jump(self, line: str) -> str:
        if ";" in line:
            tmp = line.partition(";")[2]
            return self.jump_map[tmp]
        return self.jump_map[""]
