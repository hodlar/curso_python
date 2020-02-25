all:
	pdflatex curso_python.tex
	sleep 1
	pdflatex curso_python.tex
	sleep 1
	okular curso_python.pdf
clean:
	rm *.aux *.log *.nav *.out *.toc *.vrb *.snm
