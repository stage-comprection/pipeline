
DIRS = dbg_correction evaluation_correction format_reads_file filter_sam_output
BUILDDIRS = $(DIRS:%=build-%)
CLEANDIRS = $(DIRS:%=clean-%)

all: update $(BUILDDIRS)
$(BUILDDIRS):
	$(MAKE) -C ./cpp/$(@:build-%=%)
	chmod +x run_pipeline.py


clean: $(CLEANDIRS)
$(CLEANDIRS):
	$(MAKE) -C ./cpp/$(@:clean-%=%) clean
	rm -rf binaries/$(@:clean-%=%)


init: install $(BUILDDIRS)


install: 
	mkdir binaries
	mkdir ext


update:
	git submodule foreach git pull origin master
	


.PHONY: $(SUBDIRS)
.PHONY: $(CLEANDIRS)
.PHONY: clean
.PHONY: all
.PHONY: init
