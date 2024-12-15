from ...option import *
from ...command import *

def upload(optionParser):
  repository = optionParser.find_option_from_long_name("pypi").value_by_bool("pypi", "testpypi")
  Command(["python", "-m", "twine", "upload", "--repository", repository, "dist/*"]).run()

if __name__ == "__main__":
  upload(OptionParser([Option("p", "pypi", None, "PYPI")]).parse())
