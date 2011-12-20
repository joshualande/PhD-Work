base = extended_search
extended_search:
#	pdflatex extended_search
#	bibtex extended_search
#	pdflatex extended_search
#	pdflatex extended_search
	latex $(base)
	bibtex $(base) 
	latex  $(base)
	latex  $(base)
	dvips $(base)
	# These commands make sure no compression is applied
	# # http://cosmocoffee.info/viewtopic.php?p=213
	ps2pdf -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode $(base).ps

clean:
	-rm -f $(base).aux $(base).log $(base).out \
      $(base).toc $(base).dvi $(base).bbl \
      $(base).blg $(base).ps

