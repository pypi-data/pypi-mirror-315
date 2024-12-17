<div align="center">

# LocalAssistant

**Locas - your local assistant**

[![][latest-release-shield]][latest-release-url]
[![][latest-commit-shield]][latest-commit-url]
[![][python-shield]][python-url]

[latest-release-shield]: https://badgen.net/github/release/Linos1391/LocalAssistant/development?icon=github
[latest-release-url]: https://github.com/Linos1391/LocalAssistant/releases/latest
[latest-commit-shield]: https://badgen.net/github/last-commit/Linos1391/LocalAssistant/main?icon=github
[latest-commit-url]: https://github.com/Linos1391/LocalAssistant/commits/main
[python-shield]: https://img.shields.io/badge/python-3.10+-yellow
[python-url]: https://www.python.org/downloads/

This AI is designed to be used in CLI.

</div>

# Which one should I use?
- [Pypi version](#download-by-pypi-recommended) is great, it works how I want. But if you want projects to be organized by using Anaconda / Docker... It sucks.
- [Github version](#download-by-github) solves that by using PATH, then user may modify `locas.cmd` file to use Anaconda. However, Unix user have to type `locas.cmd` instead of `locas`.

**Summary:** Window user may use Github version while Pypi is for Unix user. I still recommended Pypi though.

<br>

# Download by GitHub:

Visit [Github](https://github.com/Linos1391/LocalAssistant) and follow the instuctrion.

<br>

# Download by Pypi: (Recommended)

## Installing

Visit [PyTorch](https://pytorch.org/get-started/locally/) and download the version for your device.

```
# Example: (Me using WINDOW with CUDA 12.4)

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

After that, pip install the AI.

```
pip install LocalAssistant
```

<br>

## Preparing

### Chatting:

Before doing anything, we should download a model first.

```
locas download -n qwen Qwen/Qwen2.5-1.5B-Instruct 1
```

We will use `locas start` for AI's memory.

```
locas start
```

### Chatting with memory:

Before doing anything, we should download a model first.

```
locas download -n allmpnetv2 sentence-transformers/all-mpnet-base-v2 2
```

Memory only allow on `locas start`, remember that. Anyway, let's dive into it!

```
locas start -m
```

<br>

## Running

```
locas ...
```

Use `locas -h` for more.

<br>

## Removing

**Warning:** This act will delete all LocalAssistant files.

```
locas self-destruction pip
```

<br>

## Disclaimer

This AI was designed to communicating with Hugging Face models in CLI. Please do not use this AI for any unethical reasons. Any damages from abusing this application will not be the responsibility of the author.