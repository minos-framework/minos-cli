<p align="center">
  <a href="http://minos.run" target="_blank"><img src="https://raw.githubusercontent.com/minos-framework/.github/main/images/logo.png" alt="Minos logo"></a>
</p>

# Minos CLI: Minos' microservices up and running

[![PyPI Latest Release](https://img.shields.io/pypi/v/minos-cli.svg?label=minos-cli)](https://pypi.org/project/minos-microservice-aggregate/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/minos-framework/minos-cli/pages%20build%20and%20deployment?label=docs)](https://minos-framework.github.io/minos-cli)
[![License](https://img.shields.io/github/license/minos-framework/minos-cli.svg)](https://github.com/minos-framework/minos-cli/blob/main/LICENSE)
[![Coverage](https://codecov.io/github/minos-framework/minos-cli/coverage.svg?branch=main)](https://codecov.io/gh/minos-framework/minos-cli)
[![Stack Overflow](https://img.shields.io/badge/Stack%20Overflow-Ask%20a%20question-green)](https://stackoverflow.com/questions/tagged/minos)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/minos-framework/community)

## Summary

Minos CLI is a command line tool that helps you create and deploy Minos' microservices. Through its simple command
structure, you'll get your microservices up and running as fast as you've coded your business logic.

## Quickstart

First, we need to create a project to host our microservices

```shell
minos new project testproject
cd testproject/
```

Our project has dependencies from services that we need to set

```shell
minos set database postgres
minos set broker kafka
minos set discovery minos
minos set api-gateway minos
```

Now we can start these services using Docker

```shell
docker-compose up -d
```

Once we've the dependencies set, the project is ready to get a new microservice!

```shell
cd microservices/
minos new microservice testmicroservice
```

We're almost there! We now to create the microservice's databases

```shell
docker-compose exec postgres psql -U minos -tc 'CREATE database testmicroservice_db'
docker-compose exec postgres psql -U minos -tc 'CREATE database testmicroservice_query_db'
```

It's time to deploy our microservice

```shell
cd ..
docker-compose up -d microservice-testmicroservice
```

You can test the default endpoints through the `api-gateway` using

```shell
curl localhost:5566/testmicroservices
curl -X POST localhost:5566/testmicroservices
```

Time to start coding! Yes, already!

## Documentation

Coming soon...

## Source Code

The source code of this project is hosted at [GitHub Repository](https://github.com/minos-framework/minos-cli).

## Getting Help

For usage questions, the best place to go to is [StackOverflow](https://stackoverflow.com/questions/tagged/minos).

## Discussion and Development

Most development discussions take place over the [GitHub Issues](https://github.com/minos-framework/minos-cli/issues)
. In addition, a [Gitter channel](https://gitter.im/minos-framework/community) is available for development-related
questions.

## How to contribute

We are looking forward to having your contributions. No matter whether it is a pull request with new features, or the
creation of an issue related to a bug you have found.

Please consider these guidelines before you submit any modification.

### Create an issue

1. If you happen to find a bug, please file a new issue filling the 'Bug report' template.
2. Set the appropriate labels, so we can categorise it easily.
3. Wait for any core developer's feedback on it.

### Submit a Pull Request

1. Create an issue following the previous steps.
2. Fork the project.
3. Push your changes to a local branch.
4. Run the tests!
5. Submit a pull request from your fork's branch.

## License

This project is distributed under the [MIT](https://raw.githubusercontent.com/minos-framework/minos-cli/main/LICENSE)
license.
