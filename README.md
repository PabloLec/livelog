
<div align="center">

<h1>livelog</h1>

<a href="https://img.shields.io/github/v/release/pablolec/livelog" target="_blank">
    <img src="https://img.shields.io/github/v/release/pablolec/livelog" alt="Release">
</a>

<a href="https://github.com/PabloLec/livelog/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/pablolec/livelog" alt="License">
</a>

<a href="https://github.com/PabloLec/livelog/actions/workflows/linux-tests.yml" target="_blank">
    <img src="https://github.com/PabloLec/livelog/actions/workflows/linux-tests.yml/badge.svg" alt="Linux">
</a>

<a href="https://github.com/PabloLec/livelog/actions/workflows/macos-tests.yml" target="_blank">
    <img src="https://github.com/PabloLec/livelog/actions/workflows/macos-tests.yml/badge.svg" alt="macOS">
</a>

<a href="https://github.com/PabloLec/livelog/actions/workflows/windows-tests.yml" target="_blank">
    <img src="https://github.com/PabloLec/livelog/actions/workflows/windows-tests.yml/badge.svg" alt="Windows">
</a>

</div>

---

`livelog` is yet another Python logger.

Its main purpose is to provide live logging for situation where logging to console is not possible. For example working on a GUI, TUI, a software plugin or a script instanciated from a different shell.

It provides a `Logger` object for your code and a built-in reader to see your logs in real time from another shell.
Even if its overall behavior is opinionated it does offer some customization.

## Installation

```
python3 -m pip install livelog
```

## Logging

#### Basics

In your code, create a `Logger` instance with:

``` python
from livelog import Logger

logger = Logger()
```

#### Parameters

`Logger` takes multiple optional arguments:

- `file` (str): Path for your logging file. Default is a file named "livelog.log" in your system tmp directory.
- `level` (str): Minimum level to be logged. Default is "DEBUG", you can also select "INFO", "WARNING", and "ERROR". Note that level filtering can also be done directly from the reader.
- `enabled` (bool): Whether logging is enabled or not. Default is True.
- `erase` (bool): Whether preexisting logging file should be erased or not. Default is True.

``` python
from livelog import Logger

logger = Logger(file= "/home/user/",
                level = "INFO",
                enabled = False,
                erase = False)
```

#### Methods

Use the following methods to write log messages:

- `logger.debug("message")`
- `logger.info("message")`
- `logger.warn("message")`
- `logger.error("message")`

``` python
from livelog import Logger

logger = Logger()
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warn("This is a warning message")
logger.error("This is an error message")
```

#### Attributes

You can get and set attributes after instantiation:

``` python
from livelog import Logger

logger = Logger(file="/tmp/file.log")
logger.debug("This will write to /tmp/file.log")

logger.file = "/tmp/another_file.log"
logger.debug("This will write to /tmp/another_file.log")

logger.level = "ERROR"
logger.debug("This debug message will not be written.")

logger.enabled = False
logger.error("Logging disabled. This error message will not be written.")
```

#### Singleton

`livelog` also provides a built-in singleton:

```your_first_file.py```
``` python
from livelog import LoggerSingleton


logger = LoggerSingleton(file="/tmp/file.log")
logger.debug("This will write to /tmp/file.log")
```

```another_file.py```
``` python
from livelog import LoggerSingleton


logger = LoggerSingleton()
# LoggerSingleton() returned the instance from your first file.
logger.debug("This will write to /tmp/file.log")
```

## Reading

Although you can access to your logging file like any other, you can use the provided reader.

If you did not specify a file for `Logger` simply use:
```
python3 -m livelog
```

`livelog` will read in real time the default log file.

#### Options

- `-f` or `--file` - Set the path of your logging file
- `-l` or `--level` - Set the minimum log level to be read.
- `--nocolors` - Do not print colors

*Example:*
```
python3 -m livelog -f /tmp/myfile.log -l INFO --nocolors
```
