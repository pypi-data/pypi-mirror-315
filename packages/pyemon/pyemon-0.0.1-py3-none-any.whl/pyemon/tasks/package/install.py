from ...option import *
from ...command import *

def upload(optionParser):
  args = [
    optionParser.find_option_from_long_name("pip").value_by_bool("pip", "pipenv"),
    "install"
  ]
  if optionParser.find_option_from_long_name("dev").Value:
    args.append("--dev")
  if optionParser.find_option_from_long_name("test").Value:
    args.append("-i https://test.pypi.org/simple/")
  #Command(args + optionParser.Argv.List).run()

if __name__ == "__main__":
  upload(sys.argv[1:])
