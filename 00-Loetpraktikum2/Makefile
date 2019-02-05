all: Loetpraktikum.pdf

anleitung.pdf:
	wget http://129.217.224.2/HOMEPAGE/PHYSIKER/MASTER/SKRIPT/ArbeitsblLoet.pdf -q \
		--user TUDoFP --password WS1819 -O $@

all_plots = $(addprefix plots/, \
	diode_Diode_Durchlassrichtung.pdf \
	diode_Diode_Sperrrichtung.pdf \
	diode_Zener-Diode_Durchlassrichtung.pdf \
	diode_Zener-Diode_Sperrrichtung.pdf \
	spannungsteiler_R_L=100Ohm.pdf \
	spannungsteiler_R_L=100kOhm.pdf \
	spannungsteiler_R_L=1kOhm.pdf \
)

all_data = $(addprefix data/, \
	diode.csv spannungsteiler.csv )


build:
	mkdir -p $@

Loetpraktikum.pdf: $(all_plots)
	gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite \
		-sOutputFile=Loetpraktikum.pdf \
		$(all_plots)

plots:
	mkdir -p plots


$(all_plots): Loetpraktikum.py $(all_data) plots
	python Loetpraktikum.py

clean:
	rm -f anleitung.pdf
	rm -rf build

.PHONY: clean
