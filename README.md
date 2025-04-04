# resolve single-node cluster yellow index health
```
PUT /myindex/_settings
{
  "index": {
    "number_of_replicas": 0
  }
}
```
define a template:
```
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
```
GET _cat/shards?v
GET _cat/nodes?v
GET _cluster/health
```
