## DataClient

### Introduction
this is a request tool which packaging method server

### Usage
1. init requester
```python
from stormer import Requester
requester = Requester(host="www.baidu.com")
# or
requester = Requester("http://www.baidu.com", redis_url="redis://127.0.0.1:6379/0", timeout=30 * 60)
# timeout: global cache timeout

```

2. register method
```python
requester.register(action="get", func="bd_download", uri="download", timeout=30 * 60)
# timeout: this requester cache timeout

```

3. call method
```python
rlt = requester.bd_download()
r_byte = rlt.bytes
print(r_byte)
```




