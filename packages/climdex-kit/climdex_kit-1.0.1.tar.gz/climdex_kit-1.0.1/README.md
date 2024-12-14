![PyPI - Status](https://img.shields.io/pypi/status/climdex-kit)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/climdex-kit)
![PyPI](https://img.shields.io/pypi/v/climdex-kit)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/climdex-kit)
![PyPI - License](https://img.shields.io/pypi/l/climdex-kit)

# `climdex-kit`: compute, publish, analyse

* [Background](#background)
* [Content](#content)
* [Installation](#installation)
* [Usage](#usage)
* [Data Organization](#data-organization)
* [Logging](#logging)
* [Examples](#examples)

[![climdex-kit IO overview](docs/uml/climdex.io.overview.svg)](docs/uml/)

This project contains a Python package for the parallelized
local computation of [scenario](https://climatescenarios.org/primer/)-aware
climate indices starting from input time-series
of climate projections.

The package comes with an pre-compiled initial set of indices, mostly
relying on the [CDO](https://code.mpimet.mpg.de/projects/cdo) operators.
For the more advanced ones (SPI and SPEI), the [climate-indices](https://climate-indices.readthedocs.io)
Python package is used.
This set of indices can be easily customised or extended: please
check out [how to contribute](CONTRIBUTING.md) if you are interested.

The package is written in Python and for most of the implemented climate indices
relies on both the [CDO](https://code.mpimet.mpg.de/projects/cdo/wiki/Cdo#Documentation)
library, and the [climate-indices](https://github.com/monocongo/climate_indices) package.

## Background

A climate index is information derived from one or more climate variables
(precipitation, mean temperature, etc). The index can range from a simple
conditional counting of days against a threshold, to more complex
statistical processing.

The information is usually calculated spatially
on a pixel-by-pixel basis, with possibly some form of aggregation over time.
Hence the spatio-temporal domain of an index is generally a time-series
with the same spatial resolution, and with either the same or a coarser
temporal step.

The availability of robust and easily interpretable information about
the spatial distribution and temporal evolution of climate related-hazards,
especially climate extremes, is an increasing need not only for the
research community but also for a wide range of sectors and applications.

The European Environmental Agency has been currently supporting, in the
framework of the European Topic Centre on Climate Change impacts, vulnerability
and Adaptation (ETC-CCA), the review and selection of suitable climate-related
indices for Europe to be recommended and implemented for adaptation purposes.


## Content

The project is structured as follows:

* `src/` : source folder containing the Python package implementation
* `test/` : test suites
* `etc/` : folder with configuration files (most notably the **indices.ini**
           file with the definition of the climate indices
* `notebooks/` : folder with the Jupyter notebooks
* `docs/` : documentation folder
* `requirements.txt`/`environment.yml` : package dependencies for *pip*
   and *conda* environments
* `conda-lock.yml` : environment lock file
* `Makefile` : set of rules for building and installing the package
* `AUTHORS` : list of authors
* `CONTRIBUTING.md` : help for developers
* `CHANGELOG.md` : list of notable changes for each release of the project
* `README.md` : this file

The following files are required for packaging and distribution:

* `pyproject.toml` : tells what is required to build the project
* `setup.cfg`/`setup.py` : static/dynamic package metadata for **setuptools**


## Installation

The package is available as both *pip* sdist/wheel and *conda* package.

### Dependencies

The package relies on the
[CDO](https://code.mpimet.mpg.de/projects/cdo/wiki/Cdo#Installation-and-Supported-Platforms)
operators library v1.9.9. If you are using *conda* environments, you can install the package as follows:

```sh
conda install -c conda-forge cdo=1.9.9
```

In alternative, you can install the `climdex-kit` *conda* package as explained later in this file.

### Install from PyPI via pip

```sh
$ python3 -m pip install climdex-kit
```

### Install as conda package

```sh
TODO
```

### Install in development mode

For developers: refer to the instructions in the [CONTRIBUTING](CONTRIBUTING.md)
file for the setup of the development environment instead.

## Usage

The `climdex` Python package provides a set sub-commands for the specific actions to be taken

* `list`/`ls` : list all available indices
* `show`/`sh` : show the details of a specific index
* `mlut` : shows the lookup-table of the models that are used by the input ensembles
* `compute`/`co` : compute one or more indices
* `analyse`/`an` : analyses input indices ensembles to extract aggregated more readable data

There is thus a hierarchical organization of the CLI arguments.
At any level of the hierarchy, the `--help`/`-h` option can be called to print
the help message.

### general args

| <div style="width:30%">option</div> | <div style="width:60%">description</div> | allowed values |
|:------------------------------------|:-----------------------------------------|:--------------:|
| `--version`            | Get the version number of the program | |
| `--idx-conf`/`-c` FILE | Alternative indices configuration file (.ini) (default is ./etc/indices.ini) | abs/rel path |
| `--log-conf`/`-L` FILE | Alternative logging configuration file (.yaml) (default: ./etc/logging.yml)  | abs/rel path |
| `-d`                   | Enable debug mode | |

(See `$ python -m climdex -h` for a full synopsis)


### {list,ls} args

This sub-command currently does not provide any option.
Run `$ python -m climdex list` to get a summary of all available climate indices.


### {show,sh} args

| <div style="width:30%">option</div> | <div style="width:60%">description</div> | allowed values |
|:------------------------------------|:-----------------------------------------|:--------------:|
| `INDEX` | The index configuration to be visualized | see `{list,ls}` sub-command | 

(See `$ python -m climdex show -h` for a full synopsis)

### {mlut} args

No args to be provided for this action: the output will be a table of the mappings from
indices to model names that could be used for more handy filtering (`--model` instead of `--regex`) or e.g. used to encode 
models coordinates when loading ensembles as OGC grid coverages for rasdaman.

```
========== Climate Models LUT ====================
  #00 --> EUR-11_CNRM-CERFACS-CNRM-CM5_CLMcom-CCLM4-8-17_r1i1p1_v1
  #01 --> EUR-11_CNRM-CERFACS-CNRM-CM5_CLMcom-ETH-COSMO-crCLIM-v1-1_r1i1p1_v1
  #02 --> EUR-11_CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63_r1i1p1_v2
  #03 --> EUR-11_CNRM-CERFACS-CNRM-CM5_KNMI-RACMO22E_r1i1p1_v2
  ...
```

### {compute,co} args

| <div style="width:30%">option</div> | <div style="width:60%">description</div> | allowed values |
|:------------------------------------|:-----------------------------------------|:--------------:|
| `--index` / `-i` INDEX | A comma-separated list of indices to be computed | see `{list,ls}` sub-command | 
| `--multiprocessing` N  | The CPU parallelism to be employed | int>0 (N of CPUs) or one among {`one`, `all_but_one`, `all`} |
| `--idir` DIR           | Root folder where to look for input files (expected structure: *$input_dir/variable/scenario/\*.nc*) | abs/rel path |
| `--odir`/`-o` DIR      | Root folder where to store indices files | abs/rel path |
| `--scenario`/`-s` S    | White-space separated list of scenarios | sub-folders of input variables |
| `--regex`/`-x` R       | Filter input files with a regular expression | regex |
| `--metadata-only`/`-m` | Only re-set the output attributes (metadata) on existing indices files (compute the index file too on non-existing file instead) | |
| `--dry-run`/`-n`       | Only print jobs to output without doing anything | |
| `--force`/`-f`         | Force overwrite of existing output indices files (otherwise execution is stopped) | |

(See `$ python -m climdex compute -h` for a full synopsis)


### {analyse,an} args

Given the huge amount of options for the analysis sub-command, we will subdivide them
into three different categories.

Plotting utilities for analysis outputs can be found in the [`plots`](src/climdex/analyse/plots.py) module.

(See `$ python -m climdex analyse -h` for a full synopsis)

#### analysis I/O and execution

| <div style="width:30%">option</div> | <div style="width:60%">description</div> | allowed values |
|:------------------------------------|:-----------------------------------------|:--------------:|
| `--type`/`-t`         | The type of analysis | {`map`,`trend`/`trn`, `uncertainty`/`unc` } | 
| `--src-type` TYPE     | The type of the source of the input indices | {`local`, `openeo`, `wcps`} |
| `--src` SRC           | Source of the climate indices | either input folder or endpoint URL |
| `--odir`/`-o` DIR     | Output folder where to store analysis files | |
| `--oformat` FMT       | Format of the output analysis files | {`nc`, `png`, `json`, `geojson` } |
| `--multiprocessing` N | The CPU parallelism to be employed | int>0 (N of CPUs) or one among {`one`, `all_but_one`, `all`} |
| `--dry-run`/`-n`      | Only print jobs to output without doing anything | |
| `--force`/`-f`        | Force overwrite of existing output indices files (otherwise execution is stopped) | |
| `--lenient`/`-l`      | Silently accept empty outputs when input filters are not overlapping with input domain (otherwise exceptions are raised) | |

### input filtering

These arguments lets the user reduce the scope of the analysis, at different scales: from
the index future scenario, to intra-ensemble model selection, and also at the "pixel" level
within a single future projection.

#### dimensions trimming/clipping

"Image"-level scoping options.

| <div style="width:30%">option</div> | <div style="width:60%">description</div> | allowed values |
|:------------------------------------|:-----------------------------------------|:--------------:|
| `--index` / `-i` INDEX[,INDEX...] | A comma-separated list of indices to be analysed | see `{list,ls}` sub-command |
| `--scenario`/`-s` S [S ...]       | White-space separated list of future scenarios | |
| `--model`/`-m` M [M ...]          | White-space separated list of climate models | see `mlut` sub-command |
| `--bbox` xmin,ymin,xmax,ymax      | Input horizontal bounding-box | input native coordinates |
| `--wgs84-bbox` lat_min,lon_min,lat_max,lon_max | Input horizontal WGS84 bounding-box | latitude/longitude decimal degrees coordinates |
| `--clip` GEOM                     | Horizontal spatial clipping  | WKT geometry text or file containing WKT  |
| `--clip-id` I                     | When clip is a file, the indexing label to be used to describe each geometry in the analysis output files | |
| `--tint` [t0[,t1] ...]            | White-space separated list of input time interval(s) of analysis | timestep `t` or time interval `t0,t1` |
| `--baseline` t0,t1                | The baseline time interval | |

#### pixel-based filtering

"Pixel"-level/fine-grained filtering options.

| <div style="width:30%">option</div> | <div style="width:60%">description</div> | allowed values |
|:------------------------------------|:-----------------------------------------|:--------------:|
| `--hfilter` [h],[H]           | Pixel-level altitude filter (needs a `--dem`) | { `h,`, `h,H`, `,H` } |
| `--dem` FILE                  | The Digital Elevation Model to be used for `--hfilter` | DEM with same H-grid as input indices |
| `--significant` DIM [DIM ...] | Keep only statistically significant (Wilcoxon test) "pixels" with the given [core dimensions](https://tutorial.xarray.dev/advanced/apply_ufunc/core-dimensions.html) | |
| `--conf-level` L              | The confidence level to be used in the Wilcoxon test (`--significant`) (default is 95%) | [1-99] int |
| `--perc-pos` PERC             | Keep only the sections where PERC% of the values in the ensemle are >0 | [0-100] int |
| `--perc-neg` PERC             | Keep only the sections where PERC% of the values in the ensemle are <0 | [0-100] int 

### aggregation

Finally, these arguments let the user specify how many and which types of aggregation are
to be applied across the dimensions of the climate indices, which span the horizontal XY spatial axes,
time, the future scenarios, and models within the ensemble.

| <div style="width:30%">option</div> | <div style="width:60%">description</div> | allowed values |
|:------------------------------------|:-----------------------------------------|:--------------:|
|`--xyaggr` A [A ...] | Spatial (horizontal) aggregation  | {`avg`, `med`, `min`, `max`, `qX`, `pXX`, `range`, `perc_pos`, `perc_neg`} |
| `--taggr` A [A ...] | Temporal aggregation | {`avg`, `med`, `min`, `max`, `qX`, `pXX`, `range`, `perc_pos`, `perc_neg`} |
| `--eaggr` A [A ...] | Ensemble aggregation | {`avg`, `med`, `min`, `max`, `qX`, `pXX`, `range`, `perc_pos`, `perc_neg`}  |
| `--baseline-op` OP  | The operator used to compare target interval (`--tint`) with baseline (`--baseline`) | {`diff`, `perc_diff`, `ratio`} |


## Data organization

The package expects a fixed organization of the input datasets and a fixed naming scheme
in order to properly extract all the metadata.

The path and name of a climate projection NetCDF starting from the $IDIR input
root directory (`--idir` in the command line) shall be as follows:

```sh
$IDIR/{var}/{scenario}/{var}_{model}_{timeres}_{yearstart}{yearend}_{scenario}.nc
```

Being:

* `{var}` : the climate variable (whose label shall also coincide with the name of the
variable in the NetCDF)
* `{scenario}` : the name of the emissions scenario
* `{model}` : the name of the climate model used to create the projection
* `timeres` : the time-step of the time-series (e.g. day, month, etc)
* `yearstart` / `yearend` : time range of the time-series (`YYYY` format)

For ancillary scenario-independent datasets (e.g. land mask),
the `{scenario}/` sub-folder can be omitted mandatory, and the name
of the dataset shall be `{var}.nc`.

Analogously, given the $ODIR output specified via `--odir/-o` CLI argument, 
each index file will be stored then as follows:

```sh
$ODIR/{index}/{scenario}/{index}_{model}_{timeres}_{yearstart}{yearend}_{scenario}.nc
``` 

## Logging

By default the program logs to both console (with colored output to highlight warnings and errors),
and to a file called `climdex.log` in the current working directory.

The configuration of both loggers can be found in `./etc/logging.yaml`, otherwise use
the `--log-conf`/`-L` option to set an alternative configuration.


## Examples

Here some examples of command-line calls of the climdex-kit available commands:

```sh
# list all avaiable indices
$ python -m climdex list

# show the configuration details of the index [spei12]
$ python -m climdex show spei12

# show the model indexing used
$ python -m climdex mlut

# compute the frost days [fd] and 12-months SPI [spi12] index on all available climate
#   projections for scenario rcp85 and by using 3 CPUs
$ python -m climdex \ 
    compute \
    --index amt,spi12   \
    --multiprocessing 3 \
    --scenario rcp85    \
    --idir $IDIR        \
    --odir $ODIR

# update the metadata of all existing indexes of scenario rcp85, and compute the missing ones anew
#   using all CPUs + turn on debug mode + dry run only
$ python -m climdex -d \ 
    compute \
    --index all           \
    --scenario rcp85      \
    --multiprocessing all \
    --metadata-only       \
    --idir $IDIR          \
    --odir $ODIR          \
    --dry-run

# re-compute the [fd] and [tn] indices for the model "EUR-11_CNRM-CERFACS-CNRM-CM5_CLMcom-CCLM4-8-17_r1i1p1_v1"
#   and scenario rcp45 and keep it on a separate file for comparison with existing
#   + use 1 CPU (sequential execution)
$ python -m climdex \ 
    compute \
    --index fd,tn         \
    --scenario rcp45      \
    --multiprocessing one \
    --idir $IDIR          \
    --odir $ODIR          \
    --regex "*EUR-11_CNRM-CERFACS-CNRM-CM5_CLMcom-CCLM4-8-17_r1i1p1_v1*"
 
# re-compute (and overwrite when existing) all indexes on rcp45 and rcp85 scenarios
#   + using all available CPUs except one
$ python -m climdex \ 
    compute \
    --index all                   \
    --scenario rcp45 rcp85        \
    --multiprocessing all_but_one \
    --idir $IDIR                  \
    --odir $ODIR                  \
    --force

# extract the 2D maps of relative difference with respect to [1981,2010] baseline of the [rx5day] and [r95ptot]
#   indices over the time interval [2041,2070], averaging over time and pickling the ensemble median value,
#   and for both rcp45 and rcp85 scenarios
#  (input from locally available NetCDFs computed with climdex-compute)
$ python -m climdex \
    analyse -t map  \
    --index rx5day,r95ptot \
    --src-type local       \
    --src  $IDIR \
    --odir $ODIR \
    --oformat nc \
    --scenario rcp45 rcp85 \
    --tint     2041,2070 \
    --baseline 1981,2010 \
    --baseline-op "perc_diff" \
    --taggr avg \
    --eaggr med

# extract time profile of 5th, 50th, and 95th time percentiles of [su] and [tr] indices over the whole series
#   over averaged grid points below 700m of altitude and both rcp45 and rcp85 scenarios
#  (input from locally available NetCDFs computed with climdex-compute)
$ python -m climdex  \ 
    analyse -t trend \
    --index su,tr    \
    --src-type local \
    --src  $IDIR     \
    --odir $ODIR     \
    --oformat json   \
    --scenario rcp45 rcp85 \
    --hfilter ,700 \
    --dem $DEM_FILE\
    --xyaggr avg \
    --eaggr p05 med p95

# extract the five-number statistics (min, 5p, med, 95p, max) of [tx90p] and [tn90p] indices over the three 
#   different time intervals, with values relative to a [1981-2010] baseline
#   over averaged grid points for both rcp45 and rcp85 scenarios
#  (input from locally available NetCDFs computed with climdex-compute)
$ python -m climdex  \ 
    analyse -t trend \
    --index su,tr    \
    --src-type local \
    --src  $IDIR     \
    --odir $ODIR     \
    --oformat json   \
    --scenario rcp45 rcp85 \
    --tint     2011,2040  2041,2070  2071,2100 \
    --baseline 1981,2010 \
    --baseline-op "diff" \
    --taggr  avg \
    --xyaggr avg \
    --eaggr min p05 med p95 max

# extract the map of data range and percentage of agreement (positive direction) within the ensemble
#   of relative differences with respect to [1981-2010] baseline for the time period 2081-2100
#   for the [tr] index only over the grid points above the 1'000m of altitude, for the rcp45 scenario
#  (input from locally available NetCDFs computed with climdex-compute)
$ python -m climdex \
    analyse -t map  \
    --index tr      \
    --src-type local\
    --src  $IDIR \
    --odir $ODIR \
    --oformat nc \
    --scenario rcp45 \
    --tint     2081,2100 \
    --baseline 1981,2010 \
    --baseline-op "diff" \
    --taggr avg \
    --eaggr range perc_pos \
    --hfilter 1000, \
    --dem $DEM_FILE

# For each geometry in the regions.shp file (uniquely identified and to be serialized using "catasto_code" field), compute
#   five time-series of the ensemble i) minimum, ii) 1st quartile, iii) median, iv) 3rd quartile, and
#   v) maximum of the spatial averages for each timestep wihtin the 2071-2100 time period and
#   serialize it as a GeoJSON Feature Collection, for both rcp45 and rcp85 climate scenarios,
#   parallelizing the tasks across all available CPUs
$ python -m climdex \
    analyse -t trn  \
    --index hwd     \
    --src-type local  \
    --src  $IDIR      \
    --odir $ODIR      \
    --oformat geojson \
    --scenario rcp45 rcp85 \
    --tint 2071,2100 \
    --xyaggr avg \
    --eaggr  min q1 med q3 max \
    --clip regions.shp \
    --clip-id catasto_code \
    --multiprocessing all 
```

## Credits
This project is funded by the
 [FAct CLIMAX](https://www.eurac.edu/en/institutes-centers/center-for-climate-change-and-transformation/projects/fact-climax)
project at Eurac Research (Center for Climate Change and Transformation, Institute for Earth Observation).

[![eurac_logo](media/eurac_logo_small.png)](https://www.eurac.edu/en/institutes-centers/center-for-climate-change-and-transformation)

