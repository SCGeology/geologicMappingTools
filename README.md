# SCGS Geologic Mapping Tools

Repository for various python scripts used for SCGS geologic mapping tasks. 

### thin_geol_points
#### Helps the geologist thin out geologic observations for displaying on 1:24,000 scale map. 

- The user creates a fishnet grid with a certain size, and then tool selects a single point from each 'cell' in the grid for display.
- A new field is created called "show_hide" that is populated with 1 or 0 to indicate which points to query for a 'thinned' display.
- This particular version of the tool lets the geologist choose a field that indicates how many geologic measurements were made at each point. The tool then prioritizes points in a cell that have a greater number of measurements. 

This is useful because geologists may have a dense set of measurements that cannot possibly be displayed on 1:24,000 map. The tool can be run with fishnet grids of different sizes to achieve the desired density of points for display. 
Since it only adds a field for querying to display, other manual filtering is still availabe. 

### mapUnitsPoints
#### Gets map unit from geologic polygons and puts them into the point data. 

This is necessary for the GeMS data model for geologic map data. 

### Glossary
#### Generates a list of terms from the GeMS database that are in fields that require a definition in the glossary table. 

The tool adds the terms to the glossary table (if they aren't already there) and gives the source of term so you can verify that it needs to be defined. 
