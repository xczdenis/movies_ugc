-- Source table. This table doesn't store data (ENGINE = Null).
-- The data is stored in aggregating table 'movie_viewing_agg'.
CREATE TABLE IF NOT EXISTS ${CH_DB_MOVIES}.movie_viewing ON CLUSTER ${CH_CLUSTER_NAME}
(
    user_id UUID,
    movie_id UUID,
    viewed_seconds Int64
)
ENGINE = Null;


-- Distributed view for source table
CREATE TABLE IF NOT EXISTS default.movie_viewing ON CLUSTER ${CH_CLUSTER_NAME}
(
    user_id UUID,
    movie_id UUID,
    viewed_seconds Int64
)
ENGINE = Distributed(${CH_CLUSTER_NAME}, ${CH_DB_MOVIES}, movie_viewing, rand());


-- Aggregating table
CREATE TABLE IF NOT EXISTS ${CH_DB_MOVIES}.movie_viewing_agg ON CLUSTER ${CH_CLUSTER_NAME}
(
    user_id UUID,
    movie_id UUID,
    viewed_seconds AggregateFunction(sum, Int64)
)
ENGINE = ReplicatedAggregatingMergeTree
ORDER BY (user_id, movie_id)
SETTINGS replicated_deduplication_window = 0;


-- Materialized view for aggregating table
CREATE MATERIALIZED VIEW IF NOT EXISTS ${CH_DB_MOVIES}.movie_viewing_agg_mv ON CLUSTER ${CH_CLUSTER_NAME}
TO ${CH_DB_MOVIES}.movie_viewing_agg
AS
SELECT
    user_id,
    movie_id,
    sumState(viewed_seconds) AS viewed_seconds
FROM ${CH_DB_MOVIES}.movie_viewing
GROUP BY
    user_id,
    movie_id;


-- Distributed view for aggregating table
CREATE TABLE IF NOT EXISTS default.movie_viewing_agg ON CLUSTER ${CH_CLUSTER_NAME}
(
    user_id UUID,
    movie_id UUID,
    viewed_seconds AggregateFunction(sum, Int64)
)
ENGINE = Distributed(${CH_CLUSTER_NAME}, ${CH_DB_MOVIES}, movie_viewing_agg, rand());
