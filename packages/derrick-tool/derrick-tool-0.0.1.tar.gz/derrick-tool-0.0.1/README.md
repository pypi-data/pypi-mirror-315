## DerrickTools工具
提供包含但不限于各种加密算法的实现、时间戳和各种格式时间字符串之间的转换等功能

### 安装

```shell
pip install derrick-tools
```

### 使用

+  #### 日期时间工具

  ```python
  from DerrickTools.engine.datetime.main import DateTimeTool    # 导入function_tool_derrick.UsualTool下的DateTimeTool类
  
  if __name__ == '__main__':
      print(DateTimeTool.timestamp2time(1681721029)) # 打印 2023-04-17 16:43:49
      print(DateTimeTool.time2timestamp('2023-04-17 16:43:49')) # 打印 1681721029
  
      ret = DateTimeTool.get_range_of_date_by_str('2022-02-02 15:30:28', formatter='%Y-%m-%d %H:%M:%S', tsType=TimestampType.MILLISECOND)
      print(ret) # 打印 [1643731200000, 1643817599999]
  
      print(DateTimeTool.get_difference_between_time('2024-02-20 08:30:00', '2024-02-20 08:31:30'))   # 打印90
  ```

  

+ #### 加密算法工具

  ```python
  from DerrickTools.engine.secret.main import Encoder, Decoder
  md5_secret_text = Encoder.md5_encode("你好")
  print(md5_secret_text)
  
  origin_text = "Hello World"
  bs64_str = Encoder.base64_encode(origin_text)
  decoder_str = Decoder.base64_decode(bs64_str)
  print(bs64_str, decoder_str)
  ```

  
