
### Install
```sh
curl -fsSL https://fluentd.cdn.cncf.io/sh/install-ubuntu-noble-fluent-package6-lts.sh | sh
```
/etc/fluent/fluentd.conf
```
<source>
  @type tail
  path /var/log/remote/*.log
  pos_file /var/log/remote-log.pos
  tag esxi
  read_from_head true
  <parse>
    @type regexp
    # Capture timestamp, host, program, pid, message
    expression /^(?<esxi_time>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z) (?<host>\S+) (?<program>\S+)\[(?<pid>\d+)\]: (?<message>.*)$/
  </parse>
</source>
<filter esxi>
  @type record_transformer
  enable_ruby true
  <record>
    hostname ${record["host"] || record["hostname"]}
    program ${record["program"] || "unknown"}
  </record>
</filter>
<match esxi>
  @type elasticsearch
  host IP_OR_HOSTNAME
  port PORT
  user _user_
  password _password_
  scheme https
  ssl_verify false
  logstash_format true
  logstash_prefix esxi-dev
  type_name _doc
  tag_key program
</match>
```

```sh
touch /var/log/remote-log.pos
chown _fluentd:_fluentd /var/log/remote-log.pos
```


```json
{
  "index": {
    "lifecycle": {
      "name": "delete-after-60-days"
    },
    "number_of_shards": "3",
    "number_of_replicas": "0"
  }
}
```
```json
{
  "dynamic_date_formats": [
    "strict_date_optional_time",
    "yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z",
    "date_optional_time",
    "basic_date_time"
  ],
  "dynamic_templates": [],
  "properties": {
    "hostname": {
      "type": "text",
      "fields": {
        "keyword": {
          "ignore_above": 256,
          "type": "keyword"
        }
      }
    },
    "@timestamp": {
      "format": "strict_date_optional_time",
      "type": "date"
    },
    "host": {
      "type": "text",
      "fields": {
        "keyword": {
          "ignore_above": 256,
          "type": "keyword"
        }
      }
    },
    "pid": {
      "type": "text",
      "fields": {
        "keyword": {
          "ignore_above": 256,
          "type": "keyword"
        }
      }
    },
    "program": {
      "type": "text",
      "fields": {
        "keyword": {
          "ignore_above": 256,
          "type": "keyword"
        }
      }
    },
    "message": {
      "type": "text",
      "fields": {
        "keyword": {
          "ignore_above": 256,
          "type": "keyword"
        }
      }
    },
    "esxi_time": {
      "format": "strict_date_optional_time",
      "type": "date"
    }
  }
}
```
