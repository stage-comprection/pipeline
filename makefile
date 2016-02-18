# This is a bit a fraud, just launching makefiles

DIRS = dbg_correction evaluation_correction format_reads_file filter_sam_output
BUILDDIRS = $(DIRS:%=build-%)
CLEANDIRS = $(DIRS:%=clean-%)

all: $(BUILDDIRS)
$(DIRS): $(BUILDDIRS)
$(BUILDDIRS):
	$(MAKE) -C ./cpp/$(@:build-%=%)
	chmod +x run_pipeline.py


clean: $(CLEANDIRS)
$(CLEANDIRS):
	$(MAKE) -C ./cpp/$(@:clean-%=%) clean
	rm -rf binaries/$(@:clean-%=%)


.PHONY: $(SUBDIRS)
.PHONY: $(CLEANDIRS)
.PHONY: clean
.PHONY: all
