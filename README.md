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

You should also use a sparql endpoint as data source as there is no reason in importing the data multiple times.

## Functionality

The script splits the list of resources in the `restriction_file` in `numberOfThreads` equal parts and creates a jekyll setup for each thread.
The jekyll setups are executed in parallel and build to their individual destination rectories.
The resulting destination directories are collected (merged) into the specified `destinationPath` directory.
The result in `destinationPath` should be equal to what a single threaded jekyll execution produces in `_site`.

This method has some overhead as it executes multiple complete jekyll processes in parallel.
This includes that all non-resource pages are built multiple times.

This script helps to speed up build processes with many resource pages.

## License

MIT License

Copyright (c) 2019 AKSW Research Group @ University of Leipzig

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
