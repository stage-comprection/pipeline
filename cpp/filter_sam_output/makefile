# Compiler options
CC = g++
OPTCFLAGS= -Ofast -march=native
CFLAGS= -Wall -Werror -std=c++11 $(OPTCFLAGS)
LDFLAGS= -pthread

# Directory organisation
BASEDIR = .
SRC = $(BASEDIR)/src
BUILD = $(BASEDIR)/build
BIN = $(BASEDIR)/bin

# Program name
TARGET = filter_sam_output

# Rules

all: init $(TARGET)

$(TARGET): $(BUILD)/$(TARGET).o
	$(CC) $(CFLAGS) -o $(BIN)/$(TARGET) $^

$(BUILD)/%.o: $(SRC)/%.cpp
	$(CC) $(CFLAGS) -c -o $@ $^


clean:
	rm -rf $(BUILD)/*.o
	rm -rf $(BIN)/$(TARGET)

init: 
	mkdir -p $(BUILD) $(BIN)

rebuild: clean $(TARGET)
