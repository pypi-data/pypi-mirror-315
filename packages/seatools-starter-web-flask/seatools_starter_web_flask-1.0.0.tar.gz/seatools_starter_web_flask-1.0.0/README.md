# seatools flask 启动器

该框架必须和`seatools-starter-server-*`的包集成配合使用, 这里以`seatools-starter-server-uvicorn`为例

## 使用指南
1. 安装, `poetry add flask seatools-starter-server-uvicorn seatools-starter-web-flask`
2. 配置`config/application.yml`如下:
```yaml

seatools:
  server:
    # 此处为uvicorn参数配置
    uvicorn:
      host: 0.0.0.0
      port: 8000
      workers: 1
      reload: true
  # 此处为flask配置
  flask:
    # 与 Flask 参数一致
    import_name: seatools.ioc.server.app
    static_folder: static
    template_folder: templates
    ...
```
3. 使用, 通过定义ioc容器函数加载

```python
import abc
from seatools.ioc import Autowired, Bean
from flask import Flask

# 添加路由
from flask import Flask


@Bean
def api_controller(app: Flask):
    @app.get('/')
    def hello():
        return 'hello flask'


class Service(abc.ABC):
    
    def hello(self):
        raise NotImplementedError


# flask 与 seatools 的集成注入
@Bean
class ServiceA(Service):

    def hello(self):
        return "serviceA"


@Bean
def a2_router(app: Flask, service: Service):  # 具体注入方式见seatools

    @app.get('/service')
    def service():
        return service.hello() # return hello flask
```
3. 运行, 具体见`seatools-starter-server-*`, [`seatools-starter-server-uvicorn`](https://gitee.com/seatools-py/seatools-starter-server-uvicorn)
