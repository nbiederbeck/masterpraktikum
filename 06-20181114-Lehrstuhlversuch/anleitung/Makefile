all: build/anleitung.pdf

build:
	mkdir -p $@

build/anleitung.pdf: FORCE tikz/build/overview.pdf build/theta2.pdf build/hadroness.pdf | build
	latexmk --pdf --output-directory=build --halt-on-error --interaction=nonstopmode \
		anleitung.tex

tikz/build/overview.pdf:
	$(MAKE) -C tikz

build/theta2.pdf: build/hadroness.pdf
build/hadroness.pdf:
	$(MAKE) -C plots

FORCE:

clean:
	rm -rf build
	$(MAKE) -C tikz clean
	$(MAKE) -C plots clean

.PHONY: all clean FORCE
