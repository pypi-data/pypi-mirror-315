.. _plot_reference:

Plot Class Reference
==================

.. currentmodule:: triggercalib.objects

The Plot class provides plotting utilities for trigger efficiencies and intermediate results.

Class Documentation
-----------------

.. autoclass:: Plot
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Plot Parameters
-------------

The Plot class accepts several parameters through the ``plot_kwargs`` dictionary:

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Parameter
     - Default
     - Description
   * - aspect
     - (12, 9)
     - Figure dimensions in inches (width, height)
   * - xlabel
     - observable name
     - Label for x-axis
   * - ylabel
     - "Candidates per bin"
     - Label for y-axis
   * - ylog
     - True
     - Use logarithmic y-axis scale
   * - title
     - ""
     - Plot title
   * - units
     - ""
     - Units for axis labels
   * - pulls
     - True
     - Whether to show pulls plot below main plot. If False, only the main plot is shown.
   * - xlims
     - data range
     - X-axis limits (min, max)
   * - bins
     - 100
     - Number of bins for histogram

Examples
--------

Basic usage with default parameters::

    plot = Plot(
        name="mass_fit",
        observable=mass_obs,
        data=dataset,
        pdf=total_pdf
    )
    plot.save("plots/")

Customizing the plot appearance::

    plot = Plot(
        name="mass_fit",
        observable=mass_obs,
        data=dataset,
        pdf=total_pdf,
        plot_kwargs={
            "ylog": True,
            "pulls": False,  # Hide pulls plot
            "xlabel": "m(B⁰) [MeV/c²]",
            "ylabel": "Candidates / (%.1f MeV/c²)",
            "units": "MeV/c²"
        }
    )
