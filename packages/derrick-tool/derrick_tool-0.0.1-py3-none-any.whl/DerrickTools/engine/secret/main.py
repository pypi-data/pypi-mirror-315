# -*- encoding: utf-8 -*-
"""
@File    :   main.py    
@Contact :   qiull@tellhow.com
@Author  :   Long-Long-Qiu
@Modify Time      @Version    @Description
------------      --------    -----------
2024/12/16 14:04                None
"""
import hashlib
import base64


class Encoder:
    @staticmethod
    def md5_encode(text):
        # 创建md5对象
        md5_obj = hashlib.md5()

        # 将文本转换为字节，因为md5()需要字节类型的输入
        md5_obj.update(text.encode('utf-8'))

        # 获取16进制的加密字符串
        md5_hash = md5_obj.hexdigest()

        return md5_hash

    @staticmethod
    def base64_encode(data):
        """将数据进行Base64编码。

        参数:
        data (str or bytes): 需要编码的数据，可以是字符串或字节串。

        返回:
        bytes: Base64编码后的字节串。
        """
        if isinstance(data, str):
            data = data.encode('utf-8')  # 将字符串转换为字节串
        return base64.b64encode(data)


class Decoder:

    @staticmethod
    def base64_decode(data):
        """将Base64编码的数据进行解码。

        参数:
        data (bytes): Base64编码的字节串。

        返回:
        str: 解码后的字符串。
        """
        decoded_bytes = base64.b64decode(data)
        return decoded_bytes.decode('utf-8')  # 将字节串转换为字符串


if __name__ == '__main__':
    md5_secret_text = Encoder.md5_encode("你好")
    print(md5_secret_text)

    origin_text = "Hello World"
    bs64_str = Encoder.base64_encode(origin_text)
    decoder_str = Decoder.base64_decode(bs64_str)
    print(bs64_str, decoder_str)
