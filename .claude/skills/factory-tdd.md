# factory-tdd

## Test-First Development

1. Write the test file FIRST — one test per behavior
2. Each test follows: Arrange (setup) → Act (call) → Assert (verify)
3. Run the test — it MUST fail (if it passes, the test is wrong or the feature already exists)
4. Use pytest fixtures from conftest.py (app, client, authenticated_client, db_session)
5. Test naming: `test_<what>_<condition>_<expected>` (e.g., `test_login_valid_email_redirects_to_dashboard`)
6. Cover: happy path, validation errors, auth required, not found, edge cases

Do NOT proceed to assembly until all tests are written and failing for the right reasons.
