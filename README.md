# img
cli to automatically download a collection of images or scrape them from a website

> [!NOTE]
> successor/version 2 of [PlayerG9/img](https://github.com/PlayerG9/img)

> [!CAUTION]
> This project is in an early phase and may be unstable or some features are missing.

<!-- TOC -->
* [img](#img)
  * [Installation](#installation)
  * [Updating](#updating)
  * [Uninstall / Cleanup](#uninstall--cleanup)
<!-- TOC -->

## Installation

> [!WARNING]
> This installation process is designed for **linux**.
> If you are under **Windows** you should use a [WSL](https://learn.microsoft.com/en-us/windows/wsl/install).
> If you are under **macOS** it should work but no guaranty.
> Some steps may need to be adjusted depending on your operating system.

> [!IMPORTANT]
> This program requires some dependencies during the installation or for running.
> These dependencies are installed on most linux distributions.
> But if a step fails this could help.
> ```shell
> sudo apt install python3 git bash
> ```
> this project uses [pipenv](https://pypi.org/project/pipenv/) for dependency management.
> currently you need this installed for the build-script to work.
> ```shell
> $ python3 -m pip install --user pipenv
> ```

```shell
$ mkdir -p ~/.local/src/
$ cd ~/.local/src/
$ git clone https://github.com/utility-toolbox/img.git toolbox-img
$ cd toolbox-img/
$ ./scripts/make-build.sh
$ mv ./build/img ~/.local/bin/
$ img --version
0.0.0
```

## Updating

```shell
$ cd ~/.local/src/toolbox-img/
$ git pull
$ ./scripts/make-build.sh
$ mv -f ./build/img ~/.local/bin/
$ img --version
0.0.0
```

## Uninstall / Cleanup

```shell
# uninstall
$ rm ~/.local/bin/img
# cleanup build files
$ rm -rf ~/.local/src/toolbox-img/build/*
# cleanup repository
$ rm -rf ~/.local/src/toolbox-img/
```
