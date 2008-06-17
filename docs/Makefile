all:
	asciidoc -b xhtml11 vigedit.1.txt
	asciidoc -b xhtml11 index.txt
	cat vigedit.1.txt | asciidoc -d manpage -b docbook - | xsltproc --nonet /etc/asciidoc/docbook-xsl/manpage.xsl -
