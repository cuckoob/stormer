### Pypi Upload
```
python -m pip install -i https://pypi.douban.com/simple setuptools wheel
python -m pip install -i https://pypi.douban.com/simple twine
```
#### 1. 删除dist旧版本

#### 2. 修改版本号
```bash
vim setup.py
# or
sed -i "s/version='[0-9\.]*'/version='1.0.2'/g" setup.py
```

#### 3. 打包新版本build
```bash
python setup.py check
python setup.py sdist bdist_wheel
```

#### 4. 上传新版本
```bash
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```


