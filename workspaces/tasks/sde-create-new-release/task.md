You need to release a new version of RisingWave in gitlab. You can access it at http://the-agent-company.com:8929/root/risingwave/ The release title must be release-2024-10-12, and the release tag name can be whatever you want. You don’t need to upload any binary file.

The release notes must be the following verbatim: 

sql feature
Query syntax:
Public preview: Supports AS CHANGELOG to convert any stream into an append-only changelog.
SQL commands:
Breaking change: DECLARE cursor_name SUBSCRIPTION CURSOR is the same as DECLARE cursor_name SUBSCRIPTION CURSOR since now(), which will be consumed from the current time. DECLARE cursor_name SUBSCRIPTION CURSOR FULL will start consuming data from stock. The type of operation has changed to varchar. It is one of Insert, Delete, UpdateInset, or UpdateDelete.
