SUBDIRS := $(sort $(wildcard */))

all: 01 02 03 04 05
	# $(foreach dir, $(SUBDIRS), $(MAKE) -C $(dir); )

01:
	$(MAKE) -C ./01-20180416-DebyeScherrer

02:
	$(MAKE) -C ./02-20180507-GepulsteNMR

03:
	$(MAKE) -C ./03-20180611-Diodenlaser

04:
	$(MAKE) -C ./04-20180702-Operationsverstaerker

05:
	$(MAKE) -C ./05-20181015-OptischePumpen




clean:
	$(foreach dir, $(SUBDIRS), $(MAKE) -C $(dir) clean;)
