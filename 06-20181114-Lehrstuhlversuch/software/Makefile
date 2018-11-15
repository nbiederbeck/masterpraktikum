all: build/installation_software.pdf

build:
	mkdir -p $@

build/installation_software.pdf: installation_software.md | build
	pandoc -i $< -o $@

clean:
	rm -rf build

.PHONY: all clean
