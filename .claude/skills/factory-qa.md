# factory-qa

## Quality Assurance

1. **Security:** No SQL injection, no XSS, CSRF tokens on all forms, @login_required on protected routes
2. **Code quality:** No dead code, no commented-out code, no TODO without a Linear issue
3. **Standards compliance:** Models use Mapped[], UUIDs, timestamps. Config from env. No hardcoded secrets.
4. **CSS compliance:** Templates use component classes from <appname>.css, no raw utility soup
5. **Test coverage:** Every route has at least one happy-path and one error-path test
6. **Davis-Stirling (Cove only):** Secret ballot separation, quorum rules, notice requirements

Fix any issues found before proceeding to ship.
