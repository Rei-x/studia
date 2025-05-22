# Makefile for Dagster development
# Sets DAGSTER_HOME to an absolute path to the data directory

# Get the absolute path to the data directory
CURRENT_DIR := $(shell pwd)
DATA_DIR := $(CURRENT_DIR)/data
DAGSTER_HOME := $(DATA_DIR)

.PHONY: dev clean help

dev:
	@echo "Starting Dagster development server with DAGSTER_HOME=$(DAGSTER_HOME)"
	DAGSTER_HOME=$(DAGSTER_HOME) dagster dev

clean:
	@echo "Cleaning temporary files..."
	rm -rf tmpiek9b2p3

# Help command to display available targets
help:
	@echo "Available targets:"
	@echo "  dev    - Start Dagster development server"
	@echo "  clean  - Remove temporary files"
	@echo "  help   - Display this help message"