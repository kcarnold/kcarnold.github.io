.PHONY: all check

all:
	cp /Users/ka37/Dropbox/ken/Docs/CV/cv.pdf static/kcarnold_cv.pdf
	quarto publish gh-pages --no-prompt

check:
	rg '(^draft: |TODO)'
