# Basic package template

## Summary

Just a basic package template.

## Structure

```bash
    .github/workflows               GitHub Actions CI/CD workflows.
    docs                            RST docs and doc build staging.
    Makefile                        Dev tools and params. (includes shared/Makefile)
    src/reference_package/api       Public and internal API.
    src/reference_package/cli       Command-line-interface.
    setup.cfg                       Metadata and dependencies.
    shared                          Shared dev tools Git submodule.
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

### Shared tools setup

When you first clone this repo, you'll need to set up the shared tools Git submodule. Follow the setup directions on that repo's README: https://github.com/crickets-and-comb/shared

See also https://git-scm.com/book/en/v2/Git-Tools-Submodules. And, take a look at the `.gitmodules` file in this repo.

The shared repo contains dev tools that this repo depends on, namely reusable workflows (for running QC/tests and CI/CD on GitHub) and make recipes/targets for running QC/tests locally while developing.

While the Makefile points to the shared Makefile via the Git submodule as a subdirectory, the workflows point to the shared reusable workflows via GitHub. You can point workflows at the shared workflows in the submodule directory (say for trying out uncommitted changes to a shared workflow) and run the workflows from `act` (see the `run-act` in the shared Makefile), but they will not run on the GitHub runners unless they point via GitHub.

You can override shared make targets or add new targets that aren't in the shared Makefile by adding them to this repo's top-level Makefile.

#### Setting Personal Access Token

The shared workflows rely on a Personal Access Token (PAT) (to checkout the submodule so they can use the make targets). You need to create a PAT with repo access and add it to the consuming repo's (`reference_package` in this case) action secrets as `PERSONAL_ACCESS_TOKEN`. See GitHub for how to set up PATs (hint: check the developer settings on your personal account) and how to add secrets to a repo's actions (hint: check the repo's settings).

Note: Using a PAT tied to a single user like this is less than ideal. Figuring out how to get around this is a welcome security upgrade.

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

Before opening a PR or pushing to it, in addition to running the make QC and build targets above while developing, you'll want to run locally the same CI pipeline that GitHub will run (`.github/workflows/CI_CD.yml`).

The CI workflow runs multiple Docker images, so you'll need to install Docker and have it running on your machine: https://www.docker.com/.

Once Dockers is installed and running, you can use `act`. You'll need to install that as well. I develop on a Mac, so I used `homebrew` to install it (which you'll also need to install: https://brew.sh/):

    $ brew install act

Then, run it from the repo directory:

    $ make run-act

That will run `.github/workflows/CI_CD.yml`.

Since `act` doesn't work with Mac and Windows architecture, it skips/fails them, but it is a good test of the Linux build.

Also, after QC and testing, the deployment jobs of the workflow don't run with the default parameters passed to `act` from `make run-act`. You can pass "test" or "prod" to `TEST_OR_PROD`, which will run the respective deployment jobs, but they will fail when they try to upload the package distrbution as an artifact to GitHub. But, it's still a good check of more of the workflow, useful when debugging the workflow itself.

It's generally a good practice to run `make run-act` at least once before opening a PR.

## Acknowledgement

I borrowed, modified, and added to some of the idiomatic structure and tools of IHME's Central Computation GBD team from when I worked with them in 2022-2024.