.PHONY: all

all:
	cp /Users/ka37/Dropbox/ken/Docs/CV/kcarnold_cv.pdf static/kcarnold_cv.pdf
	quarto publish gh-pages --no-prompt
