
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
