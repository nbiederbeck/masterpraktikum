BUILD_FILES = $(addprefix build/, \
	$(addsuffix .pdf, \
		aufspaltungen \
		aufbau \
		dublett \
		auswahlregeln \
		transparenz \
		resonanz \
	) \
	$(addsuffix .png, \
		$(addprefix firstPeak_, \
			1 2 3 4 5 6 7 8 9 10 \
		) \
		$(addprefix secondPeak_, \
			3 4 5 6 7 8 9 10 \
		) \
	) \
	$(addsuffix .tex, \
		b_nu \
		lin_params \
		lande \
		kernspin \
		static_B \
		T1 \
		T2 \
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
CUT = gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER
CROP = pdfcrop $@ $@


all: build/main.pdf

build/resonanz.pdf: anleitung_V21_OptischePumpen.pdf | build
	$(CUT) -dFirstPage=11 -dLastPage=11 -sOutputFile=$@ $<
	$(CROP) --bbox "100 110 600 250"
	$(CROP)


build/transparenz.pdf: anleitung_V21_OptischePumpen.pdf | build
	$(CUT) -dFirstPage=8 -dLastPage=8 -sOutputFile=$@ $<
	$(CROP) --bbox "0 370 420 530"
	$(CROP)


build/auswahlregeln.pdf: anleitung_V21_OptischePumpen.pdf | build
	$(CUT) -dFirstPage=6 -dLastPage=6 -sOutputFile=$@ $<
	$(CROP) --bbox "0 470 420 677"
	$(CROP)


build/dublett.pdf: anleitung_V21_OptischePumpen.pdf | build
	$(CUT) -dFirstPage=5 -dLastPage=5 -sOutputFile=$@ $<
	$(CROP) --bbox "0 125 600 295"
	$(CROP)


build/aufbau.pdf: anleitung_V21_OptischePumpen.pdf | build
	$(CUT) -dFirstPage=16 -dLastPage=16 -sOutputFile=$@ $<
	$(CROP) --bbox "0 385 600 650"
	$(CROP)


build/aufspaltungen.pdf: anleitung_V21_OptischePumpen.pdf | build
	$(CUT) -dFirstPage=4 -dLastPage=4 -sOutputFile=$@ $<
	$(CROP) --bbox "0 160 600 545"
	$(CROP)


anleitung_V21_OptischePumpen.pdf:
	wget http://129.217.224.2/HOMEPAGE/PHYSIKER/MASTER/SKRIPT/V21n_TeachSpin_new.pdf -q \
		--user TUDoFP --password WS1819 -O $@


build/main.pdf: $(BUILD_FILES) FORCE | build
	TEXINPUTS=build: BIBINPUTS=build: max_print_line=1048576 \
	$(TEX_CMD) main.tex

build/firstPeak_1.png: build/firstPeak_2.png
build/firstPeak_2.png: build/firstPeak_3.png
build/firstPeak_3.png: build/firstPeak_4.png
build/firstPeak_4.png: build/firstPeak_5.png
build/firstPeak_5.png: build/firstPeak_6.png
build/firstPeak_6.png: build/firstPeak_7.png
build/firstPeak_7.png: build/firstPeak_8.png
build/firstPeak_8.png: build/firstPeak_9.png
build/firstPeak_9.png: build/firstPeak_10.png
build/firstPeak_10.png: build/secondPeak_3.png
build/secondPeak_3.png: build/secondPeak_4.png
build/secondPeak_4.png: build/secondPeak_5.png
build/secondPeak_5.png: build/secondPeak_6.png
build/secondPeak_6.png: build/secondPeak_7.png
build/secondPeak_7.png: build/secondPeak_8.png
build/secondPeak_8.png: build/secondPeak_9.png
build/secondPeak_9.png: build/secondPeak_10.png
build/secondPeak_10.png: build/b_nu.tex
build/b_nu.tex: build/lin_params.tex
build/lin_params.tex: build/lande.tex
build/lande.tex: build/kernspin.tex
build/kernspin.tex: build/static_B.tex
build/static_B.tex: build/T2.tex
build/T2.tex: build/T1.tex
build/T1.tex: plots.py
	python $<


preview: $(BUILD_FILES) FORCE | build
	TEXINPUTS=build: BIBINPUTS=build: max_print_line=1048576 \
	$(PREVIEW_CMD) main.tex


FORCE:


build:
	@mkdir -p build


clean:
	rm -rf *.pdf build


.PHONY: all clean FORCE preview
