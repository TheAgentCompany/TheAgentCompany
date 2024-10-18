COPY events FROM '/Users/gneubig/work/TheAgentCompany/workspaces/tasks/sde-debug-crashed-server/events-viewer/database/events.parquet' (FORMAT 'parquet');
COPY users FROM '/Users/gneubig/work/TheAgentCompany/workspaces/tasks/sde-debug-crashed-server/events-viewer/database/users.parquet' (FORMAT 'parquet');
