# Basic package template

## Summary

Just a basic package template.

## Structure

```bash
    src/reference_package/api       Public and internal API.
    src/reference_package/cli       Command-line-interface.
    src/reference_package/lib       Implementation.
    tests/e2e                       End-to-end tests.
    test/integration                Integration tests.
    tests/unit                      Unit tests.
```

## Library functions

`reference_package` is a library from which you can import functions. Import the public example function like this: `from reference_package import wait_a_second`. Or, import the internal version like a power user like this: `from reference_package.api.internal import wait_a_second`.

Unless you're developing, avoid importing directly from library, like `from reference_package.lib.example import wait_a_second`.

## CLI

Try the example CLI:

    $ python -m example
    $ python -m example --secs 2

## Dev workflow

There are a number of dev tools in the `Makefile`. You can list all the make tools you might want to use:

    $ make list-targets

Go check them out in `Makefile`.

*Note: The dev tools are built around developing on a Mac, so they may not all work on Windows without some modifications.*

### Dev installation

You'll want this package's site-package files to be the source files in this repo so you can test your changes without having to reinstall. We've got some tools for that.

First build and activate the env before installing this package:

    $ make build-env
    $ conda activate reference_package_py3.12

Note, if you don't have Python installed, you need to pass the package name directly when you build the env: `make build-env PACKAGE_NAME=reference_package`. If you have Python installed (e.g., this conda env already activated), then you don't need to because it uses Python to grab the package name from the `setup.cfg` file.

Then, install this package and its dev dependencies:

    $ make install INSTALL_EXTRAS=[dev]

This installs all the dependencies in your conda env site-packages, but the files for this package's installation are now your source files in this repo.

### QC and testing

Before pushing commits, you'll usually want to rebuild the env and run all the QC and testing:

    $ make clean format full

When making smaller commits, you might just want to run some of the smaller commands:

    $ make clean format full-qc full-test

### CI test run

Before opening a PR or pushing to it, in addition to running the make QC and build targets above while developing, you'll want to run locally the same CI pipeline that GitHub will run (`.github/workflows/CI.yml`).

The CI workflow runs multiple Docker images, so you'll need to install Docker and have it running on your machine: https://www.docker.com/.

Once Dockers is installed and running, you can use `act`. You'll need to install that as well. I develop on a Mac, so I used `homebrew` to install it (which you'll also need to install: https://brew.sh/):

    $ brew install act

Then, run it from the repo directory:

    $ make ci-run

That will run `.github/workflows/CI.yml`.

Since `act` doesn't work with Mac and Windows architecture, it skips/fails them, but it is a good test of the Linux build. Also, the workflow is set to skip some steps when called from `act` (like uploading the dist to GitHub and publishing the package to PyPi), so it doesn't run the full workflow, but it's still a good check of most of the workflow and especially useful when debugging the workflow itself.

It's generally a good practice to run it at least once before opening a PR.

## Acknowledgement

I borrowed and modified the structure and tools from the idiomatic usage of IHME's Central Computation GBD team when I worked with them in 2023-2024.