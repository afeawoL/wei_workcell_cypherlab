.DEFAULT_GOAL := init

.PHONY += init paths checks test clean

init: # Do the initial configuration of the project
	@test -e .env || cp cypherlab.env .env

.env: init

checks: # Runs all the pre-commit checks
	@pre-commit install
	@pre-commit run --all-files || { echo "Checking fixes\n" ; pre-commit run --all-files; }

up: # Starts the workcell
	@docker compose up --remove-orphans

clean:
	@rm .env
