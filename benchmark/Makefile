#!/usr/bin/make -f

# file: Makefile
# author: Icko Iben
# course: CSI 3336
# due date: 10/04/2024
#
# date modified:        10/04/2024
#   - valgrind target added
#   - use gnu89 as standard
#
# date modified:        10/03/2024
#   - file created (and finished)
#
# Description

VERSION = 0.1.0

# Search paths
vpath %.c src
vpath %.h include
vpath %.o build

# Compilation options
CFLAGS = -Wall -Werror -Wextra -Wpedantic -std=gnu89
CC = gcc
PROGRAM = ../benchmark.out
OUTPUT_OPTION = -o $@

# Directories
SRC_DIR = src
BUILD_DIR = build
BIN_DIR = bin

# Files
SOURCES := $(wildcard $(SRC_DIR)/*.c)
OBJECTS := $(subst $(SRC_DIR),$(BUILD_DIR),$(subst .c,.o,$(SOURCES)))

# Targets
all: build
.PHONY: all

.PHONY: help
help: ## Help function
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST)  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test: ## Debug variables
	$(info SOURCES=$(SOURCES))
	$(info OBJECTS=$(OBJECTS))
	$(info PROGRAM=$(PROGRAM))
.PHONY: test

build: ## Build this program
build: $(PROGRAM)
	@echo "========"
	@echo "Project built"
	@echo "Run ./$(PROGRAM) to run the program"
.PHONY: build

$(PROGRAM): $(OBJECTS)
	$(CC) $(OBJECTS) $(OUTPUT_OPTION)

$(OBJECTS): $(SOURCES)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< $(OUTPUT_OPTION)

clean-objects: ## Clean object files
	rm -f $(OBJECTS)
.PHONY: clean-objects

clean: ## Clean program executable and object files
clean: clean-objects
	rm -f $(PROGRAM)
.PHONY: clean
