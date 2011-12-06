paper = lande_ext_src_search_walthrough

all: 
	latex $(paper)
	latex $(paper)
	dvips $(paper)
	ps2pdf -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode $(paper).ps
	rm $(paper).dvi
	rm $(paper).ps


clean:
	rm -f $(paper).aux $(paper).log $(paper).out \
		$(paper).toc $(paper).bbl \
		$(paper).blg $(paper).nav $(paper).snm
