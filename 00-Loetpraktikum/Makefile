all: Loetpraktikum.pdf

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

anleitung.pdf:
	wget http://129.217.224.2/HOMEPAGE/PHYSIKER/MASTER/SKRIPT/ArbeitsblLoet.pdf -q \
		--user TUDoFP --password WS1819 -O $@


$(all_plots): Loetpraktikum.py $(all_data) plots
	python Loetpraktikum.py

plots:
	mkdir -p plots

Loetpraktikum.pdf: $(all_plots)
	gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite \
		-sOutputFile=Loetpraktikum.pdf \
		$(all_plots)

clean:
	rm -rf plots
	rm -f Loetpraktikum.pdf

.PHONY: clean
