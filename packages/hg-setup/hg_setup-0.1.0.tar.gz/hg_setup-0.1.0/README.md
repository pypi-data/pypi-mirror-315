# hg-setup: easily setup Mercurial with a tiny Python application

[![Latest version](https://badge.fury.io/py/hg-setup.svg)](https://pypi.python.org/pypi/hg-setup/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/hg-setup.svg)
[![Heptapod CI](https://foss.heptapod.net/fluiddyn/hg-setup/badges/branch/default/pipeline.svg)](https://foss.heptapod.net/fluiddyn/hg-setup/-/pipelines)
[![Github Actions](https://github.com/fluiddyn/hg-setup/actions/workflows/ci.yml/badge.svg?branch=branch/default)](https://github.com/fluiddyn/hg-setup/actions)

## Background

Mercurial is a Python application using C and Rust extensions. It is extendable with
Mercurial extensions and two Python packages provide very useful Mercurial extensions
that most users should use : hg-git (Mercurial extension hggit) and hg-evolve (Mercurial
extensions topic and evolve).

These things are packaged in 3 PyPI packages (associated with their equivalent
conda-forge packages): mercurial, hg-git, hg-evolve.

To use Mercurial extensions, one has to write few lines in a configuration file
(~/.hgrc).

Mercurial with hg-git and hg-evolve is great but it is a bit difficult to setup. hg-setup
is there to help people to start with Mercurial and finalize its installation.

## Install

Currently, only installation from source works.

```sh
pipx install hg-setup@hg+https://foss.heptapod.net/fluiddyn/hg-setup
```

For development installation, see the file [CONTRIBUTING.md](./CONTRIBUTING.md).

### My plans

I hope that ultimately hg-setup can be installed automatically with Mercurial when
running install commands like:

```sh
# from PyPI
pipx install mercurial[full]
uv tool install mercurial[full]
# with Miniforge (conda-forge) and conda-app (https://foss.heptapod.net/fluiddyn/conda-app)
conda-app install mercurial
# this requires optional deps on conda-forge
pixi global install mercurial[full]
```

However, we are not yet there. Nevertheless, this will work very soon (once hg-setup is
on PyPI)

```sh
pipx install mercurial
pipx inject mercurial hg-git hg-evolve hg-setup
# or
uv tool install mercurial --with hg-git --with hg-evolve --with hg-setup
```

and this will work soon (once hg-setup is on conda-forge and mercurial-app has been
modified).

```sh
conda-app install mercurial
pixi global install mercurial-app
pixi global install mercurial --with hg-git --with hg-evolve --with hg-setup
```

Note that this will soon work too, independently of how Mercurial is installed:

```sh
uvx hg-setup init
```

## User interfaces

The ~/.hgrc file and shell completion for bash and zsh can be initialized with a simple
Terminal User Interface (TUI):

```sh
hg-setup init
```

We can also avoid the TUI with

```sh
hg-setup init --name "Alice Lastname" --email alice.lastname@proton.me --auto
```

The shell completion for bash and zsh can be initialized with:

```sh
hg-setup init-shell-completion bash
hg-setup init-shell-completion zsh
```
