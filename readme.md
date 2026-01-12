# HeadHunter Vacancy Parser

The parser is developed to collect information about job vacancies in Minsk.

## Installing
Commands for clonning repository and installing required dependencies\
`mkdir HHParser && cd HHParser`\
`git clone https://github.com/1roma1/HHParser.git .`\
`uv sync`

Making migrations \
`alembic upgrade head`

## Enviromental Variables

Before making migrations or running the parser, the following env variables must be set up

`PG_USER=admin`\
`PG_PASSWORD=123`\
`PG_DB=db`\
`PG_HOST=127.0.0.1`\
`PG_PORT=5432`

## Commands

`python main.py` - parse ads and load information to the database