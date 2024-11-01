Navigate to the gitlab repository for the JanusGraph project, and create a CI/CD action that processes every newly opened issue, and:

1. checks if the issue title starts with "fix:", "chore:", or "feat:", and if not comments "All issue titles must start with 'fix:', 'chore:', or 'feat:'"
2. checks if the issue body is less than 100 characters, and if so comments "All issues must have a body at least 100 characters long"

Create a new branch for your changes, and make a merge request to merge your changes into the main branch.
Make sure to include the words "comment formatting" in your merge request title.

Once you're done, merge your changes into the main branch.

Once it's in the main branch, open up an issue called "Dummy Issue 1" with a body more than 100 characters, and verify that the CI/CD action generates a comment saying "All issue titles must start with 'fix:', 'chore:', or 'feat:'".

Then, open up another issue with a titled "fix: Dummy Issue 2" but with a body less than 100 characters, and verify that the CI/CD action generates a comment saying "All issues must have a body at least 100 characters long".

If it is not working as expected, redo the task until it is working as expected.
