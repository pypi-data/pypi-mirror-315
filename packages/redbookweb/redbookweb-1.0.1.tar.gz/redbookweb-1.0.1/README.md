# redbookweb
基于小红书 Web 端进行的请求封装

# 快速入门
由于 x-s 签名较复杂，因此使用 playwright 进行模拟浏览器行为进行 js 函数调用获取签名算法， 并且其中存在大量的环境检测的行为，因此需要使用到 stealth.min.js 进行绕过。

环境安装（本地调试）
```bash
pip3 install redbookweb # 下载 redbookweb 客户端包
pip3 install playwright # 下载 playwright
playwright install # 安装浏览器环境
curl -O https://cdn.jsdelivr.net/gh/requireCool/stealth.min.js/stealth.min.js # 下载 stealth.min.js
```

如果在本机启动 Flask 需要安装如下依赖
```bash
pip3 install flask
pip3 install gevent
pip3 install requests
```

redbookweb 客户端打包
```bash
pip3 install twine # 使用 twine 来上传你的包。首先需要安装 twine
python3 setup.py sdist
twine upload dist/* # 使用 twine 上传生成的包文件
```
