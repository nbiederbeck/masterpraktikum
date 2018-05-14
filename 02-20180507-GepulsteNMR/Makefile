BUILD_FILES = \
	build/aufspaltungE.pdf \
	build/effB.pdf \
	build/aufbau.pdf \
	build/spin.pdf \
	build/signalverlauf.pdf \
	build/echo.pdf \
	build/pulssequenz.pdf \
	build/magnetisierung.pdf \
	build/signalbild.pdf \
	build/meiboom.pdf \
	build/messung_T1.png \
	build/burst_sequences.png \
	build/halftime_sequence.png \
	build/messung_D.png \
	build/table_messung_D.tex \
	build/table_messung_T1.tex \
	build/burst_peaks_mg.png

OUT_DIR = build
TEX_CMD = latexmk \
	--pdf \
	--output-directory=$(OUT_DIR) \
	--halt-on-error \
	--interaction=nonstopmode
PREVIEW_CMD = \
	$(TEX_CMD) --pvc


all: build/main.pdf


anleitung_V49_GepulsteNMR.pdf:
	wget http://129.217.224.2/HOMEPAGE/PHYSIKER/MASTER/SKRIPT/V49.pdf -q \
		--user TUDoFP --password WS1718 \
		-O anleitung_V49_GepulsteNMR.pdf

Pulsed_NMR.pdf:
	wget https://www.physics.rutgers.edu/grad/506/Pulsed_NMR.pdf -q

build/main.pdf: $(BUILD_FILES) FORCE | build
	TEXINPUTS=build: BIBINPUTS=build: max_print_line=1048576 \
	$(TEX_CMD) main.tex

preview: FORCE | build
	TEXINPUTS=build: BIBINPUTS=build: max_print_line=1048576 \
	$(PREVIEW_CMD) main.tex

build/halftime_sequence.png: scripts/halftime.py matplotlibrc
	python scripts/halftime.py

build/table_messung_T1.tex: scripts/plot_T1.py data/messung_T1.txt matplotlibrc
	python scripts/plot_T1.py

build/table_messung_D.tex: scripts/plot_D.py data/messung_D.txt matplotlibrc
	python scripts/plot_D.py

build/messung_D.png: scripts/plot_D.py matplotlibrc
	python scripts/plot_D.py

build/messung_T1.png: scripts/plot_T1.py data/messung_T1.txt matplotlibrc
	python scripts/plot_T1.py

build/burst_sequences.png: scripts/bursts.py matplotlibrc
	python scripts/bursts.py

build/punktgitter.pdf: anleitung_V41_DebyeScherrer.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=2 -dLastPage=2 \
		-sOutputFile=build/punktgitter.pdf \
		anleitung_V41_DebyeScherrer.pdf
	pdfcrop --bbox "97 650 600 785" build/punktgitter.pdf build/punktgitter.pdf
	pdfcrop build/punktgitter.pdf build/punktgitter.pdf

build/aufspaltungE.pdf: anleitung_V49_GepulsteNMR.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=2 -dLastPage=2 \
		-sOutputFile=build/aufspaltungE.pdf \
		anleitung_V49_GepulsteNMR.pdf
	pdfcrop --bbox "0 190 480 350" build/aufspaltungE.pdf build/aufspaltungE.pdf
	pdfcrop build/aufspaltungE.pdf build/aufspaltungE.pdf

build/effB.pdf: anleitung_V49_GepulsteNMR.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=6 -dLastPage=6 \
		-sOutputFile=build/effB.pdf \
		anleitung_V49_GepulsteNMR.pdf
	pdfcrop --bbox "0 270 200 455" build/effB.pdf build/effB.pdf
	pdfcrop build/effB.pdf build/effB.pdf

build/aufbau.pdf: anleitung_V49_GepulsteNMR.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=7 -dLastPage=7 \
		-sOutputFile=build/aufbau.pdf \
		anleitung_V49_GepulsteNMR.pdf
	pdfcrop --bbox "200 290 600 490" build/aufbau.pdf build/aufbau.pdf
	pdfcrop build/aufbau.pdf build/aufbau.pdf

build/spin.pdf: anleitung_V49_GepulsteNMR.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=9 -dLastPage=9 \
		-sOutputFile=build/spin.pdf \
		anleitung_V49_GepulsteNMR.pdf
	pdfcrop --bbox "0 350 600 700" build/spin.pdf build/spin.pdf
	pdfcrop build/spin.pdf build/spin.pdf

build/signalverlauf.pdf: anleitung_V49_GepulsteNMR.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=9 -dLastPage=9 \
		-sOutputFile=build/signalverlauf.pdf \
		anleitung_V49_GepulsteNMR.pdf
	pdfcrop --bbox "0 100 600 280" build/spin.pdf build/signalverlauf.pdf
	pdfcrop build/signalverlauf.pdf build/signalverlauf.pdf

build/echo.pdf: anleitung_V49_GepulsteNMR.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=10 -dLastPage=10 \
		-sOutputFile=build/echo.pdf \
		anleitung_V49_GepulsteNMR.pdf
	pdfcrop --bbox "0 260 700 580" build/echo.pdf build/echo.pdf
	pdfcrop build/echo.pdf build/echo.pdf

build/pulssequenz.pdf: anleitung_V49_GepulsteNMR.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=11 -dLastPage=11 \
		-sOutputFile=build/pulssequenz.pdf \
		anleitung_V49_GepulsteNMR.pdf
	pdfcrop --bbox "0 500 600 680" build/pulssequenz.pdf build/pulssequenz.pdf
	pdfcrop build/pulssequenz.pdf build/pulssequenz.pdf

build/meiboom.pdf: anleitung_V49_GepulsteNMR.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=12 -dLastPage=12 \
		-sOutputFile=build/meiboom.pdf \
		anleitung_V49_GepulsteNMR.pdf
	pdfcrop --bbox "0 290 600 623" build/meiboom.pdf build/meiboom.pdf
	pdfcrop build/meiboom.pdf build/meiboom.pdf

build/magnetisierung.pdf: anleitung_V49_GepulsteNMR.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=17 -dLastPage=17 \
		-sOutputFile=build/magnetisierung.pdf \
		anleitung_V49_GepulsteNMR.pdf
	pdfcrop --bbox "0 290 600 623" build/magnetisierung.pdf build/magnetisierung.pdf
	pdfcrop build/magnetisierung.pdf build/magnetisierung.pdf

build/signalbild.pdf: anleitung_V49_GepulsteNMR.pdf | build
	gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
		-dFirstPage=18 -dLastPage=18 \
		-sOutputFile=build/signalbild.pdf \
		anleitung_V49_GepulsteNMR.pdf
	pdfcrop --bbox "0 560 600 700" build/signalbild.pdf build/signalbild.pdf
	pdfcrop build/signalbild.pdf build/signalbild.pdf


FORCE:


build:
	@mkdir -p build


clean:
	rm -rf *.pdf build

.PHONY: all clean FORCE preview
