# Minimal makefile for Sphinx documentation

# Treat warnings as errors so CI fails on Sphinx warnings (including MyST fence issues).
SPHINXOPTS    ?= -W --keep-going
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile vendor-upstream vendor-check

# English build (default)
html:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

# Chinese build
html-zh_CN:
	@$(SPHINXBUILD) -b html -D language=zh_CN "$(SOURCEDIR)" "$(BUILDDIR)/html/zh_CN" $(SPHINXOPTS) $(O)

# Build both languages
html-all: html html-zh_CN

# Extract translatable strings
gettext:
	@$(SPHINXBUILD) -b gettext "$(SOURCEDIR)" "$(BUILDDIR)/gettext" $(SPHINXOPTS) $(O)

# Update translation catalogs
update-po:
	@sphinx-intl update -p "$(BUILDDIR)/gettext" -l zh_CN

# Clean build directory
clean:
	rm -rf "$(BUILDDIR)"

# Fetch pinned upstream Markdown into source/_vendored/ (see SOURCES.json).
vendor-upstream:
	python3 scripts/vendor_upstream_md.py --sync

# Verify vendored files match the recorded commit SHA (no network).
vendor-check:
	python3 scripts/vendor_upstream_md.py --check

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
