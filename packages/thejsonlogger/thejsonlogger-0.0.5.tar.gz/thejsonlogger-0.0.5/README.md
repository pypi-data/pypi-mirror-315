# thejsonlogger

A simple JSON [structured logging](https://cloud.google.com/logging/docs/structured-logging) formatter for Python.

## Examples

### Configuration

`logging.conf`

```
[formatters]
keys=thejsonlogger

[formatter_thejsonlogger]
class=thejsonlogger.TheJSONLogger

[handlers]
keys=console

[handler_console]
class=logging.StreamHandler
args=(sys.stdout,)
formatter=thejsonlogger

[loggers]
keys=root

[logger_root]
level=INFO
handlers=console

[logger_<logger_name>]
level=INFO
handlers=console
```
