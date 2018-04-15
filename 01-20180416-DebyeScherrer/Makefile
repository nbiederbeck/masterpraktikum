BUILD_FILES = \
	anleitung_V41_DebyeScherrer.pdf \
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


anleitung_V41_DebyeScherrer.pdf:
	wget http://129.217.224.2/HOMEPAGE/PHYSIKER/MASTER/SKRIPT/V41.pdf -q \
		--user TUDoFP --password WS1718 \
		-O anleitung_V41_DebyeScherrer.pdf


build/main.pdf: build/punktgitter.pdf
build/main.pdf: build/versuchsaufbau.pdf
build/main.pdf: build/ausdehnung_probe.pdf
build/main.pdf: build/verzug_probe.pdf
build/main.pdf: build/absorptionskante.pdf
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
	pdfcrop --bbox "97 650 600 986" build/punktgitter.pdf build/punktgitter.pdf 
	pdfcrop build/punktgitter.pdf build/punktgitter.pdf

build/versuchsaufbau.pdf: anleitung_V41_DebyeScherrer.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=13 -dLastPage=13 \
		-sOutputFile=build/versuchsaufbau.pdf \
		anleitung_V41_DebyeScherrer.pdf
	pdfcrop --bbox "00 80 380 305" build/versuchsaufbau.pdf build/versuchsaufbau.pdf 
	pdfcrop build/versuchsaufbau.pdf build/versuchsaufbau.pdf 

build/ausdehnung_probe.pdf: anleitung_V41_DebyeScherrer.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=14 -dLastPage=14 \
		-sOutputFile=build/ausdehnung_probe.pdf \
		anleitung_V41_DebyeScherrer.pdf
	pdfcrop --bbox "0 120 280 337" build/ausdehnung_probe.pdf build/ausdehnung_probe.pdf
	pdfcrop build/ausdehnung_probe.pdf build/ausdehnung_probe.pdf 

build/verzug_probe.pdf: anleitung_V41_DebyeScherrer.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=15 -dLastPage=15 \
		-sOutputFile=build/verzug_probe.pdf \
		anleitung_V41_DebyeScherrer.pdf
	pdfcrop --bbox "0 425 315 630" build/verzug_probe.pdf build/verzug_probe.pdf
	pdfcrop build/verzug_probe.pdf build/verzug_probe.pdf 

build/absorptionskante.pdf: anleitung_V41_DebyeScherrer.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=16 -dLastPage=16 \
		-sOutputFile=build/absorptionskante.pdf \
		anleitung_V41_DebyeScherrer.pdf
	pdfcrop --bbox "0 430 280 590" build/absorptionskante.pdf build/absorptionskante.pdf
	pdfcrop build/absorptionskante.pdf build/absorptionskante.pdf 

FORCE:


build:
	@mkdir -p build


clean:
	rm -rf *.pdf build

.PHONY: all clean FORCE preview
