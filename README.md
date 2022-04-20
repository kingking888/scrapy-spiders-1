# scrapy-spiders
![checks][checks] ![publish][publish]

Collection of scrapy spiders.

## Table of Contents
* [About](#about)
* [Prerequisites](#prerequisites)
* [Install](#install)
  * [Filesystem pipeline setup](#filesystem-pipeline-setup)
  * [S3 pipeline setup](#s3-pipeline-setup)
  * [API pipeline setup](#api-pipeline-setup)
  * [Activate environment](#activate-environment-and-go-to-the-spiders-dir)
* [Spiders](#spiders)
    * [Complete spiders list](https://github.com/agblox/scrapy-spiders/wiki/Spiders-list-with-tags)
* [Steps on handling a difficult spider](https://github.com/agblox/scrapy-spiders/wiki/Steps-for-dealing-with-an-difficult-scraper)
* [How to build the spider fast way](https://github.com/agblox/scrapy-spiders/wiki/How-to-build-the-spider-fast-way)
* [Build](#build)
* [Contribute](#contribute)
* [Development issues](docs/README.md)

### About
This code repository provides the collection of scrapy spiders we use for fetching the data from different data sources.

### Prerequisites
Tools to install: [git][g], [pre-commit][pk], [poetry][p], [Docker][dk]

In case you are using Ubuntu it is HIGHLY recommended install all global dependencies
with [this][a] playbook for automated tools installation (Ubuntu only). It will take from your shoulders all
boring stuff.

Refer to [Development issues](docs/README.md) if you've got stuck with set up or development.

### Install
- `git clone git@github.com:agblox/scrapy-spiders.git`
- `cd scrapy-spiders`
- `poetry shell`
- `make repo-init`
- `make bootstrap`
(Sometimes this command fails while installing packages because poetry with version >= 1.1.1 installs dependency parallel. So for consistent installation run poetry config experimental.new-installer false' before excuting 'make bootstrap')
- `make swarm-init`
- `make start-selenium`
- `make tests`

### Running locally
For store scraping results one or more pipelines must be activated. We are use S3 and API pipeline for production spiders.
To be able to test spiders locally no need to enable these pipelines, you can use
filesystem pipeline only.

#### Filesystem pipeline setup
Set `TO_FILE=1` environment variable to store files locally to the `src/data` dir. Unset this variable to deactivate filesystem pipeline.

Run command example (from `src/` dir):
```commandline
TO_FILE=1 scrapy crawl agfax.com -a config=no_url_test.json
```
[Config file example](docs/config_examples/no_url_test.json)

---

#### S3 pipeline setup
Set `S3_BUCKET=<S3 bucket name>` environment variable to store files locally to the S3 bucket. Unset this variable to deactivate S3 pipeline.

You need to set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables if you want to run spider locally.

#### API pipeline setup
Set `API_URL=<URL of API server>` environment variable to store data to AI datasets. Unset this variable to deactivate API pipeline.

Set API server credentials variables.
- `API_USER=<user name>`
- `API_PASSWORD=<password>`

#### Slack Notifications pipeline setup
Set `TO_SLACK=1` environment variable to send notifications to Slack. Unset this variable to deactivate Notification pipeline.
You have to set `NOTIFIER_ARN=<notifier_arn>` variable also to be able to use this pipeline.

#### Whether keep or not video stream files along with audio in YouTube spider
Set `KEEP_VIDEO=1` environment variable to enable a possibility to store video files in same dir as audio.

---

### Spiders
#### Activate environment and go to the spiders dir
- `poetry shell`
- `cd src`

Configurations for spiders can be downloaded from `/sources/spider-config` endpoint of [AI datasets server][ai-sr] by
providing a spider's name to it (defined in spider's class). Or use these [examples](docs/config_examples)

[`BaseSpider` config file example](docs/config_examples/no_url_test.json)

[`EquitySpider`, `TwitterSearch` config file example](docs/config_examples/equity_site_conf_test.json)

[`RedditSearchSpider` config file example](docs/config_examples/reddit_search_conf_test.json)

[`TwitterSpider` config file example](docs/config_examples/twitter_conf_test.json)

[`RedditSpider` config file example](docs/config_examples/reddit_test_conf.json)

[`RedditCommentsSpider` config file example](docs/config_examples/reddit_comments_conf_test.json)

#### Running spiders
```commandline
scrapy crawl <spider_name> -a config=<path to config file>
```

(NOTE: if spider uses selenium be sure you have a docker swarm up and running chrome browser under it)

#### Running `TwitterSpider` twitter
You need to set  `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_TOKEN` and `TWITTER_ACCESS_TOKEN_SECRET` variables if you want to run this spider.


#### Running `RedditSpider`, `RedditSearchSpider` or `RedditCommentsSpider`
You need to set `REDDIT_CLIENT_SECRET`, `REDDIT_CLIENT_ID`, `REDDIT_PASSWORD`, `REDDIT_USERNAME` variables if you want to run this spider.

## Build
- Release GitHub [workflow](.github/workflows/release.yml).  Release commit types: `fix`, `feat`.
- Publish GitHub [workflow](.github/workflows/publish.yml). Build and push docker image.

## Contribute
Commit message style - [Conventional Commits][cc].

### Examples commit messages
* ```
  feat(new spider): add the agfax spider
  ```
* ```
  fix: add missing variable to settings

  The error occurred because of <reasons>.
  ```
* ```
  feat: remove texts put endpoint

  refers to DAI-234
  BREAKING CHANGES: texts endpoint no longer supports text node editing.
  ```
* ```
  build(release): bump version to 5.0.0
  ```
* ```
  build: update dependencies
  ```
* ```
  refactor: move foor loop to a separate method
  ```
* ```
  style: make log output more precise
  ```

[cc]: https://www.conventionalcommits.org/en/v1.0.0/
[g]: https://www.atlassian.com/git/tutorials/install-git
[pk]: https://pre-commit.com/#install
[p]: https://python-poetry.org/docs/#installation
[a]: https://github.com/IaroslavR/ansible-role-server-bootstrap

[checks]: https://github.com/agblox/scrapy-spiders/actions/workflows/checks.yml/badge.svg
[publish]: https://github.com/agblox/scrapy-spiders/actions/workflows/publish.yml/badge.svg
[ai-sr]: https://demo.datalake.diviai.com/ui/
[dk]: https://docs.docker.com/get-docker/
