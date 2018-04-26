BUILD_FILES = \
	anleitung_V49_GepulsteNMR.pdf \
	build/main.pdf

OUT_DIR = build
TEX_CMD = latexmk \
	--pdf \
	--output-directory=$(OUT_DIR) \
	--halt-on-error \
	--interaction=nonstopmode
PREVIEW_CMD = \
	$(TEX_CMD) --pvc


all: $(BUILD_FILES)


anleitung_V49_GepulsteNMR.pdf:
	wget http://129.217.224.2/HOMEPAGE/PHYSIKER/MASTER/SKRIPT/V49.pdf -q \
		--user TUDoFP --password WS1718 \
		-O anleitung_V49_GepulsteNMR.pdf

build/main.pdf: FORCE | build
	TEXINPUTS=build: BIBINPUTS=build: max_print_line=1048576 \
	$(TEX_CMD) main.tex

preview: FORCE | build
	TEXINPUTS=build: BIBINPUTS=build: max_print_line=1048576 \
	$(PREVIEW_CMD) main.tex

build/punktgitter.pdf: anleitung_V41_DebyeScherrer.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=2 -dLastPage=2 \
		-sOutputFile=build/punktgitter.pdf \
		anleitung_V41_DebyeScherrer.pdf
	pdfcrop --bbox "97 650 600 785" build/punktgitter.pdf build/punktgitter.pdf 
	pdfcrop build/punktgitter.pdf build/punktgitter.pdf

FORCE:


build:
	@mkdir -p build


clean:
	rm -rf *.pdf build

.PHONY: all clean FORCE preview
