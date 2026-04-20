import numpy as np
import pandas as pd

from backtest_analytics.failure_analysis import ic_crowding_trend
from backtest_analytics.performance_metrics import annualised_return, sharpe_confidence_interval
from backtest_analytics.signal_analysis import compute_ic_timeseries, compute_time_series_ic_decay
from backtest_analytics.transaction_costs import compute_breakeven_cost
from backtest_analytics.validation import purged_walk_forward_splits


def test_annualised_return_uses_compounding():
    daily_returns = pd.Series([0.10, 0.10], index=pd.date_range("2024-01-01", periods=2, freq="D"))
    result = annualised_return(daily_returns, trading_days=2)
    assert np.isclose(result, 0.21)


def test_compute_ic_timeseries_uses_next_realised_returns():
    dates = pd.date_range("2024-01-01", periods=4, freq="D")
    cols = list("ABCDE")
    signal = pd.DataFrame(
        [np.arange(1, 6), np.arange(1, 6), np.arange(1, 6), np.arange(1, 6)],
        index=dates,
        columns=cols,
    )
    realised_returns = pd.DataFrame(
        [
            np.zeros(5),
            np.arange(1, 6),
            np.arange(5, 0, -1),
            np.arange(1, 6),
        ],
        index=dates,
        columns=cols,
    )

    ic_ts = compute_ic_timeseries(signal, realised_returns, horizon=1)

    assert np.isclose(ic_ts.loc[dates[0]], 1.0)
    assert np.isclose(ic_ts.loc[dates[1]], -1.0)
    assert np.isclose(ic_ts.loc[dates[2]], 1.0)


def test_purged_walk_forward_splits_enforce_purge_and_embargo():
    index = pd.date_range("2024-01-01", periods=50, freq="B")
    folds = purged_walk_forward_splits(
        index=index,
        n_splits=3,
        test_size=5,
        purge_gap_days=2,
        embargo_gap_days=3,
        expanding=True,
    )

    assert len(folds) == 3
    for fold in folds:
        assert fold.train_end < fold.test_start - pd.Timedelta(days=2)

    for prev_fold, next_fold in zip(folds, folds[1:]):
        assert next_fold.test_start >= prev_fold.embargo_end


def test_compute_breakeven_cost_includes_risk_free_rate():
    rf_daily = 0.05 / 252
    turnover = 0.20
    target_cost_bps = 10.0
    gross_returns = pd.Series(
        [rf_daily + target_cost_bps / 1e4 * turnover] * 30,
        index=pd.date_range("2024-01-01", periods=30, freq="B"),
    )

    breakeven = compute_breakeven_cost(gross_returns, turnover, risk_free_annual=0.05, trading_days=252)
    assert np.isclose(breakeven, target_cost_bps)


def test_ic_crowding_trend_handles_short_series():
    ic_series = pd.Series(
        np.linspace(0.01, -0.01, 100),
        index=pd.date_range("2024-01-01", periods=100, freq="B"),
    )
    result = ic_crowding_trend(ic_series, recent_years=3, trading_days=252)
    assert "error" in result


def test_sharpe_confidence_interval_newey_west_is_finite():
    returns = pd.Series(
        [0.001, 0.002, -0.001, 0.0015, 0.0005, -0.0002] * 30,
        index=pd.date_range("2024-01-01", periods=180, freq="B"),
    )
    result = sharpe_confidence_interval(returns, method="newey_west")

    assert np.isfinite(result["sharpe"])
    assert np.isfinite(result["se"])


def test_compute_time_series_ic_decay_for_single_asset():
    dates = pd.date_range("2024-01-01", periods=12, freq="B")
    signal = pd.Series(np.arange(12, dtype=float), index=dates, name="signal")
    realised_returns = pd.Series(np.arange(12, dtype=float) / 100.0, index=dates, name="ret")

    decay = compute_time_series_ic_decay(signal, realised_returns, horizons=[1, 2], min_obs=5)

    assert list(decay.index) == [1, 2]
    assert np.isclose(decay.loc[1, "ic"], 1.0)
    assert np.isclose(decay.loc[2, "ic"], 1.0)
    assert decay.loc[1, "n_obs"] >= 5
