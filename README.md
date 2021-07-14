# The api for flora application

## Configuration

After checkout of a repository, please perform the following steps in exact sequence:

1. Copy docker-compose.override

```shell
cp docker-compose.override.yml.dist docker-compose.override.yml
```

2. Create `.env` file from `.env.dist`

```shell
cp .env.dist .env
```

Remember to fill up required values in `.env`

3. Run `npm i`

4. Run `npm run docker-build`

5. Run watch - `npm run watch`

## Dev setup

1. In order to run the whole app type:

```shell
npm run start
```

2. In order to watch files for dev purpose type:

```shell
npm run watch
```

3. If you need to close all containers run:

```shell
npm run down
```

4. To get into Docker container's shell:

```shell
npm run shell
```

## Code generation

We're using Plop for routes, models, actions (queries and mutations), commands and handlers generation.

```shell
npm run plop
```

## Code style

```shell
npm run lint
npm run format
```

## Database migrations

```shell
npm run generate-migration -- <migration-name>
```

This should generate a migration for all connected entities.

## Adminer setup

Adminer is configured in `docker-compose.override.yml` and should work out of the box on port 8080. To login to adminer use the following values:

```shell
Database type: postgres
Server: postgres
User: postgres
Password: password
Database: app
```

## Debugging

### VS Code

There is `launch.json` configuration inside `editors/vsc` directory. Just copy it and create new debugger to make it work with vsc :) 

## Tests

- integration: `npm run integration`
- units: `npm run units`

## License

[![license](https://img.shields.io/badge/license-MIT-4dc71f.svg)](https://raw.githubusercontent.com/TheSoftwareHouse/express-boilerplate/main/LICENSE)

This project is licensed under the terms of the [MIT license](/LICENSE).

The application was created with [TSH express-boilerplate](https://github.com/TheSoftwareHouse/express-boilerplate)
