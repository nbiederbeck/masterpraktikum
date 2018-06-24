BUILD_FILES = $(addprefix build/, \
	$(addsuffix .pdf, \
	\
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


FORCE:


build:
	mkdir -p build


clean:
	rm -rf *.pdf build


.PHONY: all clean FORCE preview
