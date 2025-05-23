# Users
```
GET _security/user
```

# Roles
```
GET _security/role
PUT _security/role/rolename
{
    "cluster": [],
    "indices": [
      {
        "names": [
          "rolename*"
        ],
        "privileges": [
          "create",
          "create_doc",
          "create_index",
          "index",
          "read",
          "view_index_metadata",
          "write"
        ],
        "allow_restricted_indices": false
      }
    ],
    "applications": [],
    "run_as": [],
    "metadata": {},
    "transient_metadata": {
      "enabled": true
    }
}
```
