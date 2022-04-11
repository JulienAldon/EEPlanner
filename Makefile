BUILDDIR	= docs/build/singlehtml

all:
	$(MAKE) -C docs singlehtml
	cp -r $(BUILDDIR)/_static .
	cp $(BUILDDIR)/index.html .

.PHONY: clean

clean: 
	rm -rf static index.html