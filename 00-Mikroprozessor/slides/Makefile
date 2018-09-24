all: build/main.pdf

build:
	mkdir -p $@

build/main.pdf: FORCE | build
	latexmk \
		--output-directory=build \
		--pdf \
		--halt-on-error \
		--interaction=nonstopmode \
	main.tex

FORCE:

clean:
	rm -rf build

.PHONY: all clean FORCE
