# Detailed documentation of the SOFIA Lattice Statistics program

## Purpose

This program computes statistics on a lattice generated by SOFIA:

* Number of formal concepts
* Number of edges
* Depth of the lattice

## Execution

This program can be executed with:

```bash
python latticeStatistics.py lattice.json statistics.json
```

with:

* _lattice.json_: lattice generated by SOFIA
* _statistics.json_: Name of the file where the statistics of the lattice will be stored
