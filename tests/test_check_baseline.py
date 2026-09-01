from functions.check_baseline import check_baseline, COLD_LIMIT_C, BASELINE_WARN_W, SPREAD_WARN_W


def test_prints_the_selected_zone(capsys):
    check_baseline(25.0, 1.5, 0.8)
    out = capsys.readouterr().out
    assert "25.00 C plate" in out and "1.50 W" in out and "spread 0.80 W" in out


def test_a_healthy_baseline_raises_no_warning(capsys):
    check_baseline(25.0, 1.5, 0.8)
    assert "WARNING" not in capsys.readouterr().out


def test_warns_in_the_ill_conditioned_cold_end(capsys):
    check_baseline(COLD_LIMIT_C - 1, 0.0, 0.0)
    assert "non-monotonic" in capsys.readouterr().out


def test_does_not_warn_just_above_the_cold_limit(capsys):
    check_baseline(COLD_LIMIT_C, 0.0, 0.0)
    assert "non-monotonic" not in capsys.readouterr().out


def test_warns_when_the_curve_looks_stale(capsys):
    check_baseline(25.0, BASELINE_WARN_W + 0.1, 0.0)
    assert "recalibrating" in capsys.readouterr().out


def test_the_stale_curve_warning_is_symmetric(capsys):
    check_baseline(25.0, -(BASELINE_WARN_W + 0.1), 0.0)
    assert "recalibrating" in capsys.readouterr().out


def test_warns_when_the_zone_missed_whole_noise_cycles(capsys):
    """A wide spread means the mean sits somewhere up the swing, not at its centre."""
    check_baseline(25.0, 0.0, SPREAD_WARN_W + 0.1)
    assert "Re-cut it over whole" in capsys.readouterr().out


def test_a_tight_zone_draws_no_spread_warning(capsys):
    check_baseline(25.0, 0.0, SPREAD_WARN_W)
    assert "Re-cut" not in capsys.readouterr().out


def test_every_warning_can_fire_at_once(capsys):
    check_baseline(-45.0, 25.0, 20.0)
    assert capsys.readouterr().out.count("WARNING") == 3
