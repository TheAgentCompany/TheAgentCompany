# Contributing

Thanks for your interest in contributing to The Agent Company! We welcome and appreciate contributions.
To report bugs, create a [GitHub issue](https://github.com/neulab/TheAgentCompany/issues/new).

If want to know how to edit code on serer side or task image, please echeck [DEVELOPMENT.md](./DEVELOPMENT.md)

## Contribution Guide
### For the member of our internal team
If you already have the access to this repository and can create branch on main repository. Git clone it, create your branch and open pull request for it.

### For community contributor

#### 1. Fork the Official Repository

Fork [The Agent Company repository](https://https://github.com/neulab/TheAgentCompany) into your own account.
Clone your own forked repository into your local environment.

```shell
git clone git@github.com:<YOUR-USERNAME>/TheAgentCompany.git
```

#### 2. Configure Git

Set the official repository as your [upstream](https://www.atlassian.com/git/tutorials/git-forks-and-upstreams) to synchronize with the latest update in the official repository.
Add the original repository as upstream

```shell
cd TheAgentCompany
git remote add upstream git@github.com:neulab/TheAgentCompany.git
```

Verify that the remote is set.
```shell
git remote -v
```
You should see both `origin` and `upstream` in the output.

#### 3. Synchronize with Official Repository
Synchronize latest commit with offical repository before coding.

```shell
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

#### 4. Create a New Branch And Open a Pull Request
After you finish implementation, open forked repository. The source branch is your new branch, and the target branch is `neulab/TheAgentCompany` `main` branch. Then PR should appears in [TheAgentCompany PRs](https://github.com/neulab/TheAgentCompany/pulls).

Then The Agent Company team will review your code.

## PR Rules

### 1. Pull Request title

As described in [here](https://github.com/commitizen/conventional-commit-types/blob/master/index.json), a valid PR title should begin with one of the following prefixes:

- `feat`: A new feature
- `fix`: A bug fix
- `doc`: Documentation only changes
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `style`: A refactoring that improves code style
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `ci`: Changes to CI configuration files and scripts (example scopes: `.github`, `ci` (Buildkite))
- `chore`: Other changes that don't modify src or test files
- `revert`: Reverts a previous commit

For example, a PR title could be:
- `refactor: modify package path`
- `feat(frontend): xxxx`, where `(frontend)` means that this PR mainly focuses on the frontend component.

You may also check out previous PRs in the [PR list](https://github.com/neulab/TheAgentCompany/pulls).

As described in [here](https://github.com/neulab/TheAgentCompany/labels), we create several labels. Every PR should better tag with corresponding labels.

### 2. Pull Request description

- If your PR is small (such as a typo fix), you can go brief.
- If it is large and you have changed a lot, it's better to write more details.


## How to begin
Please check the details in each parts.

For Server work: [gitlab](./servers/gitlab/README.md), [owncloud](./servers/owncloud/README.md), [plane](./servers/plane/README.md), [rocketchat](./servers/rocketchat/README.md)

For task work: [example](./workspaces/tasks/example/README.md)

## Tests
TODO: make sure code pass the test before submit.
