# Structuring flat data

Datasets are often available as flat CSV files and need some 
pre-processing to recover the tree structure needed for treemappping.
We provide some help for two ways of obtaining the tree structure 
(expressed in JSON), depending on whether each level of the 
hierarchy is represented by a separate column or the group structure 
is separate. 

## Columns as levels of hierarchy

Often each level of grouping is represented by a separate column.  
In this case we can think of the CSV file as a linearization of a 
tree, with each row representing a path from root to leaf.  We still 
need to identify the order of columns and which columns hold numeric 
data in the leaves of the tree, which we can do with a schema file 
in JSON like `restructure/data/beverage_schema.json` for
`restructure/data/beverages_by_meal.csv`  (a simple test case) or
`restructure/data/park_visit_schema.json` for the real dataset
`US-National-Parks_Recreation_Visits_1972-2023.csv` Note in both 
cases that columns are not necessarily ordered left to right from 
most general to most specific.  The order of column headers in the 
schema is taken as order general to specific. 

Utility program `csv_to_json.py` extracts a tree from a CSV file and 
a schema and 
produces a JSON representation.   

Sometimes it is useful to first 
summarize numeric data (aggregating rows that share some fields), 
which `aggregate.py` can do with the same schema.  Similar 
summarization can be accomplished with Python Panda aggregation 
functions, in SQL with SUM.  Excel can even produce subtotals, but 
in a manner unsuited to further processing.  SQL and Pandas provide 
more power and flexibility, but `aggregate.py` may be useful for 
simple scripted workflows with a minimum of programming. 

For example, we might first summarize the national park visit data 
by state, and then produce a JSON representation of that data for 
treemapping, with the following shell commands: 

```shell
cd restructure
python3 aggregate.py data/park_visit_schema.json data/US-National-Parks_RecreationVisits_1979-2023.csv visits.csv --by State
python3 csv_to_json.py data/park_visit_schema.json visits.csv data/visits.json
```

## Separate grouping information

Sometimes we have just a flat collection of data but we want to 
impose a hierarchical structure on it based on an external source of 
information.  For example, we might have just a list of university 
major codes and counts of students, even though we know that the 
majors are grouped into departments, schools, colleges, etc.  The 
hierarchical structure is known to us, but it is not reflected in 
the data set.   We want to reorganize that flat data set into a 
hierarchical (tree-structured) data set. 

It is not too hard to reorganize one flat data set manually, but it 
is both tedious and error-prone to repeat the same reorganization 
multiple times.  Therefore, we would rather automate the 
reorganization based on a _schema_ that can be reused.  That's what 
this sub-project attempts.

## The Schema

We parse a schema as a json file. The schema is the grouping 
structure we want to impose on the data, represented as a list of
dictionaries. For example, if we wanted to group eggs and milk as 
proteins, grains and root vegetables as starches, and further 
identify various foods as grains and root vegetables, we might 
take the following json structure as a schema: 

```python
{"protein":  ["milk", "eggs"]}, 
  {"starch": { "grain":  ["wheat", "buckwheet", "rye"], 
              "roots":  ["potato", "carrot", "turnip"] }}
```
Then, if our data set (in CSV form) is 
```text
potato,12
cabbage,2
eggs,3
carrot,4
```
We would produce a structure like 
```python
  { "starch": {
      "roots": {  "potato": 12,  "carrot": 4  }
    },
    "cabbage": 2,
    "protein": { "eggs": 3 }
}
```
Note: 
- the structured data is always a dictionary, which is printed
  as a text file in json format
-  the order of the produced structure reflects the data set 
   rather than the schema
- schema elements that are not represented in the data set are omitted
  from the structure.
- data elements that do not appear in the schema become roots of the 
  structured data forest

## Approach

For each leaf element of the schema, we construct an association of 
that leaf element to an _ancestry path_ from root to leaf.  This 
ancestry path guides insertion into the resulting structure. 

## Sample data sets

In addition to the example above (`sample-data.csv` and 
`sample-structure.json`), I have included `sample-major-counts.csv` 
based on Fall 2023 enrollment in CS 210 at U. Oregon, and 
`sample-majors-schema.json` based on the grouping of major codes at
that time.  