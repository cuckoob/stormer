## DataClient

### Introduction
this is a request tool which packaging method server

### Usage
1. init requester
```python
from stormer import Requester

requester = Requester(
    "http://www.baidu.com", 
    redis_url="redis://127.0.0.1:6379/0", 
    redis_nodes="127.0.0.1:7000,127.0.0.1:7001,127.0.0.1:7002", 
    redis_password="",
    timeout=30 * 60
)
# timeout: global cache timeout

```

2. register method
```python
requester.register(
    action="get", 
    func="bd_download", 
    uri="/", 
    timeout=30 * 60
)
# timeout: this requester cache timeout

```

3. call method
```python
rlt = requester.bd_download()
r_byte = rlt.bytes
print(r_byte)
```




