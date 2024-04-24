img(1) -- cli to automatically download a collection of images or scrape them from a website
=============================================

## SYNOPSIS

- `img [-h] [-v] {collect,scrape,get} ...`
- `img collect [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--timeout TIMEOUT] [--header HEADERS] [--referer HEADERS] [--max-skip MAX_SKIP] urls [urls ...]`
- `img scrape [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--timeout TIMEOUT] [--header HEADERS] [--referer HEADERS] [--linked | --no-linked] site`
- `img get [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--timeout TIMEOUT] [--header HEADERS] [--referer HEADERS] urls [urls ...]`

## DESCRIPTION


## OPTIONS

### `img collect`

### `img get`

### `img scrape`

## SHELL-COMPLETION

To get shell-completion you have to add the following line at the end of your `~/.bashrc`.

```shell
eval "$(img --shell-complete)"
```

## BUGS

https://github.com/utility-toolbox/img/issues

## AUTHOR

https://github.com/PlayerG9

## SEE ALSO

https://github.com/utility-toolbox/img
