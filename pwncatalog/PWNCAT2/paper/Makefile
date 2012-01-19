manuscript = pwncat2

latexbw:
	latex "\newif\ifcolorfigure\colorfigurefalse\input{$(manuscript)}"
	
latexcolor:
	latex "\newif\ifcolorfigure\colorfiguretrue\input{$(manuscript)}"

dvips:
	dvips $(manuscript)

ps2pdf:
	# These commands make sure no compression is applied
	# # http://cosmocoffee.info/viewtopic.php?p=213
	ps2pdf -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode $(manuscript).ps

color:
	latexcolor
	bibtex $(manuscript) 
	latexcolor
	latexcolor
	dvips
	ps2pdf

bw:
	latexbw
	bibtex $(manuscript) 
	latexbw
	latexbw
	dvips
	ps2pdf

all:
	color

clean:
	-rm -f $(manuscript).aux $(manuscript).log $(manuscript).out \
      $(manuscript).toc $(manuscript).dvi $(manuscript).bbl \
      $(manuscript).blg $(manuscript).ps

