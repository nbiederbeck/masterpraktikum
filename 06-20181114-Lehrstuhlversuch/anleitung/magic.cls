\ProvidesClass{magic}
\LoadClass{scrartcl}


\RequirePackage{caption}
\RequirePackage{subcaption}


\RequirePackage{xcolor}
\xdefinecolor{mblue}{RGB}{43, 50, 122}
\definecolor{myellow}{RGB}{228, 188, 15}
\DeclareCaptionFont{myellow}{\color{myellow}}

\addtokomafont{title}{\color{mblue}}      
\addtokomafont{paragraph}{\color{mblue}}
\addtokomafont{subparagraph}{\color{mblue!70}}
\addtokomafont{section}{\color{mblue}}
\addtokomafont{subsection}{\color{mblue}}
\addtokomafont{pagenumber}{\color{mblue!70}} 

\captionsetup{%
	labelfont={bf, myellow},     % bold label in colour
	format=plain,               % no indentation under the label
	width=0.9\textwidth,        % slightly smaller width than text
	font=small,                 % font slightly smaller than text
}
