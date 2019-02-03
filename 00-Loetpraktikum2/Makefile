all: anleitung.pdf

anleitung.pdf:
	wget http://129.217.224.2/HOMEPAGE/PHYSIKER/MASTER/SKRIPT/ArbeitsblLoet.pdf -q \
		--user TUDoFP --password WS1819 -O $@

build:
	mkdir -p $@ 

Loetpraktikum.pdf: $(all_plots)
	gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite \
		-sOutputFile=Loetpraktikum.pdf \
		$(all_plots)

clean:
	rm -f anleitung.pdf
	rm -rf build

.PHONY: clean
