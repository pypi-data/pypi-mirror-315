# ErrorFieldConcordance

Thie package provides calculation (and optionally graphing) of concordance (trending agreement) between two measures using an error field method.

## Function Call
After importing the package, the method can be called as follows:

```
Concordance = ErrorFieldConcordance(X,Y,IDS=[], plot_TF=False,graph_label='',X_name='ΔX',Y_name='ΔY',min_plot_range=3,decolor_threshold=2)
```

Function Parameters:
+ The X and Y parameters are lists or arrays of equal size corresponding to paired measures to be compared. These should be the observations themselves (not the changes observed between observations).  
+ IDS is a list of the same length as X & Y containing subject identifiers for individual subjects in the lists. If all of the observations are from the same subject this parameter can be empty.
+ plot_TF is a boolean that controls whether or not a figure is created.
+ graph_label is an optional string parameter to be placed in the graph title.
+ XMeasName and YMeasName are used to customize the X and Y graph labels if desired
+ MinPlotRange can be used to extend the plot range if desired. Normally the plot will include ± the largest absolute change observed, but if this range is too small the MinPlotRange parameter can be used to fix a minimum axis range.
+ decolor_threshold sets the radius for the desaturation circle at the center of the graph.  This is a graphical/appearance modifier only, it has no effect on the calculation of the Error Field Concordance value, but is useful to visually represent the central region where points are weighted the least in the final calculation.

## Notes
The observations passed in X & Y (and the corresponding subject identifiers in IDs) should be grouped by subject and ordered temporally. The function will then calculate the changes in successive observations within subjects.  If X, Y, and IDS are not grouped by subject and ordered by time results will be invalid.

Time differences in the observations should be based on the aims of the project; the function itself is agnostic to the specifics. Ideally the time differences are all the same, otherwise interpretation of the graph and results may be biased.

## Output

The returned value is a tuple of (error field concordance %, standard deviation %).  

The error field concordance value is a number in the range of \[-100,100\]:  
+ Values > 60% indicate strong concordance.
+ Values between +20% and +60% indicate concordance.
+ Values between -20% and +20% indicate relative independence, or low overall change in the sample.
+ Values between -60% and -20% indicate discordance.
+ Values less than -60% indicate strong discordance.  
 

## Graphing
![Example Error Field Concordance graph showing plotting of random data](https://www.wtfstatistics.com/assets/ExampleFigure1.png)

The figure above shows an Error Field Concordance plot for two 1,000 sample arrays of noise (i.e. independent samples).  The data demonstrates the fields in the plot, with blue zones indicating concordance (the measures move in the same direction and magnitude), red zones indicating discordance (the measures move in opposite directions), and yellow zones indicating relative independence of movement.

## Citing
Please cite this package using the following:  *PubMed Reference & Citation TBD*

## Contributors
Thanks go out to Bernd Saugel, Sean Coeckelenbergh, Ishita Srivastava, and Brandon Woo for their collective contributions to this project.