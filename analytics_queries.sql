-- Analytics Queries

-- Traffic daily summary for the last two weeks
\echo 'Traffic daily summary for the last two weeks'
\qecho >>>> Traffic daily summary for the last two weeks
select time_stamp, subscriber_count from traffic.stats_overview_daily where time_stamp > current_timestamp - 14;
 
 
-- Traffic data storage stats
\echo 'Traffic data storage stats'
\qecho >>>> Traffic data storage stats
SELECT partition_key, sum(ros_size_bytes) traffic_ros_size_bytes, sum(ros_row_count) traffic_ros_row_count FROM partitions WHERE projection_name ILIKE 'stats_b%' OR projection_name ILIKE 'stats_super%' GROUP BY partition_key ORDER BY 1;
 
-- Column Storage Stats per column
\echo Column Storage Stats per column
\qecho >>>> Column Storage Stats per column
SELECT anchor_table_schema, anchor_table_name, anchor_table_column_name, sum(ros_used_bytes) ros_used_bytes FROM column_storage GROUP BY anchor_table_schema, anchor_table_name, anchor_table_column_name ORDER BY 4 DESC LIMIT 50;
 
 
-- Column Storage Stats per table
\echo 'Column Storage Stats per table'
\qecho >>>> Column Storage Stats per table
select anchor_table_schema, anchor_table_name, sum(ros_used_bytes) ros_used_bytes from column_storage group by anchor_table_schema, anchor_table_name order by 3 desc limit 50;
 
 
-- Projections
\echo 'Projections'
\qecho >>>> Projections
select * from projection_storage where used_bytes > 1000000000;
 
 
-- Score Hourly Rollups
\echo 'Score Hourly Rollups'
\qecho >>>> Score Hourly Rollups
select left(query,80) sql, (query_duration_us/1000/1000)::integer duration, processed_row_count, reserved_extra_memory from query_profiles where query ilike 'insert into score.stats_hourly%' order by 2 desc limit 50;
 
 
-- Traffic Rollups
\echo 'Traffic Rollups'
\qecho >>>> Traffic Rollups
select * from (select row_number() over (partition by job_path order by duration desc) rn, * from datacore.job_history where started_at > current_timestamp - 7) t where rn <= 5 order by job_path, rn;
 
 
-- Peak Hour Rows
\echo 'Peak Hour Rows'
\qecho >>>> Peak Hour Rows
select count(*) total_rows_peak, count(case when server_hostname = '' then null else server_hostname end) server_hostname_exists, count(case when subscriber = '' then null else subscriber end) subscriber_exists  from traffic.stats s, score.peak_hours p where p.peak >= current_timestamp - 1 and s.time_stamp = p.peak;
 
 
-- Server Hostname analysis
\echo 'Server Hostname analysis'
\qecho >>>> Server Hostname analysis
select approximate_count_distinct(s.subscriber) distinct_sub_peak, approximate_count_distinct(s.server_hostname) distinct_hostname_peak from traffic.stats s, score.peak_hours p where p.peak >= current_timestamp - 1 and s.time_stamp = p.peak;
 
 
-- Server Hostname cardinality analysis
\echo 'Server Hostname cardinality analysis'
\qecho >>>> Server Hostname cardinality analysis
with sub as (select s.subscriber, count(s.server_hostname) cnt, count(distinct s.server_hostname) cnt_dist from traffic.stats s, score.peak_hours p where p.peak >= current_timestamp - 1 and time_stamp = p.peak and s.server_hostname is not null group by subscriber) select avg(cnt) hostname_per_sub, avg(cnt_dist) distinct_hostname_per_host, avg(cnt/cnt_dist) ratio from sub;


-- Disk utilization
\echo 'Disk utilization'
\qecho >>>> Disk utilization
select node_name, storage_usage, to_char(sum(disk_space_free_mb)/1024,'9,999.99') as disk_space_free_gb 
, to_char(sum(disk_space_used_mb)/1024,'9,999.99') as disk_space_used_gb, avg(REGEXP_REPLACE(disk_space_Free_percent, '\D'))
from disk_storage where storage_status = 'Active' group by 1,2 order by 2, 1;


-- Moveout timings
\echo 'Moveout timings'
\qecho >>>> Moveout timings
select min(duration), max(duration), avg(duration) 
from (select start.time as start_time, complete.time as complete_time, complete.time - start.time as duration, start.node_name, start.transaction_id, start.operation
           , start.event as start_event, complete.event as complete_event 
        from (select * from dc_tuple_mover_events where operation = 'Moveout' and event = 'Start') as start 
       inner join (select * from dc_tuple_mover_events where operation = 'Moveout' and event = 'Complete') as complete 
          on start.transaction_id = complete.transaction_id and start.node_name = complete.node_name 
       order by start_time) sq ;


-- Mergeout timings
\echo 'Moveout timings'
\qecho >>>> Moveout timings
select min(duration), max(duration), avg(duration) 
from (select start.time as start_time, complete.time as complete_time, complete.time - start.time as duration, start.node_name, start.transaction_id, start.operation
           , start.event as start_event, complete.event as complete_event 
       from (select * from dc_tuple_mover_events where operation = 'Mergeout' and event = 'Start') as start 
      inner join (select * from dc_tuple_mover_events where operation = 'Mergeout' and event = 'Complete') as complete 
         on start.transaction_id = complete.transaction_id and start.node_name = complete.node_name 
      order by start_time) sq;


-- Disk space used by the biggest tables
\echo 'Disk space used by the biggest tables'
\qecho >>>> Disk space used by the biggest tables
select projection_schema, anchor_table_name
, to_char(sum(used_bytes)/1024/1024/1024,'999,999.99') as disk_space_used_gb 
from projection_storage 
group by projection_schema, anchor_table_name 
order by disk_space_used_gb desc limit 10;


-- Overview of system issues
\echo 'Overview of system issues'
\qecho >>>> Overview of system issues
select event_Category, event_Type, event_description, count(*) from query_Events group by 1,2,3 order by 4 desc  ;
