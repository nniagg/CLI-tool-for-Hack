from __future__ import annotations

import json
import os
from ctypes import c_short
from dataclasses import dataclass
from typing import Any, Iterable, List

from n2t.core.assembler.facade import Assembler


@dataclass
class HackSimulator:
    registrebi = [0] * 32768
    gamoyenebuli = [False] * 32768
    d_registri: int = 0
    a_registri: int = 0

    @classmethod
    def load_from(cls, filename: str) -> HackSimulator:
        return cls(filename)

    def prog(self, filename: str, cycles: int) -> None:
        if filename.endswith(".hack"):
            input = self.readFileHack(filename)
        else:
            input = self.readFileAsm(filename)
        outputList = self.gashveba(input, cycles)
        jList = self.jsonWrite(outputList)
        outname = os.path.splitext(filename)[0] + ".json"
        with open(outname, "w") as file:
            json.dump(jList, file, indent=2)

    def jsonWrite(self, lst):
        dicti = {"RAM": {}}
        for item in lst[1:]:
            cnt, n = item.split(":")
            dicti["RAM"][cnt] = int(n)
        return dicti

    def readFileHack(self, filename):
        return self.readFile(filename)

    def readFileAsm(self, filename):
        ass = Assembler.create()
        ass_cd = list(self.readFile(filename))
        return ass.assemble(ass_cd)

    def readFile(self, filename):
        with open(filename, "r") as file:
            for line in file:
                yield line.replace(" ", "").strip()

    def gashveba(self, xazebi: Iterable[str], cycles: int) -> List[str]:
        instr = list(iter(xazebi))
        n = 0
        for i in range(cycles):
            if n >= len(instr):
                continue
            n = self.maint(instr[n], n)
        result = ["RAM:"]
        for i, n in enumerate(self.registrebi):
            if self.gamoyenebuli[i]:
                line = f"{n if n >= 0 else 2**16 + n}"
                result.append(f"{i}: {line}")
        return result

    def maint(self, xazi: str, n: int) -> Any:
        if xazi.startswith("0"):
            self.a_registri = int(xazi[1:], 2)
            return n + 1

        xazis_nawili = xazi[3:][:7]
        val = c_short(self.get_comp(xazis_nawili)).value

        jump = xazi[3:][10:]
        dest = xazi[3:][7:10]

        if dest != "000":
            self.save_value(dest, val)

        if jump == "000":
            return n + 1
        else:
            return self.simulate_jump_instruction(jump, val, n)

    def get_comp_helper1(self, flag):
        if flag == "0":
            return self.a_registri
        else:
            return self.registrebi[self.a_registri]

    def get_comp_helper2(self, flag):
        if flag == "0":
            return ~self.a_registri
        else:
            return ~(self.registrebi[self.a_registri])

    def get_comp_helper3(self, flag):
        if flag == "0":
            return -self.a_registri
        else:
            return -self.registrebi[self.a_registri]

    def get_comp_helper4(self, flag):
        if flag == "0":
            return self.a_registri + 1
        else:
            return self.registrebi[self.a_registri] + 1

    def get_comp_helper5(self, flag):
        if flag == "0":
            return self.a_registri - 1
        else:
            return self.registrebi[self.a_registri] - 1

    def get_comp_helper6(self, flag):
        if flag == "0":
            return self.d_registri + self.a_registri
        else:
            return self.d_registri + self.registrebi[self.a_registri]

    def get_comp_helper7(self, flag):
        if flag == "0":
            return self.d_registri - self.a_registri
        else:
            return self.d_registri - self.registrebi[self.a_registri]

    def get_comp_helper8(self, flag):
        if flag == "0":
            return self.a_registri - self.d_registri
        else:
            return self.registrebi[self.a_registri] - self.d_registri

    def get_comp_helper9(self, flag):
        if flag == "0":
            return self.a_registri & self.d_registri
        else:
            return self.registrebi[self.a_registri] & self.d_registri

    def get_comp(self, xazi: str) -> Any:
        flag = xazi[0]
        xazi = xazi[1:]
        if xazi == "101010":
            return 0
        if xazi == "111111":
            return 1
        if xazi == "111010":
            return -1
        if xazi == "001100":
            return self.d_registri
        if xazi == "110000":
            return self.get_comp_helper1(flag)
        if xazi == "001101":
            return ~self.d_registri
        if xazi == "110001":
            return self.get_comp_helper2(flag)
        if xazi == "001111":
            return -self.d_registri
        if xazi == "110011":
            return self.get_comp_helper3(flag)
        if xazi == "011111":
            return self.d_registri + 1
        if xazi == "110111":
            return self.get_comp_helper4(flag)
        if xazi == "001110":
            return self.d_registri - 1
        if xazi == "110010":
            return self.get_comp_helper5(flag)
        if xazi == "000010":
            return self.get_comp_helper6(flag)
        if xazi == "010011":
            return self.get_comp_helper7(flag)
        if xazi == "000111":
            return self.get_comp_helper8(flag)
        if xazi == "000000":
            return self.get_comp_helper9(flag)
        if flag == "0":
            return self.a_registri | self.d_registri
        return self.registrebi[self.a_registri] | self.d_registri

    def save_value_helper(self, jump, n):
        self.registrebi[self.a_registri] = n
        self.gamoyenebuli[self.a_registri] = True
        if jump == "011":
            self.d_registri = n
        elif jump == "101":
            self.a_registri = n

    def save_value_helper2(self, n):
        self.d_registri = n
        self.registrebi[self.a_registri] = n
        self.gamoyenebuli[self.a_registri] = True
        self.a_registri = n

    def save_value(self, jump: str, n: Any) -> None:
        if jump == "010":
            self.d_registri = n
        elif jump == "001" or jump == "011" or jump == "101":
            self.save_value_helper(jump, n)
        elif jump == "100":
            self.a_registri = n
        elif jump == "110":
            self.a_registri = n
            self.d_registri = n
        else:
            self.save_value_helper2(n)

    def helper1(self, jump, cnt):
        if jump > 0:
            return self.a_registri
        else:
            return cnt + 1

    def helper2(self, jump, cnt):
        if jump == 0:
            return self.a_registri
        else:
            return cnt + 1

    def helper3(self, jump, cnt):
        if jump >= 0:
            return self.a_registri
        else:
            return cnt + 1

    def helper4(self, jump, cnt):
        if jump < 0:
            return self.a_registri
        else:
            return cnt + 1

    def helper5(self, jump, cnt):
        if jump != 0:
            return self.a_registri
        else:
            return cnt + 1

    def helper6(self, jump, cnt):
        if jump <= 0:
            return self.a_registri
        else:
            return cnt + 1

    def simulate_jump_instruction(self, jump_type: str, jump: Any, cnt: int) -> Any:
        ans: Any = self.a_registri
        if jump_type == "110":
            return self.helper6(jump, cnt)
        if jump_type == "100":
            return self.helper4(jump, cnt)
        if jump_type == "010":
            return self.helper2(jump, cnt)
        if jump_type == "001":
            return self.helper1(jump, cnt)
        if jump_type == "011":
            return self.helper3(jump, cnt)
        if jump_type == "101":
            return self.helper5(jump, cnt)
        return ans
