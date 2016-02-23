
DIRS = dbg_correction evaluation_correction format_reads_file bowtie_to_reads
BUILDDIRS = $(DIRS:%=build-%)
CLEANDIRS = $(DIRS:%=clean-%)
INITDIRS = $(DIRS:%=init-%)

all: update $(BUILDDIRS)
$(BUILDDIRS):
	$(MAKE) -C ./cpp/$(@:build-%=%)


clean: $(CLEANDIRS)
$(CLEANDIRS):
	$(MAKE) -C ./cpp/$(@:clean-%=%) clean
	rm -rf binaries/$(@:clean-%=%)


init: makedirs $(INITDIRS) permission
$(INITDIRS):
	$(MAKE) -C ./cpp/$(@:init-%=%) init


makedirs: 
	mkdir binaries


permission:
	chmod +x run_pipeline.py


update:
	git submodule foreach git pull origin master
	


.PHONY: $(SUBDIRS)
.PHONY: $(CLEANDIRS)
.PHONY: clean
.PHONY: all
.PHONY: init
