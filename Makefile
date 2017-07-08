
SHELL=/bin/bash

install: setup database defaults
	@echo "Setup completed!"

setup:
	@pip3 install -r requirements.txt
	@echo "Packages installed"

database:
	@python3 setup_database.py

defaults:
	-@read -n 1 -p "Add some fake entries to the database? (y/n): " x && { echo; \
	echo "$$x" | grep -qi "y" && \
	python3 lots_of_books.py; } || true

.PHONY: setup database
