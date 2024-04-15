# img
cli to automatically download a collection of images or scrape them from a website

> [!NOTE]
> successor/version 2 of [PlayerG9/img](https://github.com/PlayerG9/img)

> [!CAUTION]
> This project is in an early phase and may be unstable or some features are missing.

<!-- TOC -->
* [img](#img)
  * [Help](#help)
    * [`img`](#img-1)
    * [`img collect`](#img-collect)
    * [`img get`](#img-get)
  * [Installation](#installation)
  * [Updating](#updating)
  * [Uninstall / Cleanup](#uninstall--cleanup)
<!-- TOC -->

## Help

> [!WARNING]
> Help may be outdated. Use `img --help` and `img <cmd> --help`.

### `img`

```text
usage: img [-h] [-v] {collect,get} ...

positional arguments:
  {collect,get}
    collect      Collects images. Manually add 1+ {0} to specify which numbers should increment for the next url
    get          similar to the `wget` program. used to download provided images

options:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

### `img collect`

```text
usage: img collect [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--max-skip MAX_SKIP] urls [urls ...]

positional arguments:
  urls                  URLs to collect from

options:
  -h, --help            show this help message and exit
  -c CONCURRENT, --concurrent CONCURRENT
                        Number of concurrent downloads (default: 3)
  --on-conflict {rename,skip,replace}
                        How to handle conflict of filenames during download (default: rename)
  --max-skip MAX_SKIP   How many url can be failing before stopping searching (default: 0)
```

### `img get`

```text
usage: img get [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] urls [urls ...]

positional arguments:
  urls                  URLs to download

options:
  -h, --help            show this help message and exit
  -c CONCURRENT, --concurrent CONCURRENT
                        Number of concurrent downloads (default: 3)
  --on-conflict {rename,skip,replace}
                        How to handle conflict of filenames during download (default: rename)
```

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
