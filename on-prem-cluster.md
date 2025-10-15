
### Install elasticsearch on nodes
```sh
curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elasticsearch.list
sudo apt update
sudo apt install elasticsearch -y
```

### sync certificates and keystore from one node to the others
/etc/elasticsearch/certs/
/etc/elasticsearch/elasticsearch.keystore

### grant permission to data direcroty
```sh
chown -R elasticsearch:elasticsearch /mnt/elasticsearch
```

### Elasticsearch config file
/etc/elasticsearch/elasticsearch.yaml
```yml  
cluster.name: log-cluster
node.name: es01
path.data: /mnt/elasticsearch
path.logs: /var/log/elasticsearch
network.host: 0.0.0.0
discovery.seed_hosts: ["es01","es02","es03"]
cluster.initial_master_nodes: ["es01","es02","es03"]
node.roles: ["master", "data", "ingest"]
xpack.security.enabled: true
xpack.security.enrollment.enabled: true
xpack.security.http.ssl:
  enabled: true
  keystore.path: certs/http.p12
xpack.security.transport.ssl:
  enabled: true
  verification_mode: certificate
  keystore.path: certs/transport.p12
  truststore.path: certs/transport.p12
http.host: 0.0.0.0
```
change `node.name` for other nodes


### test elasticsearch
```sh
/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
curl -k -uelastic:pass https://127.0.0.1:9200
```

### install kibana on first node(optional)
```sh
/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
/usr/share/kibana/bin/kibana-setup
```
/etc/kibana/kibana.yml
```yml
# This section was automatically generated during setup.
server.port: 5601
server.host: 0.0.0.0
server.publicBaseUrl: https://kibana-log.mysite.io
elasticsearch.hosts: [https://es01:9200]
elasticsearch.serviceAccountToken: weeer523423f2fjx3uc342urc3ir8u3298x3
elasticsearch.ssl.certificateAuthorities: [/var/lib/kibana/ca_1760544533544.crt]
logging.appenders.file.type: file
logging.appenders.file.fileName: /var/log/kibana/kibana.log
logging.appenders.file.layout.type: json
logging.root.appenders: [default, file]
pid.file: /run/kibana/kibana.pid
xpack.fleet.outputs: [{id: fleet-default-output, name: default, is_default: true, is_default_monitoring: true, type: elasticsearch, hosts: [https://es01:9200], ca_trusted_fingerprint: bsdfwewqersdfaqw341}]
```
