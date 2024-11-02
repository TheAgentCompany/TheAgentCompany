Your task is to migrate the Sotopia (on GitLab) repository's dependency management system from poetry (https://python-poetry.org/) to UV (https://github.com/astral-sh/uv).

This involves:
1. Updating all GitHub workflow files to use UV instead of poetry for dependency management
2. Updating documentation files to reflect the change in package manager
3. Ensuring all commands and instructions are updated to use UV syntax

The migration should maintain all existing functionality while taking advantage of UV's improved performance.