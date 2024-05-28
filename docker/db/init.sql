-- CREATE DATABASE piauiemdados;
\c piauiemdados -- Connect to the newly created database

-- Adjust runtime settings
ALTER SYSTEM SET max_connections TO '50';
ALTER SYSTEM SET shared_buffers TO '1GB';
ALTER SYSTEM SET work_mem TO '16MB';
ALTER SYSTEM SET maintenance_work_mem TO '512MB';

-- Reload the configuration to apply changes
SELECT pg_reload_conf();