<!--
 * @Author: your name
 * @Date: 2022-02-05 00:15:52
 * @LastEditTime: 2022-02-28 14:09:40
 * @LastEditors: Please set LastEditors
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: \PyPackage\cjen\README.md
-->

该项目封装了测试人员写自动化代码的常用功能作为装饰器，
目标是能让测试人员更关注业务逻辑的实现，隐藏和业务逻辑无关的细节。
GitHub地址：https://github.com/thcpc/cjen

# Release 1.0.1
get_mapping, put_mapping, post_mapping, delete_mapping, upload_mapping 增加json_clazz参数，作用同operate.json.factory

# Release 1.0.2
- 1. 修改metaMysql 没有数据时，是警告信息而不是错误信息

- 2. 方便批量检查，增加了 context["cursor"]

# Release 1.0.2b
- 1. 修改了创建metaMysql后，直接释放数据库连接池（临时修改方案）

# Release 1.0.3
- 1. 上传的文件支持sql

# Release 1.0.4
- 1. 修改了文件的判断

# Release 1.0.4.1b
- 1. 测试http请求的写日志文件

# Release 1.0.4.2b
- 1. fix a bug
  
# Release 1.0.5
- 1. 增加了http请求的日志文件

# Release 1.0.5.2
- 1. 增加了封装操作步骤
  
# Release 1.0.5.3
- 1. 修复了文件下载日志的bug 和对是否是文件下载的判断

# Release 1.0.5.4
- 1. 取消了文件下载请求响应的日志
  
# Release 1.0.5.5
- 1. 增加了Step的装饰器

# Release 1.0.5.6
- 1. bug：不管step是否运行都会注册到BigTangerine
     修复：调用接口时才会注册到BigTangerine中

# Release 1.0.5.7
- 1. scenario 中的step 都应该使用相同的service, 所以在构造函数中增加了service参数，同时兼容以前的方法

# Release 1.0.5.8
- 1. 取消FormData中,文件作为必填项

# Release 1.0.5.9
- 1. 修复了upload 会修改service中的全局headers
  
# Release 1.0.6.0
- 1. 增加了测试装饰器

# Release 1.0.6.1
- 1. 在Scenario中增加了测试用例的注册机制
# Release 1.0.6.2
- 1. 修复一些低级错误

# Release 1.0.7
- 1 . 针对 mysql 增加可通过函数参数传递查询参数，而不是一定需要通过上下文传递

# Release 1.0.7
- 1 . 修改查询参数为空时，设置查询参数为
# Release 1.0.9
- 1 . xlsx读取装饰器
- 2 . list_eql 函数
# Release 1.0.10
- 1 . 增加了通用数据结构 树
# Release 1.0.11
- 1 . xlsx 读取装饰器，支持在函数中指定文件路径
# Release 1.0.12
- 1 . property 校验装饰器
- # Release 1.0.13
- 1 . 增加DBBigTangerine
- # Release 1.0.14
- 1 . 修复了DatabaseInfo port的BUG

- # Release 1.0.15
- 1 . 增加对数据库字段byte转为Bool

- # Release 1.0.16 废弃
- 1 . 增加对数据库字段byte转为Bool

- # Release 1.0.17　废弃
- 1 . 增加对数据库字段byte转为Bool


- # Release 1.0.18
- 1 . 修复提交的BUG，增加打印参数，控制解决IO占用的问题