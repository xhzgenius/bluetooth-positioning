# Bluetooth-positioning
北京大学计算机网络2023年春季学期课程Lab1：通过蓝牙嗅探装置进行设备定位。

## Build env
```
pip3 install msgpack msgpack_numpy mysql-connector-python matplotlib
```

## DataBase 
1. installation 
    - login to mysql 
    ```bash 
    sudo mysql -u root 
    ```
    - add an account;
    ```mysql
    mysql> CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
    mysql> GRANT ALL PRIVILEGES ON *.* TO 'user'@'localhost';
    ```
    - add a key.py with following attributes:
    ```python
    user = 'xxx'
    host = 'xxx'
    password = 'xxx'
    ``` 

2. API
```
1: signals (mac VARCHAR(255), rssi VARCHAR(255), date VARCHAR(255))
2: locations (x VARCHAR(255), y VARCHAR(255), date VARCHAR(255))
```

## Run 
```
python ./main.py 
```

## 排雷指南
##### 服务器寿命不超过2分钟，之后就死了
原因：单线程HTTPServer太垃圾，默认0.5秒处理一次请求，造成服务器堵塞。改成ThreadingHTTPServer光速解决。

##### MySQL Error 2013: Connection lost
原因：三个进程共用一个MySQL Cursor，导致不明错误。

##### get_signal等查询语句查询不出东西，误以为插入失败
原因：查询语句写炸了，插入是对的。查询语句里面的字符串值应该加引号！！！

## 实验记录
##### 坐标
小型地砖的斜边长度为53.2cm，黑盒子的横向距离为5个斜边，纵向距离为4个斜边。如图：

■

|

|

|

|

■ —— —— —— —— —— ■

也即横向距离为266.0cm，纵向距离为212.8cm。左上角黑盒子的水平高度是75.6cm，其它两个是0。因此三个黑盒子的坐标：

- (0, 212.8, 75.6)
- (0, 0, 0)
- (266.0, 0, 0)


