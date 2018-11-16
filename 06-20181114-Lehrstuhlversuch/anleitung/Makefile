all: build/anleitung.pdf

build:
	mkdir -p $@

build/anleitung.pdf: FORCE tikz/build/overview.pdf| build
	latexmk --pdf --output-directory=build --halt-on-error --interaction=nonstopmode \
		anleitung.tex

tikz/build/overview.pdf:
	make -C tikz

FORCE:

clean:
	rm -rf build tikz/build

.PHONY: all clean FORCE
