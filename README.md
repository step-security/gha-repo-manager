# Repo Manager via Github Actions
x
<!-- action-docs-description -->
## Description

Manage your Github repo(s) settings and secrets using Github Actions and a yaml file


<!-- action-docs-description -->

## Usage

This action manages your repo from a yaml file. You can manage:

* branch protection
* labels
* repos
* secrets
* repo settings
* Files

See [examples/settings.yml](./examples/settings.yml) for an example config file. The schemas for this file are in [repo_manager.schemas](./repo_manager/schemas).

### File Management -- Experimental

File management can copy files from your local environment to a target repo, copy files from one location to another in the target repo, move files in the target repo, and delete files in the target repo.

File operations are performed using the Github BLOB API and your PAT. Each file operation is a separate commit.

This feature is helpful to keep workflows or settings file in sync from a central repo to many repos.

### Example workflow

```yaml
name: Run Repo Manager
on: [workflow_dispatch]
jobs:
  repo-manager:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v5
    name: Checkout
    - name: Run RepoManager
      uses: step-security/gha-repo-manager@v1
      with:
        # Apply your settings to the repo, can also be check to just check repo settings vs your file or validate, to validate your
        # file is valid
        action: apply
        settings_file: .github/settings.yml
        # need a PAT that can edit repo settings
        token: ${{ secrets.GITHUB_PAT }}

```

<!-- action-docs-inputs -->
## Inputs

| parameter | description | required | default |
| - | - | - | - |
| action | What action to take with this action. One of validate, check, or apply. Validate will validate your settings file, but not touch your repo. Check will check your repo with your settings file and output a report of any drift. Apply will apply the settings in your settings file to your repo | `false` | check |
| settings_file | What yaml file to use as your settings. This is local to runner running this action. | `false` | .github/settings.yml |
| repo | What repo to perform this action on. Default is self, as in the repo this action is running in | `false` | self |
| github_server_url | Set a custom github server url for github api operations. Useful if you're running on GHE. Will try to autodiscover from env.GITHUB_SERVER_URL if left at default | `false` | none |
| token | What github token to use with this action. | `true` |  |



<!-- action-docs-inputs -->

<!-- action-docs-outputs -->
## Outputs

| parameter | description |
| - | - |
| result | Result of the action |
| diff | Diff of this action, dumped to a json string |



<!-- action-docs-outputs -->

<!-- action-docs-runs -->
## Runs

This action is a `docker` action.


<!-- action-docs-runs -->
