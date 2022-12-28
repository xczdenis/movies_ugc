#!/bin/bash
# Create table views_progress

set -e

clickhouse client -n <<-EOSQL
	CREATE TABLE IF NOT EXISTS $CH_DB_NAME.views_progress ON CLUSTER $CH_CLUSTER_NAME
	    (
	        created DateTime,
	        id Int64,
	        movie_frame Int64,
	        movie_id Int64,
	        rating Float64,
	        user_id Int64
	    )
	    ENGINE = ReplicatedMergeTree
	    PARTITION BY toYYYYMMDD(created)
	    ORDER BY id;
EOSQL
