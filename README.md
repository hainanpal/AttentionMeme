# AttentionMeme
用来生成“注意！本游戏包含以下要素”的梗图


### 准备素材

目录结构如下

        your_directory/
        ├── config.yaml
        ├── title.png
        ├── 1-xxxx.png
        ├── 2-xxxx.png

* `config.yaml`配置各种布局参数，参考`/example/arkham`中的内容
* `title.png`是标题左侧的图标
* 每个梗的图片以`编号-文字`的方式命名
  * 编号必须是整数，仅用来排序，可以重复
  * 图片不必是正方形，会做裁剪
* 支持`png`、`jpg`、`jpeg`格式的图片

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行
```bash
python layout.py --input_dir <your_directory>
```

### 生成效果

![示例](/example/arkham/output.png)