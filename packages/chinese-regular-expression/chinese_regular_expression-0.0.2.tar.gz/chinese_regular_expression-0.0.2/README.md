## 简述

正则表达式（regular expression）读写不易，此 API 尝试改进。

现在处于调研与规划中，相关文档编写中：
- [功能](https://gitee.com/Program-in-Chinese/regular-expression/blob/master/文档/功能.md)
- [设计](https://gitee.com/Program-in-Chinese/regular-expression/blob/master/文档/设计.md)，包括 API 细节与示例
- 测试：`$ pytest`

设想的简单演示：
```python
# 对应 r'\$?[^\\\)]'
序列("$").可无().不是(反斜杠, 右小括号).表达()

# r'(\")((?<!\\)\\\1|.)*?\1'
分段(双引号)
  .分段(
    任一(
      序列(反斜杠, 引用分段(1)).前面不是(反斜杠),
      序列(非换行字符)
    )
  ).若干().不贪()
  .引用分段(1)
```

如各位有“如何写 XXX 这样的正则表达式”之类的问题，欢迎提 issue。普遍出现的需求将纳入设计与之后的测试。

## 渊源

- 2020-12-03 [正则表达式 API 技术验证与设计细化](https://zhuanlan.zhihu.com/p/328550803)
- 2020-11-30 [用中文 API 让正则表达式更易读写？](https://zhuanlan.zhihu.com/p/323940002)