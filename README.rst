Crochet CAD
===========

.. image:: https://landscape.io/github/judy2k/crochet-cad/master/landscape.png
   :target: https://landscape.io/github/judy2k/crochet-cad/master
   :alt: Code Health

A collection of utilities to aid in designing round crochet patterns, such as
Amigurumi. Currently this consists of a command-line script that will generate
text patterns for Spheres, Cones, or Donuts (Tori).

Crochet CAD is distributed under the GNU General Public License v3, see
COPYING.txt for more details.

Installation
------------

Crochet CAD requires a relatively recent `Python 3`_ installation (I test with
3.5.2). If you run Linux or OSX you almost certainly already have this
installed, otherwise install the latest Python 3 revision.

.. _`Python 3`: http://python.org/download/

Download crochet-cad from the download_ site and unzip it.

cd into the directory and run the following to install::

    python setup.py install

Running Crochet CAD
-------------------

The `crochet-cad` command provides access to all the pattern-generation
functionality. The command is called with a sub-command and a pattern is
printed to stdout as plain-text.

cd into the directory, and run::

    crochet-cad donut -i 18 -r 18
    
or::

    crochet-cad ball -r 18

or::

    crochet-cad cone -r 16 -c 60

To get more information about available options run::

    crochet-cad --help
    crochet-cad donut --help
    crochet-cad ball --help
    crochet-cad cone --help

------------------------------------------------------------------------------

Requests for new features and bug reports can be made using the github
issues_ tracker

.. _download: https://github.com/bedmondmark/crochet-cad/zipball/master
.. _issues: https://github.com/bedmondmark/crochet-cad/issues
