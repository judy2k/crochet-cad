Crochet CAD
===========

A collection of utilities to aid in designing round crochet patterns, such as
Amigurumi. Currently this consists of a command-line script that will generate
text patterns for Spheres or Donuts (Tori).

Crochet CAD is distributed under the GNU General Public License v3, see
COPYING.txt for more details.

Installation
------------

Crochet CAD requires a relatively recent `Python 2`_ installation (I test with
2.5+). If you run Linux or OSX you almost certainly already have this
installed, otherwise install the latest Python 2 revision.

.. _`Python 2`: http://python.org/download/

Currently there's no setup script or installer, so just download_ the latest
revision and unzip it.

Running Crochet CAD
-------------------

The `crochet-cad` command provides access to all the pattern-generation
functionality. The command is called with a sub-command and a pattern is
printed to stdout as plain-text.

cd into the directory, and run::

    crochet-cad donut -i 18 -r 18
    
or::

    crochet-cad ball -r 18

To get more information about available options run::

    crochet-cad --help
    crochet-cad donut --help
    crochet-cad ball --help

------------------------------------------------------------------------------

Requests for new features and bug reports can be made using the github
issues_ tracker

.. _download: https://github.com/bedmondmark/Crochet-Cad/zipball/master
.. _issues: https://github.com/bedmondmark/Crochet-Cad/issues