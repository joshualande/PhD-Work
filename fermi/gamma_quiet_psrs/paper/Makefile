manuscript = gamma_quiet_psrs

# These commands make sure no compression is applied
# when running ps2pdf
# http://cosmocoffee.info/viewtopic.php?p=213
PS2PDFARGS = "-dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode"

DEFBWFIGS = \def\bwfigures{true}

color: $(manuscript).pdfcolor

bw: $(manuscript).pdfbw


%.pdfcolor: %.dvicolor
	dvips $(manuscript)
	ps2pdf ${PS2PDFARGS} $(manuscript).ps

%.pdfbw: %.dvibw
	dvips $(manuscript)
	ps2pdf ${PS2PDFARGS} $(manuscript).ps

%.dvibw: %.tex
	latex "${DEFBWFIGS} \input{$(manuscript)}"
	bibtex $(manuscript) 
	latex "${DEFBWFIGS} \input{$(manuscript)}"
	latex "${DEFBWFIGS} \input{$(manuscript)}"

%.dvicolor: %.tex
	latex $(manuscript).tex
	bibtex $(manuscript) 
	latex $(manuscript).tex
	latex $(manuscript).tex

clean:
	-rm -f $(manuscript).aux $(manuscript).log $(manuscript).out \
      $(manuscript).toc $(manuscript).dvi $(manuscript).bbl \
      $(manuscript).blg $(manuscript).ps $(manuscript).tdo

