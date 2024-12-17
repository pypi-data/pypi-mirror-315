# mdx_spanner

This package enables `rowspan` and `colspan` in markdown tables when using [MkDocs](https://www.mkdocs.org/).

## Syntax

### Basics (spanning indicators)

You can activate `colspan` by putting only `~~` in a cell. This will merge the cell with the cell in the previous column.

You can activate `rowspan` by putting `__` in a cell. This will merge the cell with the cell in the previous row. If the cell in previous row is empty it will continue to merge until it finds a non-empty cell.

Sample:

```md
| Header 1 | Header 2 | Header 3 |
| ---------| -------- | -------- |
| Value 1  |    ~~    | Value 2  |
|          |    ~~    | Value 3  |
|_        _|    ~~    | Value 5  |
| Value 6  | Value 7  | Value 8  |
```

This should result in the following table:
```md
+----------+----------+----------+
| Header 1 | Header 2 | Header 3 |
+----------+----------+----------+
| Value 1             | Value 2  |
|                     +----------+
|                     | Value 3  |
|                     +----------+
|                     | Value 5  |
+----------+----------+----------+
| Value 6  | Value 7  | Value 8  |
+----------+----------+----------+
```

### Advanced (alignment markers)

You can change the alignment of a single spanned cell by adding markers to the spanning indicators.

To change the horizontal alignment (when multiple columns are merged) put colons before and/or after the `~~` to indicate the alignment:

| Sample | Result |
| ------ | ------ |
| `:~~`  | Left aligned |
| `:~~:`  | Centered |
| `~~:`  | Right aligned |

<br>
To change the vertical alignment (when multiple rows are merged) put one of the following chars (`^`,`=`,`_`) between the `__` to indicate the alignment:

| Sample | Result |
| ------ | ------ |
| `_^_`  | Top aligned |
| `_=_`  | Centered |
| `___`  | Bottom aligned |

Sample:

```md
| Header 1   | Header 2 | Header 3 |
| ---------- | -------- | -------- |
| Value 1    |   :~~:   | Value 2  |
|            |    ~~    | Value 3  |
|_     =    _|    ~~    | Value 5  |
| Value 6    | Value 7  | Value 8  |
```
This should result in the following table:


```md
+----------+----------+----------+
| Header 1 | Header 2 | Header 3 |
+----------+----------+----------+
|                     | Value 2  |
|                     +----------+
|       Value 1       | Value 3  |
|                     +----------+
|                     | Value 5  |
+----------+----------+----------+
| Value 6  | Value 7  | Value 8  |
+----------+----------+----------+
```


## Install

```console
$ pip install mdx_spanner
```

## Usage

After installing the extension you can add it in the `mkdocs.yml` file:

```yaml
site_name: ...
nav:
  ...
theme:
  ...
markdown_extensions:
  - mdx_spanner
```