BUILD_FILES = \

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


preview: FORCE | build
	TEXINPUTS=build: BIBINPUTS=build: max_print_line=1048576 \
	$(PREVIEW_CMD) main.tex


FORCE:


build:
	@mkdir -p build


clean:
	rm -rf *.pdf build

.PHONY: all clean FORCE preview
