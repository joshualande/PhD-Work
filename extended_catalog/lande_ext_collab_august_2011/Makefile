base = collaboration_meeting_presentation
extended_catalog:
	latex $(base)
	latex $(base)
	dvips $(base)
	# These commands make sure no compression is applied
	# # http://cosmocoffee.info/viewtopic.php?p=213
	ps2pdf -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode $(base).ps
	rm $(base).dvi
	rm $(base).ps

clean:
	rm -f $(base).aux $(base).log $(base).out \
		$(base).toc $(base).bbl \
		$(base).blg $(base).nav $(base).snm

