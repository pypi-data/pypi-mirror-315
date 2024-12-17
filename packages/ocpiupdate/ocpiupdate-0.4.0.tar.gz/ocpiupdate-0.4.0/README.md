# `ocpiupdate` - An updater for OpenCPI projects

`ocpiupdate` updates OpenCPI Projects to use style associated with newer
versions of OpenCPI.

For example:

- Using `<worker>-<model>.xml` for the Worker Description files, instead of
  `<worker>.xml`.
- Using `<component>.comp/<component>-comp.xml` for Component Specification
  files instead of `specs/<component>[-_]spec.xml`.
- Using `xml` files instead of `Makefile`s.

## Dependencies

This library requires Python 3.11 or newer. This means it doesn't support the
default system `python3` install on Ubuntu 20.04 or Ubuntu 22.04.

If you use a system with Python 3.10 or older, you need to either:

- Install a newer `python3` just for this library.
    - I'd recommend using a tool like [`uv`](https://docs.astral.sh/uv).
- Download and run the containerised version.

## Installation

### `pip`

You can install the latest release from [PyPi](https://pypi.org/project/ocpiupdate):

```bash
pip install ocpiupdate
```

Or, you can install this repository directly:

```bash
# Installs `develop` branch
pip install git+https://gitlab.com/dawalters/ocpiupdate

# Installs `v0.4.0` branch
pip install git+https://gitlab.com/dawalters/ocpiupdate@v0.4.0
```

### `docker` or `podman`

The [`containers`](https://gitlab.com/dawalters/ocpiupdate/-/tree/develop/containers)
directory contains a variety of containers, relying only on a local
installation of `docker` or `podman`.

You can download a built container from the
[Gitlab Container Registry](https://gitlab.com/dawalters/ocpiupdate/container_registry)

Usage example:

```bash
project_directory=/path/to/project/root

container_name=ocpiupdate:v0.4.0

additional_arguments="--dry-run --verbose"

# for `podman`, just replace `docker`
docker run \
    --volume "$project_directory":/tmp \
    --workdir /tmp \
    "$container_name" \
    "$additional_arguments"
```

See [`containers/scripts/ocpiupdate.sh`](https://gitlab.com/dawalters/ocpiupdate/-/tree/develop/containers/scripts/ocpiupdate.sh)
for a more complex example.

### Source tarball

You can download source releases from the
[Gitlab Releases page](https://gitlab.com/dawalters/ocpiupdate/-/releases).

## Configuration

Until documentation becomes available, you can follow the release posts
available on
[the OpenCPI forum](https://opencpi.dev/t/script-to-automate-updating-aspects-of-older-opencpi-projects).

This includes examples of usage, and discussion of how to write configuration
files.

## Disclaimer

This repository has no affiliation with OpenCPI.

The maintainer doesn't maintain OpenCPI.
