SUBDIRS := $(sort $(wildcard */))

all: protokolle.pdf anleitungen.pdf 06-20181114-Lehrstuhlversuch/anleitung/build/anleitung.pdf

protokolle=\
	01-20180416-DebyeScherrer/build/main.pdf \
	02-20180507-GepulsteNMR/build/main.pdf \
	03-20180611-Diodenlaser/build/main.pdf \
	04-20180702-Operationsverstaerker/build/main.pdf \
	05-20181015-OptischePumpen/build/main.pdf \

01-20180416-DebyeScherrer/build/main.pdf:
	$(MAKE) -C ./01-20180416-DebyeScherrer build/main.pdf

02-20180507-GepulsteNMR/build/main.pdf:
	$(MAKE) -C ./02-20180507-GepulsteNMR build/main.pdf

03-20180611-Diodenlaser/build/main.pdf:
	$(MAKE) -C ./03-20180611-Diodenlaser build/main.pdf

04-20180702-Operationsverstaerker/build/main.pdf:
	$(MAKE) -C ./04-20180702-Operationsverstaerker build/main.pdf

05-20181015-OptischePumpen/build/main.pdf:
	$(MAKE) -C ./05-20181015-OptischePumpen build/main.pdf

06-20181114-Lehrstuhlversuch/anleitung/build/anleitung.pdf:
	$(MAKE) -C ./06-20181114-Lehrstuhlversuch/anleitung build/anleitung.pdf

protokolle.pdf: $(protokolle)
	pdfunite \
		01-20180416-DebyeScherrer/build/main.pdf \
		02-20180507-GepulsteNMR/build/main.pdf \
		03-20180611-Diodenlaser/build/main.pdf \
		04-20180702-Operationsverstaerker/build/main.pdf \
		05-20181015-OptischePumpen/build/main.pdf \
		$@

anleitungen=\
	01-20180416-DebyeScherrer/anleitung_V41_DebyeScherrer.pdf \
	02-20180507-GepulsteNMR/anleitung_V49_GepulsteNMR.pdf \
	03-20180611-Diodenlaser/anleitung_V60_Diodenlaser.pdf \
	04-20180702-Operationsverstaerker/anleitung_V51_Operationsverstaerker.pdf \
	05-20181015-OptischePumpen/anleitung_V21_OptischePumpen.pdf

01-20180416-DebyeScherrer/anleitung_V41_DebyeScherrer.pdf:
	$(MAKE) -C ./01-20180416-DebyeScherrer anleitung_V41_DebyeScherrer.pdf
02-20180507-GepulsteNMR/anleitung_V49_GepulsteNMR.pdf:
	$(MAKE) -C ./02-20180507-GepulsteNMR anleitung_V49_GepulsteNMR.pdf
03-20180611-Diodenlaser/anleitung_V60_Diodenlaser.pdf:
	$(MAKE) -C ./03-20180611-Diodenlaser anleitung_V60_Diodenlaser.pdf
04-20180702-Operationsverstaerker/anleitung_V51_Operationsverstaerker.pdf:
	$(MAKE) -C ./04-20180702-Operationsverstaerker anleitung_V51_Operationsverstaerker.pdf
05-20181015-OptischePumpen/anleitung_V21_OptischePumpen.pdf:
	$(MAKE) -C ./05-20181015-OptischePumpen anleitung_V21_OptischePumpen.pdf


anleitungen.pdf: $(anleitungen)
	pdfunite \
		01-20180416-DebyeScherrer/anleitung_V41_DebyeScherrer.pdf \
		02-20180507-GepulsteNMR/anleitung_V49_GepulsteNMR.pdf \
		03-20180611-Diodenlaser/anleitung_V60_Diodenlaser.pdf \
		04-20180702-Operationsverstaerker/anleitung_V51_Operationsverstaerker.pdf \
		05-20181015-OptischePumpen/anleitung_V21_OptischePumpen.pdf \
		$@

clean:
	$(foreach dir, $(SUBDIRS), $(MAKE) -C $(dir) clean;)
