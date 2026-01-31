# resolve single-node cluster yellow index health
```http
PUT /myindex/_settings
{
  "index": {
    "number_of_replicas": 0
  }
}
```

# Delete indexes
```http
DELETE /index
```

# PUT vs POST

__PUT__: This HTTP method is used in Elasticsearch primarily for creating new documents or replacing existing documents. When you use PUT, you must specify the document ID. If a document with that ID already exists, it will be overwritten.

__POST__: This method can also be used to create new documents. However, if you do not specify the document ID, Elasticsearch automatically generates one for you. POST is also used to update parts of a document.



# Create index with static mapping
```http
PUT /library
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "author": {
        "type": "text"
      },
      "publication_year": {
        "type": "integer"
      }
    }
  }
}
```
### Dev tools query string items
- Headers
- Sorting
- Filter
```http
GET _cat/indices?v
GET _cat/indices?s=store.size:desc
GET _cat/indices?index=*,-.*
```

# settings of current indexes
```http
GET /_all/_settings
GET /my-index/_stats
GET /my-index/_mapping
GET /my-index/_count
GET /my-index*/_count
GET /my-index/_settings
GET /my-index-*/_settings
PUT /my-index-*/_settings
{
  "index": {
    "lifecycle": {
      "name": "delete-after-7-days"
    },
    "number_of_shards": "3",
    "number_of_replicas": "0"
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
```http
GET /my-index/_stats
```

# Get shards, nodes, cluster health
```http
GET /_cat/
GET /_cat/indices
GET /_cat/shards?v
GET /_cat/shards/my-index-*?v
GET _cat/shards?v&index=*,-.*
GET /_cat/nodes?v
GET /_cluster/health
GET /_cluster/health?pretty
GET /_cluster/stats
GET /_cluster/settings
GET /_index_template
```

# Create index and documents
```http
#create an index with dynamic mapping
PUT /products
# create with explicit mapping
PUT /products
{
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "product_id": {
                "type": "integer"
            },
            "name": {
                "type": "text"
            },
            "description": {
                "type": "text"
            },
            "price": {
                "type": "float"
            },
            "category": {
                "type": "text"
            },
            "brand": {
                "type": "text"
            }
        }
    }
}

POST /products/_doc/1
{
  "product_id": 100,
  "name": "Dish Washer",
  "price": 11.2
}

GET /products/_doc/1

# Query
GET /products/_search
GET /products/_search
{
  "query": {
    "match":{
      "name": "Dish"
    }
  }
}

# Replace the document
PUT /products/_doc/1
{
  "price": 11.9
}

#Update the document
POST /products/_doc/1/_update
{
  "doc":{
    "price": 11.9
  }
}

# Delete Document
DELETE /products/_doc/1
# Delete Index
DELETE /products

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

##### Remote reindex
```http
POST _reindex?wait_for_completion=false
{
        "source": {
            "remote": {
                "host": "http://address:port",
                "username": "user",
                "password": "password"
            },
            "index": "myindex"
        },
        "dest": {
            "index": "myindex",
            "op_type": "create"
        }
    }
```
- op_type prevents duplication
- wait_for_completion=false for asyn task
- remote host must be defined in elasticsearch configs:
  ```yml
  nodeSets:
    config:
      reindex.remote.whitelist: "IP:PORT"`
  ```
- reindex doesn't transfer mappings and settings:
```http
GET myindex/_mapping
GET myindex/_settings
```
```http
PUT myindex
{
  "mappings": {
    "properties": {
      ...
    }
  },
  "settings": {
    ...
  }
}
```
- Ignore conflicts and other errors:
```http
POST _reindex?wait_for_completion=false
{
        "conflicts": "proceed",
        ...
}
```

# Transient vs Persistent Settings
There are two types of cluster settings - transient and persistent.

Transient Settings
These settings can be changed dynamically using the Cluster Update Settings API. Examples include things like the number of replicas for an index or routing allocation rules.

Persistent Settings
These settings require a cluster restart to take effect. Examples include cluster name, data path location, and certain network settings.







# Cerate index and mapping using file
```
curl -X PUT "https://elk:9200/my-index" -k -H 'Content-Type: application/json' -d @create_index.json

curl -X PUT "https://elk:9200/my-index/_bulk?refresh=true" -H "Content-Type: application/x-ndjson" --data-binary @index_data.ndjson
```
