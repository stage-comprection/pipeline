
DIRS = dbg_correction evaluation_correction format_reads_file filter_sam_output
BUILDDIRS = $(DIRS:%=build-%)
CLEANDIRS = $(DIRS:%=clean-%)

all: $(BUILDDIRS)
$(DIRS): $(BUILDDIRS)
$(BUILDDIRS):
	git submodule foreach git pull origin master
	$(MAKE) -C ./cpp/$(@:build-%=%)
	chmod +x run_pipeline.py


clean: $(CLEANDIRS)
$(CLEANDIRS):
	$(MAKE) -C ./cpp/$(@:clean-%=%) clean
	rm -rf binaries/$(@:clean-%=%)


install: init $(BUILDDIRS)

init:
	git submodule foreach git pull origin master



.PHONY: $(SUBDIRS)
.PHONY: $(CLEANDIRS)
.PHONY: clean
.PHONY: all
.PHONY: install 
.PHONY: init
