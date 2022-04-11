BUILDDIR	= docs/build/singlehtml

all:
	$(MAKE) -C docs singlehtml
	cp -r $(BUILDDIR)/_static static
	cp $(BUILDDIR)/index.html index.html

.PHONY: clean

clean: 
	rm -rf static index.html