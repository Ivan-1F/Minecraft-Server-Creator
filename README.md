## Minecraft-Server-Creator

This is a command line tool to help you create Minecraft server easily

![snapshot](snapshot.png)

### Installation

MCSC is available in pypi. It can be installed via `pip` command

```shell
pip install mcservercreator
```
For Chinese users, you can added a `-i https://pypi.tuna.tsinghua.edu.cn/simple` prefix to the command to use [Tsinghua tuna mirror](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/) to speed up the installation

```shell
pip install mcservercreator -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Usage

Let’s say you are going to create a new server in a folder named `my_server`. Then you can run the following commands:

```shell
cd my_server
python -m mcservercreator
```

Then you will enter the CLI, answer the given questions and your server will be ready automatically

---

一个能让你更快更简单地创建 Minecraft 服务器的命令行工具

![snapshot](snapshot.png)

### 安装

MCSC 在 pypi 中可用。它可以通过 pip 命令安装：

```shell
pip install mcservercreator
```

对于国内用户，你可以在 pip 指令的末尾添加 `-i https://pypi.tuna.tsinghua.edu.cn/simple` 后缀来使用 [清华 pypi 镜像](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/) 来加速 MCSC 的下载安装。

```shell
pip install mcservercreator -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 使用

假设你想在 `my_server` 中创建一个新的服务端，那么你可以运行以下指令：

```shell
cd my_server
python -m mcservercreator
```

然后你将会进入 CLI，回答给出的问题，服务端就会自动创建了