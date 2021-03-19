# esimportndjson

`esimportndjson` is a simple script which can help importing NDJSON files into Elasticsearch.

![screenshot](https://user-images.githubusercontent.com/21986859/111720569-0fe28300-8856-11eb-8b8d-36a763045423.png)

## Usages

```console
usage: esimport [-h] -i INPUT --index INDEX [--host HOST] [--port PORT]
                [-u USER] [-p PASSWORD] [-s] [--insecure]
                [--disable-file-length-count]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file path or input directory path (default:
                        None)
  --index INDEX         name of the Elasticsearch index to import into
                        (default: None)
  --host HOST           Elasticsearch instance hostname or IP (default:
                        127.0.0.1)
  --port PORT           Elasticsearch listening port (default: 9200)
  -u USER, --user USER  Elasticsearch username (default: None)
  -p PASSWORD, --password PASSWORD
                        Elasticsearch password (default: None)
  -s, --ssl             enable SSL (default: False)
  --insecure            disable SSL certificate verifications (default: True)
  --disable-file-length-count
                        do not count file length in progress bar, may save
                        some time for large files (default: False)
```
