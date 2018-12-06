all: ../build/theta2.pdf ../build/hadroness.pdf

../build: 
	mkdir -p $@

../build/theta2.pdf: theta2.py | ../build
		python $<

../build/hadroness.pdf: hadroness.py | ../build
		python $<

FORCE:

clean:
	rm -rf ../build/theta2.pdf ../build/hadroness.pdf

.PHONY: all clean FORCE
