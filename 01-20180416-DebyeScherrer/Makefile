.PHONY: all
all: anleitung_V41_DebyeScherrer.pdf

anleitung_V41_DebyeScherrer.pdf:
	wget http://129.217.224.2/HOMEPAGE/PHYSIKER/MASTER/SKRIPT/V41.pdf \
		--user TUDoFP --password WS1718 \
		-O anleitung_V41_DebyeScherrer.pdf

.PHONY: clean
clean:
	rm -rf anleitung_V41_DebyeScherrer.pdf
	rm -rf build
