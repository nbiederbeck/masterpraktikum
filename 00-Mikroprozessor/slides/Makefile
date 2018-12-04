all: build/main.pdf build/notes.pdf

build:
	mkdir -p $@

build/main.pdf: FORCE | build
	latexmk \
		--output-directory=build \
		--pdf \
		--halt-on-error \
		--interaction=nonstopmode \
	main.tex

build/notes.pdf: notes.md | build
	pandoc -i $< -o $@

FORCE:

clean:
	rm -rf build

.PHONY: all clean FORCE
