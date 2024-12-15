from ...option import *
from ...command import *
import shutil
import glob

def task_package_build(argv):
  for pattern in ["dist", "**/*.egg-info"]:
    for path in glob.glob(pattern, recursive = True):
      shutil.rmtree(path)
  Command(["python", "-m", "build"] + argv).run()

if __name__ == "__main__":
  task_package_build(sys.argv[1:])
