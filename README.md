# CLI-tool-for-Hack
Your task is to build a CLI tool that will simulate the execution of programs on the Hack hardware platform.

## Requirements
---
The CLI should:
   1. Get a `.hack` or `.asm` file.
   2. Run the program in the supplied file.
   3. Generate a `.json' file that will contain the final state of the RAM.
     - The file name must match the name of the supplied program.
   4. Take the number of processor cycles as an argument.

      
## Interface
---
Use python 3.11 to complete the task. Examples of running the program:

```sh
python -m n2t execute path/to/the/program.hack --cycles 10000
```

```sh
python -m n2t execute path/to/the/program.asm --cycles 10000
```

## Output data
---
After executing the program, you should generate a `.json` file, which will contain the final state of the RAM in JSON format.

```json
{
  "RAM": {
    "0": 259,
    "1": 1000,
    "2": 2000,
    "3": 0,
    "4": 0,
    "256": 123,
    "257": 0,
    "258": 12
  }
}
```

Note that the file only contains the values of the registers that the program has interacted with.

## Remarks
---
- The incoming file address can be absolute or relative.
- CLI should be operating system agnostic. (Must be compatible with Windows, Unix...)
- The output file must have the same name as the input file (just a different extension).
- You can assume that the input file contains a valid program.
- Screen and keyboard simulation will not be required.
