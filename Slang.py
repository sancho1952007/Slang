import re
import os
import sys
import platform
import colorama
from colorama import Fore

# Initialize Important Modules
colorama.init(autoreset=True)


# Variables
file=''
var={}
openFile=False
version='1.0'
path = os.path.dirname(os.path.realpath(__file__))


# Setting Global Internal Variables
var['this__version']=version


# Platform Configuration
Windows=False
Linux=False
Mac=False

if platform.system() == 'Windows':
    Windows=True
elif platform.system() == 'Linux':
    Linux=True
elif platform.system() == 'Darwin':
    Mac=True

try:
    for SlangFile in sys.argv[1:]:
        if os.path.isfile(os.path.join(path, SlangFile)):
            if  SlangFile.endswith('.sl') or SlangFile.endswith('.slang'):
                file = SlangFile
                openFile = True

                # Setting Internal Variables
                var['this__FilePath']=os.path.dirname(os.path.realpath(SlangFile))
                var['this__FileURL']=os.path.realpath(SlangFile)

            else:
                print(f'{Fore.RED}Error: Not A Slang File!')
        else:
            print(f"{Fore.RED}Error: File not found")

    
    def Run(code):
        if ":" in code:
            toReplace=re.findall('[:]\w+', code)
            sent=code
            for each in toReplace:
                try:
                    sent=sent.replace(each, var[each[1:]])
                except:
                    pass
            return Compile(sent.replace('\\n', '\n'))

        elif "#" in code:
            toReplace=code.split('#')
            sent=''.join(toReplace[0])
            return Compile(sent[:-1])

        else:
            return Compile(code)


    def Compile(code):
        if '=' in code:
            if "=" in code and '"' in code or "'" in code:
                variable=code.split('=')
                if ' ' in variable[0]:
                    return f'{Fore.RED}Error: Invalid Variable Name'
                else:
                    var[variable[0]]="".join(variable[1])[:-1][1:]

        elif len(list(code.replace(' ', '')))==0:
            None

        else:
            if code.startswith("say "):
                return code[4:].replace('\\n', '\n')

            elif code.startswith('ask '):
                return input(code[4:].replace('\n', '\n'))

            elif code.startswith('command '):
                os.system(code[8:])

            elif code.startswith('start '):
                if Windows:
                    os.system(f'start {code[5:]}')
                elif Linux:
                    os.system(f'xdg-open {code[5:]}')
                elif Mac:
                    os.system(f'open {code[5:]}')

            elif code.startswith("exit"):
                print(code[5:])
                sys.exit()

            else:
                return f"{Fore.RED}Error: {code.split(' ')[0]} Is Not Defined!"

    if openFile!=True:
        # Setting Internal Variables
        var['this__FilePath']=os.path.dirname(os.path.realpath(__file__))
        var['this__FileURL']=os.path.realpath(__file__)
        while True:
            compile=Run(input(">"))
            if compile!=None:
                print(compile)
            else:
                None
            print()
    
    else:
        with open(file, 'r') as readSlangFile:
            lines=readSlangFile.read()
            readSlangFile.close()

        for line in lines.split('\n'):
            if line.startswith('- '):
                None
                # Under Development
            else:
                compile=Run(line)
                if compile!=None:
                    print(compile)
                else:
                    None

except KeyboardInterrupt:
    print('exit')
    sys.exit()