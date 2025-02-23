## 自动配置 selenium 4 所需 Chrome 驱动
这是一个基于 Python 实现的根据 Windows or Mac 所安装谷歌浏览器版本自动配置 selenium 4 所需 Chrome 驱动的脚本。

## 使用说明
将本仓库名为`selenium_chrome_driver_auto_install.py`的文件拉取到本地，放入到 selenium 爬虫同级目录下，按照以下代码进行配置即可成功运行。
```python
# selenium 4
import selenium_chrome_driver_auto_install
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService

driver = webdriver.Chrome(service=ChromiumService(selenium_chrome_driver_auto_install.install()))
driver.get(url='https://www.baidu.com/')
```
