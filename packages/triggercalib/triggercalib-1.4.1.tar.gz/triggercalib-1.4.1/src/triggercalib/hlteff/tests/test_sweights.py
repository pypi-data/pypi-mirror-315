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

import ROOT as R

R.gROOT.SetBatch(True)

HAS_ZFIT = True
try:
    import zfit
except ModuleNotFoundError:
    HAS_ZFIT = False

if HAS_ZFIT:
    from .utils import example_file, zfit_model, check_result
else:
    from .utils import example_file, check_result


def test_sweights_roofit(example_file):
    from triggercalib import HltEff

    tree, path = example_file

    ws = R.RooWorkspace("ws")
    obs = ws.factory("discrim[4800, 5600]")
    ws.factory(
        "BreitWigner::signal_pdf(discrim, signal_mean[5200, 5175, 5225], signal_width[8, 4, 24])"
    )
    ws.factory(
        "Exponential::combinatorial_pdf(discrim, combinatorial_exponent[-0.001, -0.01, 0])"
    )
    pdf = ws.factory(
        "SUM::pdf(signal_yield[10000, 0, 100000]*signal_pdf, combinatorial_yield[1000, 0, 100000]*combinatorial_pdf)"
    )

    hlteff = HltEff(
        "test_sweights_roofit",
        tis="Hlt1DummyOne",
        tos="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        observable=obs,
        pdf=pdf,
        output_path="results/sweights_roofit/",
        sweights="signal_yield",
        threads=1,
        verbose=True,
    )
    hlteff.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [3, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff.counts("sweights_roofit")
    hlteff.efficiencies("sweights_roofit")
    hlteff.write("results/output_test_sweights_roofit.root")

    hist = hlteff.get_eff("sweights_roofit_trig_total_efficiency_observ1")
    val = hist.GetPointY(0)
    err_low = hist.GetErrorYlow(0)
    err_high = hist.GetErrorYhigh(0)

    result_okay, (true, lower, upper) = check_result(
        val,
        (err_low, err_high),
        sample=f"{path}:{tree}",
        cut="discrim > 5100 && discrim < 5300 && observ1 > 0 && observ1 < 8",
    )
    if not result_okay:
        print(f"Computed efficiency out of bounds: {true} not in ({lower}-{upper})")
        raise RuntimeError


if HAS_ZFIT:

    def test_sweights_zfit(example_file, zfit_model):
        from triggercalib import HltEff

        tree, path = example_file
        obs, pdf = zfit_model

        hlteff = HltEff(
            "test_sweights_zfit",
            tis="Hlt1DummyOne",
            tos="Hlt1DummyOne",
            particle="P",
            path=f"{path}:{tree}",
            lazy=True,
            observable=obs,
            pdf=pdf,
            output_path="results/sweights_zfit/",
            sweights="signal_yield",
            threads=1,
            expert_mode=True,
            verbose=True,
            plot_kwargs={
                "ylog": True,
                "pulls": True,
            },
        )
        hlteff.set_binning(
            {"observ1": {"label": "Observable 1", "bins": [3, 0, 8]}},
            compute_bins=True,
            bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
        )
        hlteff.counts("sweights_zfit")
        hlteff.efficiencies("sweights_zfit")
        hlteff.write("results/output_test_sweights_zfit.root")

        hist = hlteff.get_eff("sweights_zfit_trig_total_efficiency_observ1")
        val = hist.GetPointY(0)
        err_low = hist.GetErrorYlow(0)
        err_high = hist.GetErrorYhigh(0)

        result_okay, (true, lower, upper) = check_result(
            val,
            (err_low, err_high),
            sample=f"{path}:{tree}",
            cut="discrim > 5100 && discrim < 5300 && observ1 > 0 && observ1 < 8",
        )
        if not result_okay:
            print(f"Computed efficiency out of bounds: {true} not in ({lower}-{upper})")
            raise RuntimeError
