import subprocess
from collections import defaultdict
from os import listdir
from os.path import isfile, join
import re


def check_file(exe_path,input_path,output_path):

 
    try:
        with open(input_path, 'r') as input_file:
            result = subprocess.run(
                [exe_path],               # Command to run
                stdin=input_file,         # Redirect a.txt to stdin
                capture_output=True,      # Capture stdout and stderr
                text=True                 # Decode stdout and stderr as strings
            )
        stdout_lines = result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print("Error")

    with open(output_path,'r') as output_file:
        file_lines = output_file.read().splitlines()

    flag = True
    differences = []
    for line_number,(s_line, f_line) in enumerate(zip(stdout_lines, file_lines)):
        if s_line != f_line:
            differences.append(tuple([line_number, s_line, f_line]))
            flag = False


    return flag, differences

class TestCase:
    def __init__(self,input_file = None, output_file = None):
        self.input_file = input_file
        self.output_file = output_file
        self.correct = False

    def has_input_and_output(self) -> bool:
        if self.input_file is not None and self.output_file is not None:
            return True

        return False

    def correct(self):
        self.correct = True

def search_for_testcases(folder_path) -> defaultdict:

    testcases_dict = defaultdict(TestCase)
    files = list(filter(lambda x: True if len(x) >= 4 and x[-4:] == ".txt" else False,[f for f in listdir(folder_path) if isfile(join(folder_path, f))]))

    for file in files:
        """
        Format namenumber-in(-out).txt
        -in/-out has to be at the end
        the first number will be checked
        and both -in and -out
        """
        file_number = re.findall(r'\d+', file)

        if len(file_number) == 0:
            continue

        file_number = int(file_number[0])

        contains_in = re.search("-in",file)
        contains_out = re.search("-out",file)

        #print(file_number, contains_in, contains_out)

        if contains_in is not None :

            span = contains_in.span()
            if span[0] == len(file)-7 and span[1] == len(file)-4:
                testcases_dict[file_number].input_file = file
                continue

        if contains_out is not None :

            span = contains_out.span()
            if span[0] == len(file)-8 and span[1] == len(file)-4:
                testcases_dict[file_number].output_file=file

                continue

    return list(filter(lambda x: x[1].has_input_and_output(), testcases_dict.items()))

