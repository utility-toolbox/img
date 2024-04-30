img(1) -- cli to automatically download a collection of images or scrape them from a website
=============================================

## SYNOPSIS

- $`img [-h] [-v] {collect,scrape,get} ...`
- $`img collect [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--timeout TIMEOUT] [--header HEADERS] [--referer HEADERS] [--max-skip MAX_SKIP] urls [urls ...]`
- $`img scrape [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--timeout TIMEOUT] [--header HEADERS] [--referer HEADERS] [--linked | --no-linked] site`
- $`img get [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--timeout TIMEOUT] [--header HEADERS] [--referer HEADERS] urls [urls ...]`

## DESCRIPTION

## OPTIONS

### common options

* `-c`, `--concurrent`:
number of concurrent downloads. (higher doesn't mean faster downloads)

* `--on-conflict`:
how to handle the conflict if a file already exists.
  - `rename`: adds  `(i)` to the filename (e.g. `file.txt` becomes `file (1).txt`)
  - `skip`: skips the download of this specific file
  - `replace`: the existing file get overwritten with the new content

* `--timeout`:
Specify download timeouts in seconds.
The connection timeout is the time the server has to respond.
The read timeout is the time the server has between sending data-blocks.
`img` supports 2 formats.
  - `a.b`: connection and read timeout (e.g. `1`, `1.5`)
  - `a.b:c.d`: connection:read timeout (e.g. `5:10`, `2.5:5`)

* `--header`:
Adds additional header to each request.
Can be used multiple times.
(e.g. $`--header 'Api-Key: 34hne0r9gh9034th0uset'`)

* `--referer`:
$`--referer 'https://domain.com'` is shorthand for $`--header 'referer: https://domain.com'`

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
