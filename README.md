# Wagtail Periodic Review

A Wagtail package for periodic page content reviews for quality or audit purposes.

[![Build status](https://img.shields.io/github/actions/workflow/status/torchbox/wagtail-periodic-review/test.yml?branch=main)](https://github.com/torchbox/wagtail-periodic-review/actions)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

![A screenshot of the Wagtail administrative dashboard with periodic review panels](https://github.com/torchbox/wagtail-periodic-review/raw/main/.github/wagtail-periodic-review.webp)

## Features

- Dashboard panels
- Filtered report
- Configurable next review frequency


## Installation

Install using pip:

```bash
  pip install wagtail-periodic-review
```


After installing the module, add `wagtail_periodic_review` and `wagtail.contrib.settings` to installed apps in your settings file:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    "wagtail.contrib.settings",
    "wagtail_periodic_review",
]
```

Run migrations:

```bash
$ ./manage.py migrate
```


## Usage

Add the `PeriodicReviewMixin` to your `Page` models:

```python
from wagtail.models import Page
from wagtail_periodic_review.models import PeriodicReviewMixin


class MyPage(PeriodicReviewMixin, Page):
    # Add the periodic review panels to the settings panels
    settings_panels = PeriodicReviewMixin.review_panels + Page.settings_panels
```


## Contributing

### Install

To make changes to this project, first clone this repository:

```sh
git clone git@github.com:torchbox/wagtail-periodic-review.git
cd wagtail-periodic-review
```

With your preferred virtualenv activated, install testing dependencies:

#### Using pip

```sh
python -m pip install --upgrade "pip>=21.3"
python -m pip install -e '.[testing]' -U
```

#### Using flit

```sh
python -m pip install flit
flit install
```

### pre-commit

Note that this project uses [pre-commit](https://github.com/pre-commit/pre-commit). To set up locally:

```shell
# if you don't have it yet, globally
$ python -m pip install pre-commit
# go to the project directory
$ cd wagtail-periodic-review
# initialize pre-commit
$ pre-commit install

# Optional, run all checks once for this, then the checks will run only on the changed files
$ pre-commit run --all-files
```

### How to run tests

Now you can run tests as shown below:

```sh
tox
```

or, you can run them for a specific environment `tox -e python3.9-django4.2-wagtail6.3` or specific test
`tox -e python3.9-django4.2-wagtail6.3 -- tests.test_file.TestClass.test_method`

To run the test app interactively, use `tox -e interactive`, visit `http://127.0.0.1:8020/admin/` and log in with `admin`/`changeme`.
