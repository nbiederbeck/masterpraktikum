BUILD_FILES = \
	anleitung_V41_DebyeScherrer.pdf \
	build/main.pdf


OUT_DIR = build
# TEX_CMD = latexmk \
	--pdf \
	--output-directory=$(OUT_DIR) \
	--halt-on-error \
	--interaction=nonstopmode
TEX_CMD = latexrun \
	--latex-cmd pdflatex \
	--bibtex-cmd biber \
	-O $(OUT_DIR)


all: $(BUILD_FILES)


anleitung_V41_DebyeScherrer.pdf:
	wget http://129.217.224.2/HOMEPAGE/PHYSIKER/MASTER/SKRIPT/V41.pdf \
		--user TUDoFP --password WS1718 \
		-O anleitung_V41_DebyeScherrer.pdf


build/main.pdf:
build/main.pdf: FORCE | build
	TEXINPUTS=build: BIBINPUTS=build: max_print_line=1048576 \
	$(TEX_CMD) main.tex


FORCE:


build:
	mkdir -p build


clean:
	rm -rf *.pdf build

.PHONY: all clean FORCE
