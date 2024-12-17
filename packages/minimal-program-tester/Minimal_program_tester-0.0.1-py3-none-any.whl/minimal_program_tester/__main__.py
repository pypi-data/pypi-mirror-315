
from minimal_program_tester import search_for_testcases, check_file

from colorama import init as colorama_init
from colorama import Fore, Back
from colorama import Style
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', "--exec",)
    parser.add_argument('-f', "--folder",)

    args = parser.parse_args()

    try:
        exe_path = args.exec
        tests_folder = args.folder
    except:
        print(f"{Back.RED}{Fore.YELLOW}ERROR:{Style.RESET_ALL} The executable, or test folder path is invalid" )

    print(f"{Back.MAGENTA}{Fore.YELLOW}Files loaded{Style.RESET_ALL}")


    testcases = search_for_testcases(tests_folder)

    print(f"{Back.MAGENTA}{Fore.YELLOW}Test cases parsed{Style.RESET_ALL}")

    show_diff = True

    counter = 0

    for number, testcase in testcases:
        print(f"TESTCASE[{number}]: ",end="")
        correct, differences = check_file(exe_path,tests_folder + r'\\' + testcase.input_file,tests_folder + r'\\' + testcase.output_file)
        if(correct):
            print(f"{Fore.GREEN}OK{Style.RESET_ALL}")
            counter += 1
        else:
            print(f"{Fore.RED}WA{Style.RESET_ALL}")
            if show_diff and len(differences):

                print(f"{Fore.YELLOW}{"="*50}")
                for line in differences:

                    print(f"=in line[{line[0]}]:")
                    print(f'    we got : "{line[2]}"')
                    print(f'    you got: "{line[1]}"')

                print(f"{"="*50}{Style.RESET_ALL}")


    print(f"{Back.BLUE}{Fore.YELLOW}CORRECT: {counter}/{len(testcases)} = {Back.YELLOW}{Fore.BLACK}{(float(counter)/len(testcases)):.2f}%{Style.RESET_ALL}")


