# img
cli to automatically download a collection of images or scrape them from a website

> successor/version 2 of [PlayerG9/img](https://github.com/PlayerG9/img)


## installation

> [!CAUTION]
> This installation process is designed for **linux**.
> If you are under **Windows** you should use a [WSL](https://learn.microsoft.com/en-us/windows/wsl/install).
> If you are under **macOS** it should work but no guaranty.
> Some steps may need to be adjusted depending on your operating system.

> [!INFO]
> ```shell
> sudo apt install python3 git bash
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

## updating

```shell
$ cd ~/.local/src/toolbox-img/
$ git pull
$ ./scripts/make-build.sh
$ mv -f ./build/img ~/.local/bin/
$ img --version
0.0.0
```

## uninstall/cleanup

```shell
# uninstall
$ rm ~/.local/bin/img
# cleanup build files
$ rm -rf ~/.local/src/toolbox-img/build/*
# cleanup repository
$ rm -rf ~/.local/src/toolbox-img/
```
