# Compiler options
CC = g++
OPTCFLAGS= -Ofast -march=native 
CFLAGS= -Wall -Werror -std=c++11 -I $(LIBPATH) $(OPTCFLAGS)
LDFLAGS= -pthread
LIBPATH = ../utils/src

# Directory organisation
BASEDIR = .
SRC = $(BASEDIR)/src
BUILD = $(BASEDIR)/build
BIN = $(BASEDIR)/bin

# Program name
TARGET = dbg_correction

# Objects names
OBJECTS = $(BUILD)/dbg_correction.o $(BUILD)/map_to_reference.o $(BUILD)/pipeline.o $(BUILD)/run_binaries.o $(BUILD)/settings.o $(BUILD)/utils.o

# Rules

all: init $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $(BIN)/$(TARGET) $^
	cp $(BIN)/$(TARGET) ../../binaries/$(TARGET)

$(BUILD)/%.o: $(SRC)/%.cpp
	$(CC) $(CFLAGS) -c -o $@ $^

$(BUILD)/utils.o: $(LIBPATH)/utils.cpp
	$(CC) $(CFLAGS) -c -o $@ $^

clean:
	rm -rf $(BUILD)/*.o
	rm -rf $(BIN)/$(TARGET)

init: 
	mkdir -p $(BUILD) $(BIN)

rebuild: clean $(TARGET)
