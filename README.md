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
```http
GET /_all/_settings
GET /my-index-*/_settings
PUT /my-index-*/_settings
{
  "index": {
    "number_of_replicas": 0
  }
}
```
define a template to change shards and replicas
```http
PUT /_index_template/myindex-template
{
  "index_patterns": ["myindex*"],
  "template": {
    "settings": {
      "number_of_replicas": 0,
      "number_of_shards": 3
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
GET /_index_template
```


# Asynchronous operations
```http
POST myindex/_delete_by_query?wait_for_completion=false
{
  "query": {
    "match_all": {}
  }
}

GET _tasks/abcd1234:56789
```


# Reindex
```http
POST _reindex
{
  "source": {
    "index": "index_name"
  },
  "dest": {
    "index": "new_index_name"
  }
}
```
