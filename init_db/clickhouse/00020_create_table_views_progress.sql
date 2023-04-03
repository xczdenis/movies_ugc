CREATE TABLE IF NOT EXISTS ${CH_DB_MOVIES}.views_progress ON CLUSTER ${CH_CLUSTER_NAME}
(
    created DateTime DEFAULT now(),
    id UInt64,
    movie_frame Int64,
    movie_id UUID,
    rating Float64,
    user_id Int64
)
ENGINE = ReplicatedMergeTree
PARTITION BY toYYYYMMDD(created)
ORDER BY id;
