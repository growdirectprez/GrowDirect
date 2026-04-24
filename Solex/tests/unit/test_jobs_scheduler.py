from unittest.mock import MagicMock, patch


def test_schedule_recurring_jobs_registers_both(monkeypatch):
    mock_sched = MagicMock()
    mock_sched.get_jobs.return_value = []
    fake_job = MagicMock(id="solex:test")
    mock_sched.cron.return_value = fake_job

    with patch("solex.jobs.scheduler.build", return_value=mock_sched):
        from solex.jobs.scheduler import schedule_recurring_jobs
        ids = schedule_recurring_jobs()

    assert mock_sched.cron.call_count == 2
    call_ids = [call.kwargs.get("id") for call in mock_sched.cron.call_args_list]
    assert "solex:charge_due_subscriptions" in call_ids
    assert "solex:abandonment_sweep" in call_ids


def test_schedule_recurring_jobs_cancels_existing(monkeypatch):
    existing_1 = MagicMock(); existing_1.id = "solex:charge_due_subscriptions"
    existing_2 = MagicMock(); existing_2.id = "solex:other-unrelated"
    mock_sched = MagicMock()
    mock_sched.get_jobs.return_value = [existing_1, existing_2]
    mock_sched.cron.return_value = MagicMock(id="new")

    with patch("solex.jobs.scheduler.build", return_value=mock_sched):
        from solex.jobs.scheduler import schedule_recurring_jobs
        schedule_recurring_jobs()

    # existing_1 should be cancelled (matches our ID); existing_2 left alone
    mock_sched.cancel.assert_any_call(existing_1)
    calls = [c.args[0] for c in mock_sched.cancel.call_args_list]
    assert existing_2 not in calls
