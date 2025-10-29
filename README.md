# MobaXterm 密钥生成器 (版本 2)

## 简介

这是一个优化版的 MobaXterm 授权密钥生成脚本。该脚本可以帮助生成 MobaXterm 终端工具的试用授权。

## 改进亮点

1. 使用 argparse 模块改进命令行参数解析，支持更多选项
2. 增加了完整的类型注解，提高代码可读性
3. 增强错误处理，包括版本格式验证和异常捕获
4. 支持自定义输出文件路径
5. 支持选择不同的许可证类型（专业版、教育版、个人版）
6. 支持指定许可证数量
7. 优化代码结构，将主逻辑移至 main() 函数
8. 修正了原脚本中的拼写错误

## 作者信息

- 原始作者: Double Sine
- 修改者: KZ&Trae AI IDE
- 许可证: GPLv3

## 使用方法

### 基本命令格式

python MobaXterm-Keygen-v2.py <用户名> <版本号> [选项]

### 参数说明

- <用户名> : 授权的用户名称
- <版本号> : MobaXterm 的版本号，例如 10.9

### 可选参数

- --type <类型> : 许可证类型（professional/educational/personal），默认为 professional
- --count <数量> : 许可证数量，默认为 1
- --output <文件路径> : 输出文件路径，默认为 Custom.mxtpro

### 使用示例

# 基本使用

python MobaXterm-Keygen-v2.py "用户名" 10.9

# 指定许可证类型和数量

python MobaXterm-Keygen-v2.py "用户名" 10.9 --type educational --count 5

# 指定输出文件

python MobaXterm-Keygen-v2.py "用户名" 10.9 --output my_license.mxtpro

## 安装说明

生成授权文件后，将其复制到 MobaXterm 的安装目录，通常为 `C:\Program Files (x86)\Mobatek\MobaXterm`。

## 注意事项

1. 本工具仅供学习研究使用，请支持正版软件。
2. 生成的授权文件是一个 zip 压缩包，包含加密的授权信息。
3. 若需使用自定义设置，可以将设置导出为 MobaXterm customization.custom 文件，然后与生成的授权文件合并。

## 许可证信息

本项目基于 GNU General Public License v3.0 许可发布。详细信息请参阅 LICENSE 文件。
