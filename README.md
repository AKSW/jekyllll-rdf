# Jekyllll RDF

*Parallelizer for Jekyll RDF*

TODO:
* Port this to Ruby ;-)
* Kill Child processes if this script is terminated.

## Usage

Start with:

```
./jekyllll-rdf.py <numberOfThreads> <destinationPath> <configFile>
```

e.g.

```
./jekyllll-rdf.py 4 _multisite _config.yml
```

The configuration needs to make use of the `restriction_file` feature of jekyll RDF.


## Functionality

The script splits the list of resources in the `restriction_file` in `numberOfThreads` equal parts and creates a jekyll setup for each thread.
The jekyll setups are executed in parallel and build to their individual destination rectories.
The resultings destination directories are collected (merged) into the specified `destinationPath` directory.
The result in `destinationPath` should be equal to what a single threaded jekyll execution produces in `_site`.

This method has some overhead as it executes multiple complete jekyll processes in parallel.
This includes that all non-resource pages are built multiple times.

Theis script helps to speed up builts with many resource pages.
