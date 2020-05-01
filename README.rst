cafplot
=======
Library to plot CAFAna_ objects in python/matplotlib.

``cafplot`` aims to provide a set of function to allow easy plotting of CAFAna
objects (Spectrum, Surface, etc.) with matplotlib library.


Why ``cafplot``?
================
So, why use ``cafplot`` for plotting instead of directly using CAFAna/ROOT
functions? Here are several reasons why you might be interested in ``cafplot``

- **Ease of Development**. Dynamic nature of the python typing system,
  versatile and mature standard library and rich python package ecosystem will
  make coding in python a light breeze compared to c++. Expect your python
  script be `2-3 times shorter`__ than the comparable c++ version.

- **Run Anywhere**. ``cafplot`` relies only on a few standard python packages
  for plotting. This allows you to run ``cafplot`` scripts on almost machine
  with minimal setup. Which is in stark contrast to CAFAna scripts, where
  you need to setup/compile NOvA-Art framework first.

- **Speed**. Yes, plotting with python/matplotlib is much **faster** than using
  CAFAna/ROOT. By the time it takes to compile your plotting CAFAna macro
  an analogous python script would have finished running.

- **Transferable Knowledge**. Unlike knowledge of the ROOT framework which is
  academia specific, knowledge of python/matplotlib stack is in demand in both
  academia and industry.

__ languages_


Installation
============
You can install ``cafplot`` either using ``pip`` or manually.

Using PyPI
----------
Simply run:

.. code-block:: bash

    $ pip install cafplot

Manual Installation
-------------------
1. Close the repository

.. code-block:: bash

    $ git clone https://github.com/usert5432/cafplot

2. Install ``cafplot``

.. code-block:: bash

    $ cd cafplot
    $ python setup.py install

Support for Reading ROOT Files
------------------------------
If you need support for reading ROOT files then ``uproot`` package is required
as well:

.. code-block:: bash

    $ pip install uproot


Getting Started
===============
Lets look at a simple example of plotting CAFAna Spectrum. ``cafplot`` itself
does not support creation of CAFAna Spectra from the caf files and it is meant
only for plotting. Correspondingly, the Spectrum must be filled and created
in CAFAna first.

For the purposes of this example, we will use CAFAna demo script
``CAFAna/tute/demo2p5a.C`` to create a spectrum. After running this demo
script we will get a ROOT file named ``save_your_spectra_to_disk.root`` with a
1D Spectrum ``dir_nhit_spectra``. Now, we will plot it using ``cafplot``.
First, we need to import a couple of packages:

.. code-block:: python

    import matplotlib.pyplot as plt

    from cafplot import load
    from cafplot.plot import *

Once imports are done, let's load the CAFAna Spectrum from a file
``save_your_spectra_to_disk.root`` (this will require ``uproot`` package
installed):

.. code-block:: python

    root_file = load("save_your_spectra_to_disk.root")
    spectrum  = root_file.get_spectrum("dir_nhit_spectra")

After this operation we will have CAFAna Spectrum loaded to ``spectrum``
variable. Similar to CAFAna, before plotting Spectrum we need to extract a
normalized histogram from it. Let's normalize it by POT to ``9e20``.

.. code-block:: python

    root_hist = spectrum.rhist(pot = 9e20)

Great, now we are ready to plot our first spectrum with ``cafplot``

.. code-block:: python

    f, ax = plt.subplots() # Create matplotlib Figure/Axes
    plot_rhist1d(ax, root_hist, 'NHit', histtype = "step", color = "red")
    plt.show() # show plot

You should see the plotted spectrum opened in a separate window.


Documentation
=============
Basic example of how to use ``cafplot`` is outlined in the `Getting Started`_
section. More complete examples of ``cafplot`` usage are provided in the
``examples/`` subdirectory. In particular, you might be interested in
``spectrum_plot.py`` -- complete example on how to plot CAFAna Spectrum
and ``surf_plot.py`` -- example of plotting CAFAna FrequentistSurface.

The further documentation please refer to python docstrings for each
``cafplot`` module.

Dependencies
------------
``cafplot`` is written with python version 3 in mind and won't work with python
version 2. It requires the following packages for the proper operation:

- ``numpy``
- ``matplotlib``
- ``scipy`` - at this moment ``cafplot`` uses only stats subpackage
  of ``scipy``.

Additionally, one may want to install ``uproot`` if support of reading
CAFAna objects from ROOT files is required.


Code Overview
-------------
``cafplot`` has several subpackages with different purposes:

- ``plot`` subpackage contains a collection of functions for plotting
  ``RHist``, ``Spectrum``, ``Surface`` objects.

- ``rfile`` subpackage contains functions and classes for loading CAFAna
  objects from different files (currently supports ROOT files and json files).

- ``rhist`` subpackage contains ``RHist`` class that approximates behavior
  of the ROOT histogram classes.

- ``spectrum`` subpackage defines ``Spectrum`` class to work with CAFAna
  Spectrum.

- ``stats`` subpackage for various statistical routines.

- ``surface`` subpackage contains ``Surface`` classes to work with CAFAna
  surfaces.

TODO
----

* Add support for plotting binned statistics
* Add support for plotting ROC curves


.. _CAFAna: https://cdcvs.fnal.gov/redmine/projects/novaart/wiki/CAFAna_overview
.. _languages: https://arxiv.org/abs/1409.0252

