#!/usr/bin/env python3

import subprocess
import os
import inquirer
 
# Using system() method to
# execute shell commands
subprocess.run("cmake -Bbuild . && cmake --build build", shell=True)
# list all files in build directory and find ending with "-Main", use native python
allBuildFiles = os.listdir("build")
# filter out all files that do not end with "-Main"
allBuildFiles = [file for file in allBuildFiles if file.startswith("laby") ]

# sort files

allBuildFiles.sort()

questions = [
  inquirer.List('file',
                message="Which file do you want to run?",
                choices=allBuildFiles,
            ),
]

# get the answer from the user

answers = inquirer.prompt(questions)

# run the file

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   
# check if answer is not empty

if not answers:
      print("No file selected")
      exit()

print("Running " + color.BOLD + answers["file"] + color.END)


subprocess.run("./build/" + answers["file"], text=True)


