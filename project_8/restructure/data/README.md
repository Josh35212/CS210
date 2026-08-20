# Raw (implicitly hierarchical) data for structuring

Hierarchical data often comes in the form of "flat" (text, 
spreadsheets, or databases) in which containment relations are 
indicated through contents of data fields. This structure is often 
less explicit than, say, a JSON file.  

Example:  Microsoft Excel 
[can produce treemap diagrams](
https://support.microsoft.com/en-us/office/create-a-treemap-chart-in-office-dfe86d28-a610-4ef5-9b30-362d5c624b68)
from data in which the contents of each row are essentially a path from the root 
of a tree to a leaf, and all paths are the same length.  File
[SCH-flat.csv](SCH-flat.csv) (starting from row 2) is an example
of such data.  A JSON equivalent might be
```json
"CS": {
      "1xx": { "CS 102": 376,
                "CS 110":  976,
                "CS 111": 564,
                "CS 122": 432 },
      "2xx": {  "CS 211": 552, 
                "CS 212": 496 }, 
etc.
```
[SCH-indent.csv](SCH-indent.csv) is semantically the same data, but
in a form that places each "subhead" on a row by itself, much like
a bulleted list or table of contents. 

Such "flat" representations of hierarchical data often require some 
additional processing to select and aggregate data before 
its hierarchical structure can be recovered.   For example, file
[enrollments-24S.csv](enrollments-24S.csv),
which is the ultimate source for the student credit hour (SCH) 
counts, was produced by pasting the Spring 2024 classs schedule for 
computer science into an Excel spreadsheet.  The student credit 
hours associated with each class were computed from credit hours for 
the class (e.g., 4 credits for CS 211 lecture) multiplied by 
enrollment, which enrollment in turn was calculated as the 
difference between class capacity and available seats.  For example, 
CS 211 lecture had a capacity of 150, but 12 were open, so we infer 
138 students were enrolled.  4 credits times 138 students is 552 
student credit hours. (Labs add another 138 student credit hours 
asociated with that class offering.)

## Recovering structure

The implicit hierarchical structure can be made explicit in at least 
two ways.  The clearest is probably to construct nested dictionaries 
in memory, then dump them as json.  I have provided two utility 
programs for this purpose. 

- `csv_to_json.py` extracts nested dictionary structures from a CSV 
  file with column headers (the kind of CSV file that a
  Python `csv.DictReader` can interpret).  Some of the columns 
  are interpreted as levels in the hierarchy, and at least 
  one column is interpreted as data (usually numeric) associated 
  with leaves of the tree.  `csv_to_json.py` requires a schema file 
  like `data/csv_config.json` (for `data/SCH-flat.csv`)
  or `data/park_visit_schema.json` (for 
  `data/US-National-Parks_Recreation_Visits_1979-2023.csv`)
  to identify columns by column headers.  `csv_to_json.py`
  can process CSV files in an indented format, selecting
  lines with data in the relevant columns and filling in
  omitted labels from earlier lines. 
- `schematize.py` applies a separate schema (not represented by 
  columns) to a flat list of (key, value) pairs.  For example,
  `python3 schematize.py data/sch-schema.json data/sch.csv`
  groups elements of `sch.csv` according to the patterns in 
  `sch-schema.json`. 


It is also possible to translate 
the flat file directly into a json representation, without building 
the nested dictionaries, using "control break logic."  Control break 
logic was once very common in programs that produced business 
reports, payroll, etc., from business data bases, but it is much 
less common today, and almost non-existant in computer science 
textbooks except for texts on legacy languages like COBOL and RPG.
Despite its unfashionabilty, control break logic is still useful in 
processing many flat file formats. 

The idea of control break logic is simple:  On reading each record 
(e.g., each line of a CSV file), one looks for differences in header 
("control") fields.  A change at level i (e.g., the "Program" field of
`SCH-flat.csv`) is a "control break" that implicitly also signals a 
break at each lower level (e.g., the "Level" field). 

Common spreadsheet programs like Excel can do some grouping and 
totalling using control break logic.  
Frustratingly, Excel places subtotals in the same column as detail 
data, and not in a separate column for subtotals.
It may be useful to write (yet another) Python script to
summarize data using control break logic before producing the 
hierarchical representation. 

## Data sources

The [National Parks visit database](
US-National-Parks_RecreationVisits_1979-2023.csv)
is taken from [Responsible Datasets in context](
https://www.responsible-datasets-in-context.com/), 
a source for datasets paired with rich documentation.
Please refer students to the accompanying
[documentation on national parks data](
https://www.responsible-datasets-in-context.com/posts/np-data/
) if you use this dataset in a class project.
This data is shared in accordance with its
Creative Commons license
[CC by by 4.0](
https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1).  
The datasets were curated and published by Melanie Walsh, and the data
essay was written by Melanie Walsh and Os Keyes.

[Our World in Data](https://ourworldindata.org/)
is an additional source of rich, open source datasets, mostly
in CSV format.  Not all the datasets at Our World in Data are
downloadable, but many are.  In many cases it is apparent that the
downloadable dataset must be combined ("joined") with another 
dataset to organize and present that data by geographical region.
We believe (but have not carefully checked) that Our World in Data 
is relying on the [United Nations geoscheme](
https://unstats.un.org/unsd/methodology/m49/overview/
), saved here as `UNSD-Regions-M49.csv`.



