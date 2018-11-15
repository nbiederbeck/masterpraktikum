all: build/anleitung.pdf

build:
	mkdir -p $@

build/anleitung.pdf: FORCE | build
	latexmk --pdf --output-directory=build --halt-on-error --interaction=nonstopmode \
		anleitung.tex

FORCE:

clean:
	rm -rf build

.PHONY: all clean FORCE
