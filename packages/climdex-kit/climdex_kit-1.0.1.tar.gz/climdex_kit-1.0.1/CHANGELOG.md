# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
...

## [1.0.1] - 2024-12-13
### Added
- add output formatting options for time coords and numeric decimal places of analyis values
- add `--clip-split` option to store clipped analysis in separate output files
- add `--clip-limit` argument to set a maximum number of geometries in clips
- allow multiple spatial aggregation in trends analysis

### Fixed
- fix installation of dependencies via `pip`
- runtime error on sub-pixel clipping geometries
- memory leak on analysis with multiple input time intervals

## [1.0.0] - 2024-10-02
### Added
- ANALYSE module: for extracting aggregated/filtered information from climate indices.
- Include `plots` set of utilities in ANALYSE for typical plots.
- Add codemeta.json, biblatex citation and AUTHORS files.
- Add SWHID to rasdaman template ingredients.
### Fixed
- Fix WCS dimensions order to follow CF conventions.
- Fix memory leak when combining baseline and target arrays during analysis.

## [0.1.2] - 2024-07-08
### Added
- Added CDO-based `[wsdi]`, `[cool_dd]`, `[grow_dd]`, and `[heat_dd]` indices.
- Fixed bug in `[hwd]` index.
- Add configuration of environment variables for CDO worker.
- Automatic assignment of indices by workers based on prefixes of the index configuration (eg. cdo.* -> CDO Worker).
- Add codemeta.json, biblatex citation and AUTHORS files.

## [0.1.1] - 2022-11-09
### Added
- Template recipes and import script for rasdaman.
- 6-months Winter/Summer precipitation indices.
- UML diagrams for developers.
- Minor fixes.

## [0.1.0] - 2022-01-25
### Added
- Implementation of the first set of indices with support of
  [CDO](https://code.mpimet.mpg.de/projects/cdo) and
  [climate-indices](https://climate-indices.readthedocs.io/en/latest/) libraries.
- `{compute}`, `{list}` and `{show}` sub-commands implementation.
- Virtual environment deps for both pip and conda systems.
- Packaging files for setuptools / pip.
- First Jupyter notebooks on plotting trends and comparison of indices.


[Unreleased]: https://gitlab.inf.unibz.it/earth_observation_public/cdr/climdex-kit/-/compare/v1.0.1...main
[1.0.1]: https://gitlab.inf.unibz.it/earth_observation_public/cdr/climdex-kit/-/releases/v1.0.1
[1.0.0]: https://gitlab.inf.unibz.it/earth_observation_public/cdr/climdex-kit/-/releases/v1.0.0
[0.1.2]: https://gitlab.inf.unibz.it/earth_observation_public/cdr/climdex-kit/-/releases/v0.1.2
[0.1.1]: https://gitlab.inf.unibz.it/earth_observation_public/cdr/climdex-kit/-/releases/v0.1.1
[0.1.0]: https://gitlab.inf.unibz.it/earth_observation_public/cdr/climdex-kit/-/releases/v0.1.0
