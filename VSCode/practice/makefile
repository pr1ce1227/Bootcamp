# Make file exampl 
# Treat the $() as a derefrence 
# just doing = will treet the right side as a macro 
# if you put := then it will solve the right side first then treat it as a macro 

CC=g++     # THis set my variable CC to be G++
CPPFLAGS=-g -Wall  # this sets some flags in the variable CPPFLAGS 
SRCES:=$(wildcard *.cpp)  #Wildcard is a built in recipe so we need to dereference it to get the recipe to run 
HEADERS:=$(wildcard *.h)  # ^ same as above, these recipes grap all the related files and store in the variabel 
OBJS:=$(SRCES:.cpp=.o)    # shorthand way to change the endings of the files 
# BUILD_OBJ := $(addprefix build/, $(OBJS))  # example of how to use the add prefix recipe, this will put all OBJS in build folder
BUILD_OBJ := $(patsubst %.cpp, build/%.o, $(SRCES)) # example of pattern substitue recipe, take pattern found in first and places that pattern in second argument, stores in 3rd argument
# SRCES := $(shell ls *.cpp) #using the key word shell will let you run any command line command then store the result in the variable 
# FILE := $(file main.cpp) #file take the contents of the current file and copies it to the variable created 
TARGET:=a.out  #just another variable set 

.PHONY: all   # this is used to ignore files, this is important so that all recipe will run regardless if there is an all file that is up to date in the director 

#Recipes 
all: $(TARGET)   #<target>: <Dependencies>  if dependency is listed it looks for rules regarding that dependency and solves them first if they need to be updated
	./$(TARGET)  #<Commands> 

$(TARGET): $(BUILD_OBJ)
	g++ $(BUILD_OBJ) -o $(TARGET)

build/%.o: %.cpp $(HEADERS)
	g++ -c $< -o $@

clean:            #inlucde this in all make files to undo all files created, then run make all to re-create them 
	rm a.out