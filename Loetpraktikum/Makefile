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

$(all_plots): Loetpraktikum.py $(all_data) plots
	python Loetpraktikum.py

plots:
	mkdir -p plots

Loetpraktikum.pdf: Loetpraktikum.md $(all_plots)
	pandoc -o Loetpraktikum.pdf Loetpraktikum.md
