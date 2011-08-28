cat = lande_cat_ext_collab_august_2011

all: catalog galactic 

catalog:
	latex $(cat)
	latex $(cat)
	dvips $(cat)
	ps2pdf -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode $(cat).ps
	rm $(cat).dvi
	rm $(cat).ps

gal = lande_gal_ext_collab_august_2011
galactic:
	latex $(gal)
	latex $(gal)
	dvips $(gal)
	ps2pdf -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode $(gal).ps
	rm $(gal).dvi
	rm $(gal).ps

clean:
	rm -f $(cat).aux $(cat).log $(cat).out \
		$(cat).toc $(cat).bbl \
		$(cat).blg $(cat).nav $(cat).snm
	rm -f $(gal).aux $(gal).log $(gal).out \
		$(gal).toc $(gal).bbl \
		$(gal).blg $(gal).nav $(gal).snm
