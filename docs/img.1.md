img(1) -- cli to automatically download a collection of images or scrape them from a website
=============================================

## SYNOPSIS

- $`img [-h] [-v] {collect,scrape,get} ...`
- $`img collect [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--timeout TIMEOUT] [--header HEADERS] [--referer HEADERS] [--max-skip MAX_SKIP] urls [urls ...]`
- $`img get [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--timeout TIMEOUT] [--header HEADERS] [--referer HEADERS] urls [urls ...]`
- $`img merge [-h] [-y | --yes] [--save SAVE_ARGS] output dimensions images [images ...]`
- $`img scrape [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--timeout TIMEOUT] [--header HEADERS] [--referer HEADERS] [-l | --linked | --no-linked] [-W [WIDTH]] [-H [HEIGHT]] site`

## DESCRIPTION

## OPTIONS

### common options

* `-c CONCURRENT`, `--concurrent CONCURRENT`:
number of concurrent downloads. (higher doesn't mean faster downloads)

* `--on-conflict {rename,skip,replace}`:
how to handle the conflict if a file already exists.
  - `rename`: adds  `(i)` to the filename (e.g. `file.txt` becomes `file (1).txt`)
  - `skip`: skips the download of this specific file
  - `replace`: the existing file get overwritten with the new content

* `--timeout TIMEOUT`:
Specify download timeouts in seconds.
The connection timeout is the time the server has to respond.
The read timeout is the time the server has between sending data-blocks.
`img` supports 2 formats.
  - `a.b`: connection and read timeout (e.g. `1`, `1.5`)
  - `a.b:c.d`: connection:read timeout (e.g. `5:10`, `2.5:5`)

* `--header HEADER`:
Adds additional header to each request.
Can be used multiple times.
(e.g. $`--header 'Api-Key: 34hne0r9gh9034th0uset'`)

* `--referer REFERER`:
$`--referer 'https://domain.com'` is shorthand for $`--header 'referer: https://domain.com'`

### `img collect`

> Collects images.

$`img collect [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--timeout TIMEOUT] [--header HEADERS] [--referer HEADERS] [--max-skip MAX_SKIP] urls [urls ...]`

* see [common options](#common-options)

* $`--max-skip MAX_SKIP`:
How many url can be failing before stopping searching

### `img get`

> Scrapes images from given URL

$`img get [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--timeout TIMEOUT] [--header HEADERS] [--referer HEADERS] urls [urls ...]`

* see [common options](#common-options)

### `img merge`

> Merges multiple images into one image

$`img merge [-h] [-y | --yes] [--save SAVE_ARGS] output dimensions images [images ...]`

* $`-y`, $`--yes`:
Overwrite output if it exists

* $`--save SAVE_ARGS`:
Add additional parameters while saving the generated image. (Can be used multiple times)  
Format: $`--save {key}={value}`  
See [Pillow's image-file-formats](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) for more information about file-formats and their save parameters.

* $`output`:
Output file to write to

* $`dimensions`:
Dimensions of the output image.
This is not in pixels.
e.g. `2x2` would mean 2 images wide and 2 images high.

* $`images ...`:
Input Images to merge. This must match with `dimensions`.
e.g. dimensions of `2x2` would require 4 images. (`2x3` => 6 images)

e.g. $`img merge output.webp --save method=6 --save quality=100 --save lossless=True 2x2 topleft.png topright.png bottomleft.png bottomright.png`

### `img scrape`

> Similar to the `wget` program. Used to download provided images

$`img scrape [-h] [-c CONCURRENT] [--on-conflict {rename,skip,replace}] [--timeout TIMEOUT] [--header HEADERS] [--referer HEADERS] [-l | --linked | --no-linked] [-W [WIDTH]] [-H [HEIGHT]] site`

* see [common options](#common-options)

* $`-l`, $`--linked`, $`--no-linked`:
whether to attempt to download `<a href="..."><img/></a>` urls

* $`-W [WIDTH]`, $`--width [WIDTH]`:
specify width (eg `'>500'`)

* $`-H [HEIGHT]`, $`--height [HEIGHT]`:
specify height (eg `'>500'`)

e.g. $`img scrape --width '>500' --height '<1000' https://domain.com/page/`

## SHELL-COMPLETION

To get shell-completion you have to add the following line at the end of your `~/.bashrc`.

```shell
eval "$(img --shell-complete)"
```

> Warning: adding this to the `~/.bashrc` increases the startup-time of your shells significantly.
> Adding an alias and calling it if needed should be better. (`alias load-img-completion="eval \"$(img --shell-complete)\""`)

## BUGS

https://github.com/utility-toolbox/img/issues

## AUTHOR

https://github.com/PlayerG9

## SEE ALSO

https://github.com/utility-toolbox/img
