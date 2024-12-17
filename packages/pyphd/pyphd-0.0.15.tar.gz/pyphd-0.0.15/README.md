# pyphd


# Development

For development, I use a few GitHub actions to automate a few things. Here follows short description of each of these workflows:
- Reusable worflows
  * `test-install.yml`
    - test install on various Python versions (by default 3.10-3.12)
    - ruff linting checks (stop build if error occurs)
    - run unit tests with pytest
    - upload test results (for prosperity)
  * `build-package.yml`
    - build package for Python version 3.x
    - upload package dist artifacts (by name)
  * `github-release.yml`
    - download package dist artifact (by name)
    - sign package dist with Sigstore
    - create and upload GitHub release
  * `phdenzel/hatch-bump@v*`
    - use hatch to increment a version
    - commit and push changes
- Workflows with various triggers:
  * `on_branches.yml`
    - triggers on commit to any branch (except `main`) not in a PR (pull request)
    - runs `test-install-python-version` and `build-package`
  * `on_pr.yml`
    - triggers on commit to a PR
    - runs `test-install-python-version`, `build-package`, `publish-to-testpypi`, and `version-bump-dev`
  * `on_merge.yml`
    - triggers on PR merge
    - runs `version-bump-on-merge` (increments micro version on main)
  * `on_push.yml`
    - triggers on push to the main branch upon version change
    - runs `test-install`, `build-package`, `publish-to-pypi`
