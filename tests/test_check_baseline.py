from functions.check_baseline import check_baseline, COLD_LIMIT_C, BASELINE_WARN_W


def test_prints_the_baseline_sample(capsys):
    check_baseline(25.0, 40.0, 1.5)
    out = capsys.readouterr().out
    assert "25.00 C plate" in out and "40.00 % heater" in out and "1.50 W" in out


def test_a_healthy_baseline_raises_no_warning(capsys):
    check_baseline(25.0, 40.0, 1.5)
    assert "WARNING" not in capsys.readouterr().out


def test_warns_in_the_ill_conditioned_cold_end(capsys):
    check_baseline(COLD_LIMIT_C - 1, 10.0, 0.0)
    assert "non-monotonic" in capsys.readouterr().out


def test_does_not_warn_just_above_the_cold_limit(capsys):
    check_baseline(COLD_LIMIT_C, 10.0, 0.0)
    assert "non-monotonic" not in capsys.readouterr().out


def test_warns_when_the_curve_looks_stale(capsys):
    check_baseline(25.0, 40.0, BASELINE_WARN_W + 0.1)
    assert "recalibrating" in capsys.readouterr().out


def test_the_stale_curve_warning_is_symmetric(capsys):
    check_baseline(25.0, 40.0, -(BASELINE_WARN_W + 0.1))
    assert "recalibrating" in capsys.readouterr().out


def test_both_warnings_can_fire_together(capsys):
    check_baseline(-45.0, 2.0, 25.0)
    out = capsys.readouterr().out
    assert out.count("WARNING") == 2
