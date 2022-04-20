## Development

### Add new dependency
We are using [poetry][po] as a package and virtual environment manager. If you're developing something
that requires additional packages use, please add this package to the [`pyproject.toml`](.pyproject.toml) file also.
To install a dependency to the environment and automatically add it to this file use a single command:
`poetry add <package_name>`
Here is the `add` command [poetry reference][po-add]

### How to install Python
On Linux: [How to Install Python on Linux][pt-ln]
On Windows: [How to Install Python on Windows][pt-wn]

[pt-ln]: https://realpython.com/installing-python/#how-to-install-python-on-linux
[pt-wn]: https://realpython.com/installing-python/#how-to-install-python-on-windows
[po]: https://python-poetry.org/docs/basic-usage/
[po-add]: https://python-poetry.org/docs/cli/#add
