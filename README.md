# py-device-control-with-OCR

基于 [Tesseract OCR](https://github.com/UB-Mannheim/tesseract) 的识别结果，结合 pywin32 库实现 IO 设备的控制。

## 环境

- win10 22H2/win11 23H2
- python 3.11
- tesseract-ocr-w64 5.3.4.20240503
- PostgreSQL 15.7

## Tesseract 支持

使用 Tesseract at UB Mannheim 构建的 Windows 版本，在 [此处](https://github.com/UB-Mannheim/tesseract/wiki) 获取安装包。相关说明如下：

```sh
Tesseract installer for Windows

Normally we run Tesseract on Debian GNU Linux, but there was also the need for a Windows version. That's why we have built a Tesseract installer for Windows.

WARNING: Tesseract should be either installed in the directory which is suggested during the installation or in a new directory. The uninstaller removes the whole installation directory. If you installed Tesseract in an existing directory, that directory will be removed with all its subdirectories and files.
```

> [主仓库地址](https://github.com/tesseract-ocr/tesseract)

### Tesseract 使用准备

1、引入依赖

```py
poetry add pillow
poetry add pytesseract
```

2、指定命令路径

```py
# 设置pytesseract的tesseract命令路径
pytesseract.pytesseract.tesseract_cmd = r'C:\custom\Tesseract-OCR\tesseract.exe'
```

### Tesseract 中文识别支持

安装 Tesseract 过程中，`Additional language data` 增加的中文语言包下载会失败，不必勾选，在 [此处](https://github.com/tesseract-ocr/tessdata) 使用 SSH（git@github.com:tesseract-ocr/tessdata.git） 克隆整个仓库，将如下文件放到安装目录下 `tessdata` 即可：

```sh
chi_sim.traineddata（43327KB）
chi_sim_vert.traineddata（2414KB）
```

## IO 控制支持

```py
poetry add pywin32
```

在项目中即可引入 `import win32gui` 实现 IO 设备控制。

## 其他支持

SQLAlchemy：`sqlalchemy`

PostgreSQL database adapter ：`psycopg2`

## License

[MIT license](https://spdx.org/licenses/MIT)

## Changelog

### [0.1](https://github.com/inspiration-lab/hexo-uuidlink/compare/v0.0.1...v0.0.1) (2024-06-23)

- Initial release
