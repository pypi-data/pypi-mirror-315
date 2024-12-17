###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

import numpy as np
import ROOT as R
import uproot

from array import array
from ctypes import c_double
import json
from typing import List, Union
import yaml

HAS_ZFIT = True
try:
    import zfit
except ModuleNotFoundError:
    HAS_ZFIT = False


def bins_from_taxis(axis, as_array=False):
    """Extract bin edges from a ROOT TAxis object

    Args:
        axis: ROOT TAxis object to extract bins from
        as_array: Whether to return bins as a ROOT array

    Returns:
        list or array: List of bin edges or ROOT array of bin edges
    """
    bins = [axis.GetBinLowEdge(0)] + [
        axis.GetBinUpEdge(i) for i in range(1, axis.GetNbins() + 1)
    ]

    if as_array:
        return array("d", bins)
    return bins


def load_config(path: str):
    """
    Load a configuration file from a JSON or YAML file

    Args:
        path: Path to the configuration file

    Returns:
        dict: Configuration as a dictionary

    Raises:
        ValueError: If the file is not a '.json' or '.yaml' file
    """

    if path.endswith(".json"):
        with open(path, "r") as config_file:
            config = json.load(config_file)
    elif path.endswith(".yaml"):
        with open(path, "r") as config_file:
            config = yaml.safe_load(config_file)
    else:
        raise ValueError(f"Config '{path}' must be a '.json' or '.yaml' file")
    return config


def split_paths(paths: Union[List[str], str], require_same_tree: bool = True):
    """Split ROOT file paths into tree names and file paths

    Args:
        paths: Path(s) to ROOT file(s) of the form <path>:<tree>
        require_same_tree: Whether all paths must reference the same tree

    Returns:
        tuple: Tree name(s) and file path(s)

    Raises:
        ValueError: If require_same_tree is True and different trees are provided
    """
    if isinstance(paths, str):
        paths = [paths]
    split_trees, split_paths = zip(*(reversed(p.rsplit(":", 1)) for p in paths))

    if len(set(split_trees)) == 1 and require_same_tree:
        return split_trees[0], split_paths
    elif not require_same_tree:
        return split_trees, split_paths

    raise ValueError(
        f"Same tree must be provided for all paths. Trees '{split_trees}' were provided."
    )


def tgraph_to_th(graph, name="", title=""):
    """Convert a ROOT TGraph(2D)AsymmErrors to a TH1(2)D

    Args:
        graph: ROOT TGraph(2D)AsymmErrors to convert
        name: Optional name for output histogram
        title: Optional title for output histogram

    Returns:
        TH1D or TH2D: Histogram containing graph points with symmetric errors
    """
    if not name:
        name = graph.GetName()

    if not title:
        title = graph.GetTitle()

    x = c_double(0)
    y = c_double(0)

    xbins = bins_from_taxis(graph.GetXaxis(), as_array=True)

    if isinstance(graph, R.TGraphAsymmErrors):
        hist = R.TH1D(name, title, len(xbins) - 1, xbins)
        for point in range(graph.GetN()):
            graph.GetPoint(point, x, y)
            _bin = hist.FindBin(x)
            hist.SetBinContent(_bin, y)
            hist.SetBinError(_bin, graph.GetErrorY(point))

    elif isinstance(graph, R.TGraph2DAsymmErrors):
        z = c_double(0)

        ybins = bins_from_taxis(graph.GetYaxis(), as_array=True)

        hist = R.TH2D(
            name,
            title,
            len(xbins) - 1,
            xbins,
            len(ybins) - 1,
            ybins,
        )
        for point in range(graph.GetN()):
            graph.GetPoint(point, x, y, z)
            _bin = hist.FindBin(x, y)
            hist.SetBinContent(_bin, z)
            hist.SetBinError(_bin, graph.GetErrorZ(point))
    else:
        raise TypeError(f"Object '{name}' of unrecognised type '{type(graph)}'")

    return hist


def tgraph_to_np(tgraph):
    graph = uproot.from_pyroot(tgraph)
    xvals, yvals = graph.values()
    xlow_errs, ylow_errs = graph.errors("low")
    xhigh_errs, yhigh_errs = graph.errors("high")

    return xvals, yvals, (xlow_errs, xhigh_errs), (ylow_errs, yhigh_errs)


def th_to_np(th):
    histogram = uproot.from_pyroot(th)
    yvals, edges = histogram.to_numpy()
    xerrs = np.diff(edges)
    xvals = edges[:-1] + xerrs
    yerrs = histogram.errors()

    return xvals, yvals, xerrs, yerrs


if HAS_ZFIT:

    def create_zfit_dataset(data, observable, extra_observables=[]):
        """Create a zfit dataset from numpy data

        Args:
            data: Dictionary of numpy arrays
            observable: zfit Space object defining the observable
            extra_observables: List of additional observables to include

        Returns:
            zfit.Data: Dataset for zfit operations
        """
        spaces = [observable]
        if extra_observables:
            for extra_observable in extra_observables:
                if extra_observable not in spaces and not any(
                    extra_observable == o.obs[0] for o in spaces
                ):
                    if isinstance(extra_observable, str):
                        space = zfit.Space(
                            extra_observable,
                            limits=(
                                np.min(data[extra_observable]),
                                np.max(data[extra_observable]),
                            ),
                        )
                        spaces.append(space)

        spaces = [observable]
        if extra_observables:
            for extra_observable in extra_observables:
                if extra_observable not in spaces and not any(
                    extra_observable == o.obs[0] for o in spaces
                ):
                    if isinstance(extra_observable, str):
                        space = zfit.Space(
                            extra_observable,
                            limits=(
                                np.min(data[extra_observable]),
                                np.max(data[extra_observable]),
                            ),
                        )
                        spaces.append(space)

                    elif isinstance(extra_observables, zfit.Space):
                        spaces.append(extra_observables)

        obs = zfit.dimension.combine_spaces(*spaces)

        np_dataset = np.array(list(data.values())).T
        return zfit.Data.from_numpy(obs=obs, array=np_dataset)

    def zfit_fit(nll):
        """Perform a fit using zfit

        Args:
            nll: Negative log-likelihood to minimize

        Returns:
            tuple: Fit result and convergence status
        """
        minimizer = zfit.minimize.Minuit()
        fit_result = minimizer.minimize(nll)
        fit_result.hesse()
        criterion = minimizer.create_criterion(fit_result.loss, fit_result.params)
        converged = criterion.converged(fit_result)

        return fit_result, converged


def fit_result_to_string(fit_result):
    if isinstance(fit_result, R.RooFitResult):
        result_string = f"Fit performed with RooFit from ROOT {R.__version__}\n"
        result_string += "\nInitial parameters:\n"
        for var in fit_result.floatParsInit():
            result_string += f"{var.GetName()}: {var.getVal()} +/- {var.getError()}\n"
        result_string += "\nFinal parameters:\n"
        for var in fit_result.floatParsFinal():
            result_string += f"{var.GetName()}: {var.getVal()} +/- {var.getError()}\n"

        if len(fit_result.constPars()) > 0:
            result_string += "\nConstant parameters:\n"
            for var in fit_result.constPars():
                result_string += f"{var.GetName()}: {var.getVal()}\n"
        result_string += f"\nCovariance quality: {fit_result.covQual()}\n"
        result_string += f"Fit status: {fit_result.status()}\n"
        result_string += f"Minimum value: {fit_result.minNll()}\n"

        return result_string

    elif HAS_ZFIT and isinstance(fit_result, zfit.minimizers.fitresult.FitResult):
        result_string = f"Fit performed with zfit {zfit.__version__}"
        result_string += "\nFinal parameters:\n"
        for param, param_info in fit_result.params.items():
            result_string += f"{param.name}: {param_info['value']} +/- {param_info['hesse']['error']}\n"
        result_string += f"\nValid: {fit_result.valid}\n"
        result_string += f"Converged: {fit_result.converged}\n"
        result_string += f"Fit status: {fit_result.status}\n"
        result_string += f"Minimum value: {fit_result.fmin}\n"

        return result_string

    raise TypeError(
        f"Unrecognised type '{type(fit_result)}' for 'fit_result'. 'fit_result' must be of type 'ROOT.RooFitResult' or 'zfit.minimizers.fitresult.FitResult'."
    )


def write_fit_result(fit_result, path, verbose=False):

    result_string = fit_result_to_string(fit_result)
    if verbose:
        print(result_string)

    with open(path, "w") as result_file:
        result_file.write(result_string)

    if verbose:
        print(result_string)

    return
