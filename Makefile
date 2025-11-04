CXX = clang++
CXXFLAGS = -std=c++17 -Wall -Wextra
TARGET = heap
SRC_DIR = src
BUILD_DIR = build

SOURCES = $(SRC_DIR)/heap.cpp
OBJECTS = $(BUILD_DIR)/heap.o

all: $(BUILD_DIR) $(TARGET)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJECTS)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR) $(TARGET)

run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run
