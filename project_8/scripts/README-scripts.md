# Scripts folder purpose and contents

When analyzing and visualizing data, often we need a pipeline of 
different processing steps, some of which might be Python programs 
and some of which might be other software.  We may need to repeat 
those steps consistently for many input files.  A script (e.g., a 
Unix shell script) is one way to automate and document such a series 
of steps.  (There are others, some of which are more suited to 
complex workflows or to careful documentation of data provenance.)

The scripts folder is where we can keep some simple Unix shell 
scripts that combine steps leading from raw data files (typically in 
CSV format from spreadsheets or databases) to treemap visualizations.
This might involve some restructuring with Python programs in the 
`restructure` folder before visualizing with the `treemap` program. 



