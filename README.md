# requestx

## 简介(Intro)

requestx是模拟requests包，对urllib3进行的简单封装，目的是解决在测试过程中，post body部分会被url编码的问题。

在此基础上，添加了随机UA，如果指定UA，则不会启用。

requestx is a simple wrapping of urllib3, which imitates `requests`. The purpose of requestx is to solve the problem that the body was compulsorily url-encoded when send a post HTTP request.

Additionally, random UA is automatically enabled, if UA was not passed.

## 用法(Usage)

安装依赖
install the dependence
```shell
pip3 install urllib3
```

具体用法和requests差不多，但功能不够全

The usage is almost the same as requests, but not all methods are implemented.


整个文件夹扔项目里，
`from requestx.api import *` 
或者
`from some_dir import requestx`
就可以了
