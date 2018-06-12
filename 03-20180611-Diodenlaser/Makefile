BUILD_FILES = $(addprefix build/, \
	cutawayview.pdf \
	schematicview.pdf \
	basicconfiguration.pdf \
	emissionconstruction.pdf \
	rubidiumemission.pdf \
	lasertuning.pdf \
	lasertuning_modehops.pdf \
	pn_diode.png \
)

OUT_DIR = build
TEX_CMD = latexmk \
	--pdf \
	--output-directory=$(OUT_DIR) \
	--halt-on-error \
	--interaction=nonstopmode
PREVIEW_CMD = \
	$(TEX_CMD) --pvc


all: build/main.pdf


anleitung_V60_Diodenlaser.pdf:
	wget http://129.217.224.2/HOMEPAGE/PHYSIKER/MASTER/SKRIPT/Diodenl.pdf -q \
		--user TUDoFP --password WS1718 \
		-O anleitung_V60_Diodenlaser.pdf


build/main.pdf: $(BUILD_FILES) FORCE | build
	TEXINPUTS=build: BIBINPUTS=build: max_print_line=1048576 \
	$(TEX_CMD) main.tex


preview: $(BUILD_FILES) FORCE | build
	TEXINPUTS=build: BIBINPUTS=build: max_print_line=1048576 \
	$(PREVIEW_CMD) main.tex


FORCE:


build:
	@mkdir -p build


clean:
	rm -rf *.pdf build


.PHONY: all clean FORCE preview


N = 1
build/cutawayview.pdf: anleitung_V60_Diodenlaser.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=$N \
		-dLastPage=$N \
		-sOutputFile=$@ $<
	pdfcrop $@ $@ --bbox "135 210 505 430"
	pdfcrop $@ $@

N = 2
build/schematicview.pdf: anleitung_V60_Diodenlaser.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=$N \
		-dLastPage=$N \
		-sOutputFile=$@ $<
	pdfcrop $@ $@ --bbox "-45 260 595 585"

N = 4
build/basicconfiguration.pdf: anleitung_V60_Diodenlaser.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=$N \
		-dLastPage=$N \
		-sOutputFile=$@ $<
	pdfcrop $@ $@ --bbox "70 420 580 600"

build/emissionconstruction.pdf: anleitung_V60_Diodenlaser.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=14 \
		-dLastPage=14 \
		-sOutputFile=$@ $<
	pdfcrop $@ $@ --bbox "70 530 580 710"

build/rubidiumemission.pdf: anleitung_V60_Diodenlaser.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=17 \
		-dLastPage=17 \
		-sOutputFile=$@ $<
	pdfcrop $@ $@ --bbox "90 532 520 740" 

build/pn_diode.png:
	wget https://upload.wikimedia.org/wikipedia/commons/d/d6/Pn-junction-equilibrium.png \
		-q -O $@

N = 5
build/lasertuning.pdf: anleitung_V60_Diodenlaser.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=$N \
		-dLastPage=$N \
		-sOutputFile=$@ $<
	pdfcrop $@ $@ --bbox "70 445 580 800"
	pdfcrop $@ $@

N = 10
build/lasertuning_modehops.pdf: anleitung_V60_Diodenlaser.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=$N \
		-dLastPage=$N \
		-sOutputFile=$@ $<
	pdfcrop $@ $@ --bbox "70 380 580 800"
	pdfcrop $@ $@
