## Workspaces directory

This directory hosts tasks that are local to the examinee (e.g. agents or human testers). It is structured as follows:

```
├── base_image/
│   ├── Dockerfile
│   ├── init.sh
│   ├── eval.py
│   └── ...
├── tasks/
│   └── admin-arrange-meeting-rooms-image/
│       ├── Dockerfile
│       ├── evaluator.py
│       ├── checkpoints.md
│       ├── dependencies.yml
│       ├── task.md
|   └── ...
```

Explanations:
- base_image is the folder that contains shared functions, evaluation utilities, image build scripts, and other scaffolds.
- tasks is the folder for definitions of all 175 tasks, within which
  - Dockerfile defines the environment of each task setup
  - evaluator.py defines all checkpoint grading functions
  - checkpoints.md is the documentation for grading functions (for human reference only)
  - dependencies.yml defines the list of service dependencies
  - task.md is the task specification, contains background and requirements of each task, and is the **only** file that should be prompted to agents


## Full list of task images

We built and published all 175 task images. Please find the full list below, or download
the list [here](https://github.com/TheAgentCompany/TheAgentCompany/releases/download/1.0.0/tasks.md).

If you'd like to learn how task images are built, see [this GitHub workflow](https://github.com/TheAgentCompany/TheAgentCompany/blob/main/.github/workflows/task-release.yml).

- ghcr.io/theagentcompany/admin-arrange-meeting-rooms-image:1.0.0
- ghcr.io/theagentcompany/admin-ask-for-meeting-feedback-image:1.0.0
- ghcr.io/theagentcompany/admin-ask-for-upgrade-reimbursement-image:1.0.0
- ghcr.io/theagentcompany/admin-check-employees-budget-and-reply-image:1.0.0
- ghcr.io/theagentcompany/admin-check-employees-budget-and-reply-2-image:1.0.0
- ghcr.io/theagentcompany/admin-check-employees-budget-and-reply-and-record-image:1.0.0
- ghcr.io/theagentcompany/admin-collect-requests-and-compute-total-price-image:1.0.0
- ghcr.io/theagentcompany/admin-employee-info-reconciliation-image:1.0.0
- ghcr.io/theagentcompany/admin-get-best-vendor-quote-image:1.0.0
- ghcr.io/theagentcompany/admin-make-spreadsheet-image:1.0.0
- ghcr.io/theagentcompany/admin-mass-forms-filling-image:1.0.0
- ghcr.io/theagentcompany/admin-read-survey-and-summarise-image:1.0.0
- ghcr.io/theagentcompany/admin-remove-pages-pdf-image:1.0.0
- ghcr.io/theagentcompany/admin-translate-sales-chat-image:1.0.0
- ghcr.io/theagentcompany/admin-watch-video-image:1.0.0
- ghcr.io/theagentcompany/bm-classify-nationality-image:1.0.0
- ghcr.io/theagentcompany/ds-answer-numerical-data-question-image:1.0.0
- ghcr.io/theagentcompany/ds-answer-spreadsheet-questions-image:1.0.0
- ghcr.io/theagentcompany/ds-calculate-spreadsheet-stats-image:1.0.0
- ghcr.io/theagentcompany/ds-coffee-shop-database-management-image:1.0.0
- ghcr.io/theagentcompany/ds-find-meeting-spreadsheet-image:1.0.0
- ghcr.io/theagentcompany/ds-fix-table-values-and-missing-answers-image:1.0.0
- ghcr.io/theagentcompany/ds-format-excel-sheets-image:1.0.0
- ghcr.io/theagentcompany/ds-janusgraph-exercise-image:1.0.0
- ghcr.io/theagentcompany/ds-merge-multiple-sheets-image:1.0.0
- ghcr.io/theagentcompany/ds-organise-report-sus-data-image:1.0.0
- ghcr.io/theagentcompany/ds-predictive-modeling-image:1.0.0
- ghcr.io/theagentcompany/ds-sql-exercise-image:1.0.0
- ghcr.io/theagentcompany/ds-stock-analysis-slides-image:1.0.0
- ghcr.io/theagentcompany/ds-visualize-data-in-pie-and-bar-chart-image:1.0.0
- ghcr.io/theagentcompany/example-image:1.0.0
- ghcr.io/theagentcompany/finance-apply-tax-credit-image:1.0.0
- ghcr.io/theagentcompany/finance-budget-variance-image:1.0.0
- ghcr.io/theagentcompany/finance-check-attendance-payroll-image:1.0.0
- ghcr.io/theagentcompany/finance-create-10k-income-report-image:1.0.0
- ghcr.io/theagentcompany/finance-expense-validation-image:1.0.0
- ghcr.io/theagentcompany/finance-find-signatories-image:1.0.0
- ghcr.io/theagentcompany/finance-invoice-matching-image:1.0.0
- ghcr.io/theagentcompany/finance-nonqualified-bill-ask-for-reimburse-image:1.0.0
- ghcr.io/theagentcompany/finance-qualified-bill-ask-for-reimburse-image:1.0.0
- ghcr.io/theagentcompany/finance-r-d-activities-image:1.0.0
- ghcr.io/theagentcompany/finance-revenue-reconciliation-image:1.0.0
- ghcr.io/theagentcompany/finance-substantial-presence-test-image:1.0.0
- ghcr.io/theagentcompany/hr-analyze-outing-bills-image:1.0.0
- ghcr.io/theagentcompany/hr-check-attendance-multiple-days-image:1.0.0
- ghcr.io/theagentcompany/hr-check-attendance-multiple-days-department-image:1.0.0
- ghcr.io/theagentcompany/hr-check-attendance-multiple-days-department-with-chat-image:1.0.0
- ghcr.io/theagentcompany/hr-check-attendance-one-day-image:1.0.0
- ghcr.io/theagentcompany/hr-check-for-invalid-passwords-and-ask-for-valid-passwords-image:1.0.0
- ghcr.io/theagentcompany/hr-collect-feedbacks-image:1.0.0
- ghcr.io/theagentcompany/hr-collect-multiple-valid-passwords-image:1.0.0
- ghcr.io/theagentcompany/hr-create-career-ladder-image:1.0.0
- ghcr.io/theagentcompany/hr-create-employee-manual-image:1.0.0
- ghcr.io/theagentcompany/hr-delete-and-insert-user-image:1.0.0
- ghcr.io/theagentcompany/hr-get-valid-password-image:1.0.0
- ghcr.io/theagentcompany/hr-green-card-consultation-image:1.0.0
- ghcr.io/theagentcompany/hr-internal-tooling-slides-image:1.0.0
- ghcr.io/theagentcompany/hr-make-slides-introduce-leadership-image:1.0.0
- ghcr.io/theagentcompany/hr-mass-survey-image:1.0.0
- ghcr.io/theagentcompany/hr-massive-resume-screening-image:1.0.0
- ghcr.io/theagentcompany/hr-new-grad-job-description-image:1.0.0
- ghcr.io/theagentcompany/hr-new-grad-job-description-2-image:1.0.0
- ghcr.io/theagentcompany/hr-new-grad-job-description-3-image:1.0.0
- ghcr.io/theagentcompany/hr-organize-talent-info-image:1.0.0
- ghcr.io/theagentcompany/hr-pick-interviewer-1-image:1.0.0
- ghcr.io/theagentcompany/hr-pick-interviewer-2-image:1.0.0
- ghcr.io/theagentcompany/hr-pick-interviewer-3-image:1.0.0
- ghcr.io/theagentcompany/hr-populate-salary-increase-memo-image:1.0.0
- ghcr.io/theagentcompany/hr-resume-categorization-image:1.0.0
- ghcr.io/theagentcompany/hr-resume-screening-image:1.0.0
- ghcr.io/theagentcompany/hr-salary-analysis-image:1.0.0
- ghcr.io/theagentcompany/hr-transfer-group-image:1.0.0
- ghcr.io/theagentcompany/ml-generate-gradcam-image:1.0.0
- ghcr.io/theagentcompany/ml-grade-exam-image:1.0.0
- ghcr.io/theagentcompany/pm-add-new-moderator-image:1.0.0
- ghcr.io/theagentcompany/pm-ask-for-issue-and-create-in-gitlab-image:1.0.0
- ghcr.io/theagentcompany/pm-ask-issue-assignee-for-issue-status-and-update-in-plane-image:1.0.0
- ghcr.io/theagentcompany/pm-assign-issues-image:1.0.0
- ghcr.io/theagentcompany/pm-change-channel-ownership-image:1.0.0
- ghcr.io/theagentcompany/pm-check-backlog-update-issues-image:1.0.0
- ghcr.io/theagentcompany/pm-copy-plane-issues-to-gitlab-image:1.0.0
- ghcr.io/theagentcompany/pm-create-channel-message-image:1.0.0
- ghcr.io/theagentcompany/pm-create-channel-message-medium-image:1.0.0
- ghcr.io/theagentcompany/pm-create-channel-new-leader-image:1.0.0
- ghcr.io/theagentcompany/pm-create-plane-issue-image:1.0.0
- ghcr.io/theagentcompany/pm-create-teammate-channel-from-spreadsheet-image:1.0.0
- ghcr.io/theagentcompany/pm-distribute-information-image:1.0.0
- ghcr.io/theagentcompany/pm-monitor-new-bug-issues-image:1.0.0
- ghcr.io/theagentcompany/pm-monthly-attendance-slides-image:1.0.0
- ghcr.io/theagentcompany/pm-plan-personnel-for-new-project-image:1.0.0
- ghcr.io/theagentcompany/pm-prepare-meeting-with-customers-image:1.0.0
- ghcr.io/theagentcompany/pm-present-engineer-group-members-image:1.0.0
- ghcr.io/theagentcompany/pm-present-gitlab-info-as-ppt-image:1.0.0
- ghcr.io/theagentcompany/pm-projects-analytics-image:1.0.0
- ghcr.io/theagentcompany/pm-schedule-meeting-1-image:1.0.0
- ghcr.io/theagentcompany/pm-schedule-meeting-2-image:1.0.0
- ghcr.io/theagentcompany/pm-send-hello-message-image:1.0.0
- ghcr.io/theagentcompany/pm-send-notification-to-corresponding-user-image:1.0.0
- ghcr.io/theagentcompany/pm-update-gitlab-issue-from-plane-status-image:1.0.0
- ghcr.io/theagentcompany/pm-update-plane-issue-from-gitlab-status-image:1.0.0
- ghcr.io/theagentcompany/pm-update-project-milestones-image:1.0.0
- ghcr.io/theagentcompany/pm-update-sprint-cycles-image:1.0.0
- ghcr.io/theagentcompany/qa-escalate-emergency-image:1.0.0
- ghcr.io/theagentcompany/qa-update-issue-status-according-to-colleagues-image:1.0.0
- ghcr.io/theagentcompany/research-answer-questions-on-paper-image:1.0.0
- ghcr.io/theagentcompany/research-reproduce-figures-image:1.0.0
- ghcr.io/theagentcompany/sde-add-all-repos-to-docs-image:1.0.0
- ghcr.io/theagentcompany/sde-add-one-gitlab-pipeline-image:1.0.0
- ghcr.io/theagentcompany/sde-add-wiki-page-image:1.0.0
- ghcr.io/theagentcompany/sde-change-branch-policy-image:1.0.0
- ghcr.io/theagentcompany/sde-change-license-easy-image:1.0.0
- ghcr.io/theagentcompany/sde-change-license-hard-image:1.0.0
- ghcr.io/theagentcompany/sde-check-and-run-unit-test-image:1.0.0
- ghcr.io/theagentcompany/sde-check-high-priority-issue-image:1.0.0
- ghcr.io/theagentcompany/sde-close-all-gitlab-issues-image:1.0.0
- ghcr.io/theagentcompany/sde-close-all-issue-on-all-project-under-tac-workspace-image:1.0.0
- ghcr.io/theagentcompany/sde-close-all-prs-image:1.0.0
- ghcr.io/theagentcompany/sde-close-an-issue-image:1.0.0
- ghcr.io/theagentcompany/sde-collect-open-issues-image:1.0.0
- ghcr.io/theagentcompany/sde-copilot-arena-server-easy-add-suffix-image:1.0.0
- ghcr.io/theagentcompany/sde-copilot-arena-server-new-endpoint-image:1.0.0
- ghcr.io/theagentcompany/sde-copilot-arena-server-setup-image:1.0.0
- ghcr.io/theagentcompany/sde-copy-issues-to-plane-image:1.0.0
- ghcr.io/theagentcompany/sde-copy-table-from-pdf-to-xlsx-image:1.0.0
- ghcr.io/theagentcompany/sde-create-commit-table-for-all-gitlab-users-image:1.0.0
- ghcr.io/theagentcompany/sde-create-new-characters-image:1.0.0
- ghcr.io/theagentcompany/sde-create-new-gitlab-project-logo-image:1.0.0
- ghcr.io/theagentcompany/sde-create-new-release-image:1.0.0
- ghcr.io/theagentcompany/sde-create-new-repo-image:1.0.0
- ghcr.io/theagentcompany/sde-create-sqlite-database-image:1.0.0
- ghcr.io/theagentcompany/sde-debug-crashed-server-image:1.0.0
- ghcr.io/theagentcompany/sde-delete-all-project-under-plane-image:1.0.0
- ghcr.io/theagentcompany/sde-delete-all-repos-image:1.0.0
- ghcr.io/theagentcompany/sde-delete-stale-branch-image:1.0.0
- ghcr.io/theagentcompany/sde-dependency-change-1-image:1.0.0
- ghcr.io/theagentcompany/sde-find-answer-in-codebase-1-image:1.0.0
- ghcr.io/theagentcompany/sde-find-answer-in-codebase-2-image:1.0.0
- ghcr.io/theagentcompany/sde-find-answer-in-codebase-3-image:1.0.0
- ghcr.io/theagentcompany/sde-find-api-image:1.0.0
- ghcr.io/theagentcompany/sde-fix-factual-mistake-image:1.0.0
- ghcr.io/theagentcompany/sde-fix-rising-wave-datatype-image:1.0.0
- ghcr.io/theagentcompany/sde-implement-buffer-pool-manager-bustub-image:1.0.0
- ghcr.io/theagentcompany/sde-implement-covering-index-in-janusgraph-image:1.0.0
- ghcr.io/theagentcompany/sde-implement-hyperloglog-image:1.0.0
- ghcr.io/theagentcompany/sde-implement-raft-in-go-image:1.0.0
- ghcr.io/theagentcompany/sde-install-go-image:1.0.0
- ghcr.io/theagentcompany/sde-install-openjdk-image:1.0.0
- ghcr.io/theagentcompany/sde-issue-label-management-image:1.0.0
- ghcr.io/theagentcompany/sde-migrate-package-manager-image:1.0.0
- ghcr.io/theagentcompany/sde-milestone-meeting-image:1.0.0
- ghcr.io/theagentcompany/sde-move-bustub-wiki-image:1.0.0
- ghcr.io/theagentcompany/sde-move-page-to-cloud-image:1.0.0
- ghcr.io/theagentcompany/sde-pitch-idea-to-manager-image:1.0.0
- ghcr.io/theagentcompany/sde-reply-community-issue-by-asking-npc-image:1.0.0
- ghcr.io/theagentcompany/sde-reply-community-issue-with-fixed-reply-image:1.0.0
- ghcr.io/theagentcompany/sde-repo_profile_pic-image:1.0.0
- ghcr.io/theagentcompany/sde-report-agent-repos-image:1.0.0
- ghcr.io/theagentcompany/sde-report-unit-test-coverage-to-plane-image:1.0.0
- ghcr.io/theagentcompany/sde-run-all-unit-test-image:1.0.0
- ghcr.io/theagentcompany/sde-run-janusgraph-image:1.0.0
- ghcr.io/theagentcompany/sde-run-linter-on-openhands-image:1.0.0
- ghcr.io/theagentcompany/sde-run-rising-wave-locally-image:1.0.0
- ghcr.io/theagentcompany/sde-sotopia-create-agent-image:1.0.0
- ghcr.io/theagentcompany/sde-sotopia-create-agent-wo-repo-image:1.0.0
- ghcr.io/theagentcompany/sde-sotopia-dev-container-image:1.0.0
- ghcr.io/theagentcompany/sde-sotopia-update-ci-image:1.0.0
- ghcr.io/theagentcompany/sde-summarize-recent-issues-image:1.0.0
- ghcr.io/theagentcompany/sde-sync-from-origin-repo-image:1.0.0
- ghcr.io/theagentcompany/sde-troubleshoot-dev-setup-image:1.0.0
- ghcr.io/theagentcompany/sde-update-dev-document-image:1.0.0
- ghcr.io/theagentcompany/sde-update-issue-status-on-plane-image:1.0.0
- ghcr.io/theagentcompany/sde-update-readme-image:1.0.0
- ghcr.io/theagentcompany/sde-write-a-unit-test-for-append_file-function-image:1.0.0
- ghcr.io/theagentcompany/sde-write-a-unit-test-for-scroll_down-function-image:1.0.0
- ghcr.io/theagentcompany/sde-write-a-unit-test-for-search_file-function-image:1.0.0
