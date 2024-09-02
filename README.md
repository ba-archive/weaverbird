# weaverbird

数据更新管线。

主要数据更新来源：[SchaleDB](https://schaledb.com/)

## 使用

```shell
python3 weaverbird.py update -t test/students.yaml
```

### 参数
`--target, -t`: 配置文件路径

`--name-only`: 只更新学生名单，不抓取图片

`--image-path`: 图片保存路径