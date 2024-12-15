import os
import sys
from ...option import *
from ...command import *
from ...file import *

def init(optionParser):
  userName = optionParser.find_option_from_long_name("user-name").Value
  email = optionParser.find_option_from_long_name("email").Value
  description = optionParser.find_option_from_long_name("description").Value
  projectName = optionParser.find_option_from_long_name("project-name").value_if_not(os.path.basename(os.getcwd()))

  fileStatus = FileStatus(".gitignore")
  if not fileStatus.exists():
    with open(fileStatus.Path, "w", newline = "\n") as file:
      file.write("/dist\n")
      file.write("*.egg-info\n")
      file.write("__pycache__\n")
      fileStatus.done()
  fileStatus.print()

  fileStatus = FileStatus("MANIFEST.in")
  if not fileStatus.exists():
    with open(fileStatus.Path, "w", newline = "\n") as file:
      file.write("recursive-exclude tests *.py\n")
      fileStatus.done()
  fileStatus.print()

  fileStatus = FileStatus("README.md")
  if not fileStatus.exists():
    with open(fileStatus.Path, "w", newline = "\n") as file:
      file.write("""# {}\n""".format(projectName))
      fileStatus.done()
  fileStatus.print()

  fileStatus = FileStatus("setup.py")
  if not fileStatus.exists():
    with open(fileStatus.Path, "w", newline = "\n") as file:
      file.write("from setuptools import setup\n")
      file.write("setup()\n")
      fileStatus.done()
  fileStatus.print()

  directoryPath = """src/{}""".format(projectName)
  os.makedirs(directoryPath, exist_ok = True)

  os.makedirs("tests", exist_ok = True)
  fileStatus = FileStatus("""tests/test_{}.py""".format(projectName))
  if not fileStatus.exists():
    with open(fileStatus.Path, "w", newline = "\n") as file:
      file.write("""import {}\n\n""".format(projectName))
      file.write("""def test_{}():\n""".format(projectName))
      file.write("""  print("test_{}")\n""".format(projectName))
      fileStatus.done()
  fileStatus.print()

  fileStatus = FileStatus("pyproject.toml")
  if not fileStatus.exists():
    with open(fileStatus.Path, "w", newline = "\n") as file:
      file.write("""[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{projectName}"
version = "0.0.1"
authors = [{{name = "{userName}", email = "{email}"}}]
description = "{description}"
readme = "README.md"
requires-python = ">=3.13"
classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
]
dependencies = []

#[project.scripts]
#{projectName} = "{projectName}.cli:main"

[project.urls]
Homepage = "https://github.com/{userName}/{projectName}"
Issues = "https://github.com/{userName}/{projectName}/issues"

[tool.pytest.ini_options]
pythonpath = "src"
testpaths = ["tests"]

""".format(userName = userName, email = email, description = description, projectName = projectName))
      fileStatus.done()
  fileStatus.print()

  if not os.path.isfile("Pipfile"):
    Command(["pipenv", "--python", str(sys.version_info[0])]).run()
    Command(["pipenv", "install", "--dev", "pytest"]).run()

  Command(["pip", "install", "build"]).run()
  Command(["pip", "install", "twine"]).run()

if __name__ == "__main__":
  init(OptionParser([
    Option("u", "user-name", "{USERNAME}", "User name"),
    Option("e", "email", "{EMAIL}", "Email"),
    Option("description", "description", "{DESCRIPTION}", "Description"),
    Option("p", "project-name", "", "Project name")
  ]).parse())
