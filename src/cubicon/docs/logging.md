# Logging

By default platform is configured to use stdout and rotating file logs. See 
 `django.logging` section of `config.yml` configuration file:

```yaml
django:
  logging:    
    #config: logging.yml  # use optional external logging.yml instead of builtin configs if set
    level: WARNING
    root: logs/
    fileName: debug.log
    backupCount: 90
```

- `level` - logging level
- `root` - logs root directory
- `fileName` - log filename
- `backupCount` - backup count to keep

## Custom logging configuration

Set external logging configuration yaml file path in `django.logging.config`
 to customize logging. This config is **optional**. If this configuration 
 is set and file exists, it overrides default configuration described above. 
 Log configuration file is standard for python and described in 
 [logging.config](https://docs.python.org/2/library/logging.config.html#configuration-dictionary-schema) 
 docs. See also [django logging](https://docs.djangoproject.com/en/3.1/topics/logging/#configuring-logging). 

`config.yml`:
```yaml
django:
  logging:    
    config: logging.yml
```

Sample `logging.yml`:
```yaml
version: 1
disable_existing_loggers: false
formatters:
  simple:
    format: '{asctime} [{levelname}] {name}: {message}'
    datefmt: '%Y-%m-%d %H:%M:%S'
    style: '{'
handlers:
  console:
    class: logging.StreamHandler
    stream: ext://sys.stdout
    formatter: simple
    level: WARNING
  file:
    class: logging.handlers.TimedRotatingFileHandler
    filename: logs/debug.log
    when: midnight
    backupCount: 90
    delay: true
    interval: 1
    formatter: simple
    level: WARNING
loggers:
  '': 
    handlers:
      - console
      - file
  gateway:
    level: WARNING
  plugins:
    level: WARNING
```

### Logging to fluent

To configure logging to fluent-bit/fluentd add `FluentHandler` to handlers 
 section, add formatters and set handler for loggers.

```yaml
formatters:
  ...
  fluent:
    '()': fluent.handler.FluentRecordFormatter
handlers:
  ...
  fluent:
    class: fluent.asynchandler.FluentHandler    
    host: localhost
    port: 24224
    formatter: fluent
    tag: python
    level: WARNING
loggers:
  '':
    handlers:
      - console
      - fluent
  ...
```

To send additional LogRecord attributes configure formatter format

```yaml
formatters:
  ...
  fluent:
    '()': fluent.handler.FluentRecordFormatter
    style: '{'
    format:
      level: '{levelname}'
      ...
```

See available
 [LogRecord attributes](https://docs.python.org/2/library/logging.html#logrecord-attributes)

Logging to fluent requires `fluent-logger` library to be installed.

### Logging to logstash

To configure logging to logstash add `TCPLogstashHandler` to handlers section 
 and set handler for loggers.
```yaml
handlers:
  ...
  logstash:
    class: logstash.TCPLogstashHandler
    host: logstash
    port: 5000
    version: 1
    fqdn: False
    tags:
      - platform
    level: WARNING
loggers:
  '':
    handlers:
      - console
      - logstash
  ...
```

Logstash server should be configured to receive json messages. 
[filters-json-plugin](https://www.elastic.co/guide/en/logstash/current/plugins-filters-json.html)
can be used to expand message field into an actual data structure within 
the Logstash event.

Logging to logstash requires `python3-logstash` library to be installed.

### Logging to syslog

To configure logging to syslog add `SysLogHandler` to handlers section and set 
 handler for loggers.

```yaml
handlers:
  ...
  syslog:
    class: logging.handlers.SysLogHandler    
    address:
      - localhost  # syslog server host
      - 514        # syslog server port
    facility: user
    level: WARNING
loggers:
  '':
    handlers:
      - console
      - syslog
  ...
```

Some syslog servers may require RFC5424 compliant messages. Configure custom 
formatter or `syslog-rfc5424-formatter` library can be used for formatting.
