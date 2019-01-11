all: $(addprefix build/, \
	20190111-Betz.pdf \
	)

build:
	mkdir -p $@

build/20190111-Betz.pdf: 20190111-Betz.md | build
	pandoc -i $< -o $@

clean:
	rm -rf build

.PHONY: all clean
