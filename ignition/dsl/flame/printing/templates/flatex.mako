<%namespace file="license.mako" import="license" />${license('%')}

%% Define the operation to be computed
\resetsteps

\renewcommand{\WSoperation}{Compute ${outputs} of size ${sizes} so
  that ${operation}}

\renewcommand{\WSpartition}{${partition}}

\renewcommand{\WSpartitionsizes}{${partition_sizes}}

\renewcommand{\WSinvariant}{${invariant}}

\renewcommand{\WSguard}{${guard}}

\renewcommand{\WSprecondition}{${precondition}}

\renewcommand{\WSrepartition}{${repartition}}

\renewcommand{\WSrepartitionsizes}{${repartition_sizes}}

\renewcommand{\WSbeforeupdate}{${before_update}}

\renewcommand{\WSupdate}{${update}}

\renewcommand{\WSafterupdate}{${after_update}}

\renewcommand{\WSmoveboundary}{${fuse}}

\renewcommand{\WSpostcondition}{${postcondition}}

\begin{figure}[tb!]
  \centering\small
  \worksheet
   \caption{${caption}}
  \label{fig:${label}}
\end{figure}
