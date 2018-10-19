## bug fix robot

`Bug` 修复机器人是一个 `incoming` 机器人，用于将 `commit` 中 refer 的 `issue` 标记为解决。

## Develop
```bash
python3 -m virtualenv venv

echo  "export PIP_CONFIG_FILE=\"$(pwd)/../pip.conf\"" >> venv/bin/activate

echo "[global]
index-url = http://pypi.douban.com/simple
[install]
trusted-host = pypi.douban.com" > venv/pip.conf

source venv/bin/activate

pip install -r server/requirements.txt

```

## Usage
```
-g: repo-path
-u: repo-url
-w: webhook
-d: survival day, default 30
-k: the keyword about bump version
-f: the fir url to notifice download
```

## Contribute
developer: @Langxxx
