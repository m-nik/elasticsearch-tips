# resolve single-node cluster yellow index health
```http
PUT /myindex/_settings
{
  "index": {
    "number_of_replicas": 0
  }
}
```
# settings of current indexes
```
GET /_all/_settings
GET /my-index-*/_settings
PUT /my-index-*/_settings
{
  "index": {
    "number_of_replicas": 0
  }
}
```
define a template:
```http
PUT /_index_template/myindex-template
{
  "index_patterns": ["myindex*"],
  "template": {
    "settings": {
      "number_of_replicas": 0
    }
  },
  "priority": 1
}
```

# Get shards, nodes, cluster health
```http
GET /_cat/shards?v
GET /_cat/shards/my-index-*?v
GET /_cat/nodes?v
GET /_cluster/health
```
