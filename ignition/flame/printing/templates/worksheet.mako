Compute ${outputs} of size ${sizes} so
  that ${operation}
Given ${partition} with sizes ${partition_sizes}

${precondition}

while ${guard}
do
:: ${invariant}

:: repartition with sizes ${repartition_sizes}

${repartition}

::${before_update}


${update}

::${after_update}

${fuse}

:: ${postcondition}

done
