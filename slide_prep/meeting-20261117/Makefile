.PHONY: all
all:
	python3 make_figure_data.py > /dev/null
	pdflatex -interaction=nonstopmode -halt-on-error slides.tex
	pdflatex -interaction=nonstopmode -halt-on-error slides.tex
	mkdir -p render
	rm -f render/slide-*.png
	pdftoppm -png -r 140 slides.pdf render/slide
