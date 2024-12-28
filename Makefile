.PHONY: all check

all:
	cp /Users/ka37/Dropbox/ken/Docs/CV/cv.pdf static/kcarnold_cv.pdf
	cp "/Users/ka37/Library/CloudStorage/Dropbox/ken/Oregon/Research Statement.pdf" static/kcarnold_research_statement.pdf
	quarto publish gh-pages --no-prompt

check:
	rg '(^draft: |TODO)'
