<%namespace file="license.mako" import="license" />${license('%')}

%% Define the operation to be computed
\resetsteps

\renewcommand{\WSoperation}{Compute ${outputs} of size ${sizes} so
  that ${operation}}

\renewcommand{\WSprecondition}{${precondition}}

\renewcommand{\WSpostcondition}{${postcondition}}

\renewcommand{\WSpartition}{${partition}}

\renewcommand{\WSpartitionsizes}{${partition_sizes}}

\renewcommand{\WSrepartition}{${repartition}}

\renewcommand{\WSrepartitionsizes}{${repartition_sizes}}
\renewcommand{\WSmoveboundary}{${fuse}}

\renewcommand{\WSguard}{${guard}}

\renewcommand{\WSinvariant}{${invariant}}

\renewcommand{\WSbeforeupdate}{${before_update}}

\renewcommand{\WSafterupdate}{${after_update}}

\renewcommand{\WSupdate}{${update}}

\begin{figure}[tb!]
  \centering\small
  \worksheet
   \caption{${caption}}
  \label{fig:${label}}
\end{figure}
