# factory-assembly

## Implementation

1. Pick one failing test
2. Write the MINIMAL code to make it pass — no extra features, no premature abstraction
3. Run the test — it must pass
4. Pick the next failing test, repeat
5. After all tests pass, run the full test suite: `pytest -v`
6. If any test breaks, fix before proceeding

Assembly is done when all tests from the TDD phase are green.
