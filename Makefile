.PHONY: all

all:
	quarto render
	quarto publish gh-pages
