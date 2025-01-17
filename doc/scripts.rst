**************
PypeIt scripts
**************

PypeIt is packaged with several scripts that should have
been installed directly into your path (e.g. ~/anaconda/bin).

Pipeline Scripts
++++++++++++++++


pypeit_chk_for_calibs
=====================

This script, which is similar to :ref:`pypeit-setup`, examines a set
of files for an input spectrograph and scans for the standard calibrations.
It raises warnings when these are not found.

The script usage can be displayed by calling the script with the
``-h`` option:

.. include:: help/pypeit_chk_for_calibs.rst

And a typical call::

    pypeit_chk_calibs /PypeIt-development-suite/RAW_DATA/not_alfosc/grism4/ALDc2 -s not_alfosc

After a running stream of detailed notes, it prints a table of results
to the screen::

    setups pass     scifiles
    ------ -------- ---------------
         A False ALDc200205.fits
      None True


.. _pypeit-setup:

pypeit_setup
============

This setups files for data reduction.  See :doc:`setup` for details

run_pypeit
==========

This is the main executable for PypeIt.  See :doc:`running` for details.

pypeit_view_fits
================

This is a wrapper to the Ginga image viewer.  It is a bit of a kludge
in that it writes a dummy tmp.fits file to the harddrive and sends
that into Ginga.  The dummy file is deleted afterwards.

The script usage can be displayed by calling the script with the
``-h`` option:

.. include:: help/pypeit_view_fits.rst


Data Processing Scripts
+++++++++++++++++++++++

pypeit_coadd_1dspec
===================

See :doc:`coadd1d` for further details.

pypeit_collate_1d
=================

This is a tool to help organize spectra in multiple spec1d files, group them
by source, and flux/coadd them.

The script usage can be displayed by calling the script with the
``-h`` option:

.. include:: help/pypeit_collate_1d.rst

Calibration Scripts
+++++++++++++++++++

pypeit_arcid_plot
=================

Generate a PDF plot from a MasterFrame_WaveCalib.json file.
This may be useful to ID lines in other data.

The script usage can be displayed by calling the script with the
``-h`` option:

.. include:: help/pypeit_arcid_plot.rst


pypeit_lowrdx_pixflat
=====================

Convert a LowRedux pixel flat into a PypeIt ready file.

The script usage can be displayed by calling the script with the
``-h`` option:

.. include:: help/pypeit_lowrdx_pixflat.rst

pypeit_chk_edges
================

Inspect the slit/order edges identified by PypeIt in a RC Ginga
window.

The script usage can be displayed by calling the script with the
``-h`` option:

.. include:: help/pypeit_chk_edges.rst


pypeit_chk_flats
================

Inspect the flat field images produced by PypeIt in a RC Ginga
window.  This includes the stacked 'raw' image, the pixel flat,
the illumination flat, and the flat model.

The script usage can be displayed by calling the script with the
``-h`` option:

.. include:: help/pypeit_chk_flats.rst

.. _pypeit_chk_2dslits:

pypeit_chk_2dslits
==================

This script prints a simple summary of the state of the reduction
for all of the slits in a given :doc:`out_spec2D` file.  
Here is a standard call::

    pypeit_chk_2dslits spec2d_d0315_45929-agsmsk_DEIMOS_2018Mar15T124523.587.fits 

And the output to screen will look like:

.. code-block:: bash

    ================ DET 04 ======================
    SpatID  MaskID  Flags
    0021    958445    None
    0073    958470    None
    0143    958434    None
    0212    958458    None
    0278    958410    None
    0479    958400    None
    1257    958466    None
    1352    958392    BOXSLIT
    1413    958396    None
    1492    958403    None
    1568    958457    None
    1640    958405    None
    1725    958435    None
    1818    958422    None
    1880    958390    BOXSLIT
    1984    958393    BOXSLIT

The MaskID will be populated only if the instrument includes
mask design (e.g. Keck/DEIMOS).  The Flags column describes
failure modes or reasons why the slit was not reduced.
*None* is the preferred state for a science slit.


pypeit_flux_setup
=================

This sets up files for fluxing, coadding and telluric corrections.
Note the pypeit files generated by this scripts need your changes:

    - Give sensfunc file name in the fluxing pypeit file
    - Give sensfunc file name in the coadding pypeit file
    - The coadding pypeit file includes all objects extracted from
      your main reduction, so you need to pick up the one you are
      interested in and remove all others in the coadding pypeit file
      (between coadd1d read and coadd1d end)

See :doc:`fluxing`, :doc:`coadd1d`, and :doc:`telluric` for details.

The script usage can be displayed by calling the script with the
``-h`` option:

.. include:: help/pypeit_flux_setup.rst

