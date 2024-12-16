# pyemon
Python auxiliary tools

## Concept
Make your python work easier

## What is possible
1. Initialization work required to create your own package
2. Installing the package
3. Testing the package
4. Building the package
5. Uploading the package
6. Execute your own defined tasks

## Reason for development
- I want to easily create my own packages

## Versions

|Version|Summary|
|:--|:--|
|0.1.0|Release pyemon|

## Installation
### [pyemon](https://pypi.org/project/pyemon/)
`pip install pyemon`

## CLI
### package.init
Initialization work required to create your own package

`pyemon package.init -u USERNAME -e EMAIL -d DESCRIPTION`
```
[With value]
  -u|--user-name    {USERNAME}    # User name
  -e|--email        {EMAIL}       # Email
  -d|--description  {DESCRIPTION} # Description
  -p|--project-name               # Project name
```

### package.install
Installing the package

`pyemon package.install -d pytest`
```
[No value]
  -p|--pip   # PIP
  -d|--dev   # Development
  -t|--test  # TestPYPI
```

### package.test
Testing the package

`pyemon package.test`

### package.build
Building the package

`pyemon package.build`

### package.upload
Uploading the package

`pyemon package.upload`
```
[No value]
  -p|--pypi  # PYPI
```

## Task
### 1. Prepare pyetask.py file
**[pyetask.py]**
```python
from pyemon.task import *

class CamelizeTask(Task):
  def run(self, argv):
    for arg in argv:
      print(inflection.camelize(arg))
Task.set(CamelizeTask("<words>"))

class UnderscoreTask(Task):
  def run(self, argv):
    for arg in argv:
      print(inflection.underscore(arg))
Task.set(UnderscoreTask("<words>"))

class SingularizeTask(Task):
  def run(self, argv):
    for arg in argv:
      print(inflection.singularize(arg))
Task.set(SingularizeTask("<words>"))

class PluralizeTask(Task):
  def run(self, argv):
    for arg in argv:
      print(inflection.pluralize(arg))
Task.set(PluralizeTask("<words>"))
```

### 2. Execute tasks with CLI execution

`pyemon task.run camelize device_type`
```
DeviceType
```

`pyemon task.run underscore DeviceType`
```
device_type
```

`pyemon task.run singularize posts`
```
post
```

`pyemon task.run pluralize post`
```
posts
```
