\qecho >>>> Insights Storage Analysis v1

\timing

\qecho >>>> Storage Utilization - Historical
SELECT min(time_stamp), now() - min(time_stamp) AS age FROM traffic.stats;

\qecho >>>> Storage Utilization - Database Size
SELECT sum(disk_space_used_mb)/1024 AS disk_space_used_gb FROM disk_storage WHERE storage_status = 'Active' and storage_usage = 'DATA,TEMP';

\qecho >>>> Storage Utilization - Distribution Across Nodes
SELECT node_name, storage_usage, to_char(sum(disk_space_free_mb)/1024,'999,999.99') AS disk_space_free_gb, to_char(sum(disk_space_used_mb)/1024,'999,999.99') AS disk_space_used_gb, avg(REGEXP_REPLACE(disk_space_Free_percent, '\D')) FROM disk_storage WHERE storage_status = 'Active' GROUP BY 1,2 ORDER BY 2, 1;

\qecho >>>> Storage Utilization - Partitions Sizes
SELECT table_schema, substr(projection_name,1,length(projection_name)-3) AS table_name, partition_key, sum(ros_size_bytes) AS ros_size_bytes, round(sum(ros_size_bytes)/1024^2)::int AS ros_size_MiB, round(sum(ros_size_bytes)/1024^3)::int AS ros_size_GiB, sum(ros_row_count) AS ros_row_count FROM partitions GROUP BY table_schema, table_name, partition_key ORDER BY table_schema, table_name, partition_key;

\qecho >>>> License Utilization
SELECT get_compliance_status();


\qecho >>>> Data Distribution Analysis - Table Sizes
SELECT anchor_table_schema, anchor_table_name, sum(ros_used_bytes) AS bytes FROM projection_storage GROUP BY anchor_table_schema, anchor_table_name ORDER BY bytes DESC, anchor_table_schema, anchor_table_name;


\qecho >>>> Data Distribution Analysis - Column Sizes
SELECT anchor_table_schema, anchor_table_name, anchor_table_column_name, sum(ros_used_bytes) ros_used_bytes FROM column_storage GROUP BY anchor_table_schema, anchor_table_name, anchor_table_column_name ORDER BY 4 DESC LIMIT 50;

\qecho >>>> Data Distribution Analysis - Recent Daily Traffic Summary
SELECT date_trunc('day', time_stamp)::date AS time_interval, count(distinct subscriber) AS subscribers, count(*) AS records, round(sum(bytes_in)/1024^3)::int AS GiB_in, round(sum(bytes_out)/1024^3)::int AS GiB_out, sum(connections_in) AS conns_in, sum(connections_out) AS conns_out FROM traffic.stats WHERE time_stamp >= DATE_TRUNC('day', CURRENT_TIMESTAMP - '14 day' :: INTERVAL) AND time_stamp <  DATE_TRUNC('day', CURRENT_TIMESTAMP) GROUP BY time_interval ORDER BY time_interval DESC;

\qecho >>>> Data Distribution Analysis - Traffic Records Per Subscriber
SELECT date_trunc('day',time_stamp)::date AS day, count(distinct subscriber) AS subscribers, count(*) AS records, round(count(*)/count(distinct subscriber))::int AS recs_per_sub FROM traffic.stats WHERE time_stamp >= DATE_TRUNC('day', CURRENT_TIMESTAMP - '14 day' :: INTERVAL) AND time_stamp <  DATE_TRUNC('day', CURRENT_TIMESTAMP) GROUP BY day ORDER BY day DESC;

\qecho >>>> Data Distribution Analysis - Distribution of Subscriber Daily Record Counts
SELECT floor(records/1000)*1000 AS bucket_min, count(*) FROM ( SELECT subscriber, count(*) AS records FROM traffic.stats WHERE time_stamp >= DATE_TRUNC('day', CURRENT_TIMESTAMP - '14 day' :: INTERVAL) AND time_stamp <  DATE_TRUNC('day', CURRENT_TIMESTAMP) GROUP BY subscriber ORDER BY records DESC ) t1 GROUP BY bucket_min ORDER BY bucket_min;


\qecho >>>> Score rollup duration
SELECT start_timestamp, CASE WHEN table_name = 'score.stats_hourly' THEN 'Score Hourly' WHEN table_name = 'score.peak_hours' THEN 'Score Daily' END AS rollup_name, end_timestamp - start_timestamp AS duration FROM query_requests INNER JOIN (SELECT DISTINCT session_id, request_id, anchor_table_schema || '.' || anchor_table_name AS table_name FROM projection_usage WHERE io_type = 'output' AND anchor_table_schema || '.' || anchor_table_name IN ('score.stats_hourly', 'score.peak_hours')) AS name USING(session_id, request_id) WHERE request_type = 'QUERY' ORDER BY start_timestamp DESC;

\timing
dd