.. _sideband_reference:

Sideband Class Reference
====================

.. currentmodule:: triggercalib.objects

The Sideband class provides functionality for defining and applying sideband regions in trigger efficiency calculations.

Class Documentation
-----------------

.. autoclass:: Sideband
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

Examples
--------

Basic usage with default parameters::

    sideband = Sideband(
        signal_range=(5200, 5350),     # Signal region in MeV/c²
        sideband_range=(5400, 5800),   # Sideband region in MeV/c²
        scale=1.0                      # Optional scaling factor
    )
    
    # Apply cuts
    signal_data = sideband.signal_cut(data)
    sideband_data = sideband.sideband_cut(data)
