# resolve single-node cluster yellow index health
```http
PUT /myindex/_settings
{
  "index": {
    "number_of_replicas": 0
  }
}
```
define a template:
```http
PUT _index_template/myindex-template
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
GET _cat/shards?v
GET _cat/nodes?v
GET _cluster/health
```
