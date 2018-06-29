BUILD_FILES = $(addprefix build/, \
	$(addsuffix .pdf, \
	amperemeter \
	aussteuerungsbereich\
	dreiecksgen\
	exponentialgen\
	frequenz_lin\
	linearverstaerker\
	logarithmierer\
	n_inv_elektrometer\
	operationsverstaerker\
	schmitt_trigger\
	schwingungsdiffgl\
	umkehr_diff\
	umkehr_integrator\
	) \
	$(addsuffix .png, \
	\
	) \
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


anleitung_V51_Operationsverstaerker.pdf:
	wget http://129.217.224.2/HOMEPAGE/PHYSIKER/MASTER/SKRIPT/V51.pdf -q \
		--user TUDoFP --password WS1718 \
		-O $@


build/main.pdf: $(BUILD_FILES) FORCE | build
	TEXINPUTS=build: BIBINPUTS=build: max_print_line=1048576 \
	$(TEX_CMD) main.tex


preview: $(BUILD_FILES) FORCE | build
	TEXINPUTS=build: BIBINPUTS=build: max_print_line=1048576 \
	$(PREVIEW_CMD) main.tex

build/operationsverstaerker.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=1 -dLastPage=1 \
		    -sOutputFile=$@ $<
		pdfcrop --bbox "0 450 600 595"  $@ $@
		pdfcrop $@ $@

build/aussteuerungsbereich.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=1 -dLastPage=1 \
		    -sOutputFile=$@ $<
		pdfcrop --bbox "200 70 600 280"  $@ $@
		pdfcrop $@ $@

build/linearverstaerker.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=4 -dLastPage=4 \
		    -sOutputFile=$@ $<
		pdfcrop --bbox "0 530 600 680"  $@ $@
		pdfcrop $@ $@

build/frequenz_lin.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=5 -dLastPage=5\
		    -sOutputFile=$@ $<
		pdfcrop --bbox "0 100 600 310"  $@ $@
		pdfcrop $@ $@


build/n_inv_elektrometer.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=6 -dLastPage=6\
		    -sOutputFile=$@ $<
		pdfcrop --bbox "0 320 600 477"  $@ $@
		pdfcrop $@ $@

build/amperemeter.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=7 -dLastPage=7\
		    -sOutputFile=$@ $<
		pdfcrop --bbox "0 330 600 495"  $@ $@
		pdfcrop $@ $@

build/umkehr_integrator.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=8 -dLastPage=8\
		    -sOutputFile=$@ $<
		pdfcrop --bbox "0 490 600 680"  $@ $@
		pdfcrop $@ $@

build/umkehr_diff.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=8 -dLastPage=8\
		    -sOutputFile=$@ $<
		pdfcrop --bbox "0 140 600 295"  $@ $@
		pdfcrop $@ $@
		
build/schmitt_trigger.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=9 -dLastPage=9\
		    -sOutputFile=$@ $<
		pdfcrop --bbox "0 220 600 380"  $@ $@
		pdfcrop $@ $@

build/dreiecksgen.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=10 -dLastPage=10\
		    -sOutputFile=$@ $<
		pdfcrop --bbox "0 400 600 592"  $@ $@
		pdfcrop $@ $@

build/schwingungsdiffgl.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=10 -dLastPage=10\
		    -sOutputFile=$@ $<
		pdfcrop --bbox "0 80 600 290"  $@ $@
		pdfcrop $@ $@

build/logarithmierer.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=12 -dLastPage=12\
		    -sOutputFile=$@ $<
		pdfcrop --bbox "0 520 600 688"  $@ $@
		pdfcrop $@ $@

build/exponentialgen.pdf: anleitung_V51_Operationsverstaerker.pdf | build
		gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		    -dFirstPage=12 -dLastPage=12\
		    -sOutputFile=$@ $<
		pdfcrop --bbox "0 135 600 295"  $@ $@
		pdfcrop $@ $@

FORCE:


build:
	mkdir -p build


clean:
	rm -rf *.pdf build


.PHONY: all clean FORCE preview
