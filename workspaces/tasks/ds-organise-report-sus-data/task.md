We have a collection of spreadsheet data files under the "Data Analysis" folder at http://the-agent-company.com:8092?dir=/Documents. However, their names are inconsistent, with some being confusing or non-interpretable. Your task is to review the files in the "Data Analysis" folder and identify those with the following naming issues:

1. Files without Meaningful Names: Files with names that lack context or interpretability (e.g., a random list of characters, numbers or symbols) are to be avoided. Examples: `"rxuts 31t3b.xlsx"`.

2. Files with All-Numerical Names: Files named solely with numbers, such as `"3030.xlsx"`, should be avoided.

3. Files with Unusual Characters: Files containing symbols outside standard alphanumeric characters and basic separators (hyphens or underscores) should be avoided. Examples of unusual characters include: `;`, `!`, `@`, `#`, `~`, etc.

Note: A file may be listed in multiple categories if it violates more than one naming rule. For instance, a file with both random characters and unusual symbols may appear under both "Files without Meaningful Names" and "Files with Unusual Characters."

Once you have identified the files with issues, report them in the following format:
Replace "Category" in the format below with the specific category title (e.g., "Files without Meaningful Names," "Files with All-Numerical Names," or "Files with Unusual Characters") and include each file’s name along with its extension:

```
Category: file_name_1.xlsx, file_name_2.xlsx, ...
```

Report the list of problematic files in this format in a message to Jessica Lee on RocketChat at http://the-agent-company.com:3000.
