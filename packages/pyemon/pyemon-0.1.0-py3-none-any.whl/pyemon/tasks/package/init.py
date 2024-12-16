from ...task import *
from ...status import *

class PackageInitTask(Task):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.OptionParser = OptionParser([
      Option("u", "user-name", "{USERNAME}", "User name"),
      Option("e", "email", "{EMAIL}", "Email"),
      Option("description", "description", "{DESCRIPTION}", "Description"),
      Option("p", "project-name", "", "Project name")
    ])

  def run(self, argv):
    self.OptionParser.parse(argv)
    userName = self.OptionParser.find_option_from_long_name("user-name").Value
    email = self.OptionParser.find_option_from_long_name("email").Value
    description = self.OptionParser.find_option_from_long_name("description").Value
    projectName = self.OptionParser.find_option_from_long_name("project-name").value_if_not(os.path.basename(os.getcwd()))

    fileStatus = FileStatus(".gitignore")
    if not fileStatus.exists():
      with open(fileStatus.Path, "w", newline = "\n") as file:
        file.write("/dist\n")
        file.write("*.egg-info\n")
        file.write("__pycache__\n")
        fileStatus.done()
    print(fileStatus)

    fileStatus = FileStatus("MANIFEST.in")
    if not fileStatus.exists():
      with open(fileStatus.Path, "w", newline = "\n") as file:
        file.write("recursive-exclude tests *.py\n")
        fileStatus.done()
    print(fileStatus)

    fileStatus = FileStatus("README.md")
    if not fileStatus.exists():
      with open(fileStatus.Path, "w", newline = "\n") as file:
        file.write("""# {}\n""".format(projectName))
        fileStatus.done()
    print(fileStatus)

    fileStatus = FileStatus("setup.py")
    if not fileStatus.exists():
      with open(fileStatus.Path, "w", newline = "\n") as file:
        file.write("from setuptools import setup\n")
        file.write("setup()\n")
        fileStatus.done()
    print(fileStatus)

    directoryPath = """src/{}""".format(projectName)
    os.makedirs(directoryPath, exist_ok = True)

    os.makedirs("tests", exist_ok = True)
    fileStatus = FileStatus("""tests/test_{}.py""".format(projectName))
    if not fileStatus.exists():
      with open(fileStatus.Path, "w", newline = "\n") as file:
        file.write("""import {}\n\n""".format(projectName))
        file.write("""def test_{}():\n""".format(projectName))
        file.write("""  print("TODO: test_{}()")\n""".format(projectName))
        fileStatus.done()
    print(fileStatus)

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
    print(fileStatus)

    if not os.path.isfile("Pipfile"):
      Command(["pipenv", "--python", str(sys.version_info[0])]).run()
      Command(["pipenv", "install", "--dev", "pytest"]).run()

    Command(["pip", "install", "build"]).run()
    Command(["pip", "install", "twine"]).run()
Task.parse_if_main(__name__, PackageInitTask())
