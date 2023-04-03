from config.settings import kafka_settings

topic_schema_mapping = {
    kafka_settings.KAFKA_TOPIC_MOVIE_PLAYBACK_EVENT: kafka_settings.KAFKA_SCHEMA_MOVIE_PLAYBACK_EVENT,
    kafka_settings.KAFKA_TOPIC_CURRENT_PLAYBACK_POSITION: kafka_settings.KAFKA_SCHEMA_CURRENT_PLAYBACK_POSITION,
    kafka_settings.KAFKA_TOPIC_MOVIE_VIEWING: kafka_settings.KAFKA_SCHEMA_MOVIE_VIEWING,
}
