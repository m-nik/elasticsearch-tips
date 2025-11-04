# elasticdump
```
npm install -g elasticdump
elasticdump --input=https://user:pass@elastic.mysite.io/index-name --output=/data/index-name.json --type=data
elasticdump --input=https://user:pass@elastic.mysite.io/index-name --output=/data/index-name.json --type=mapping
```

```
docker run --rm -v ./data:/data node:18-alpine sh
```
