CREATE TABLE IF NOT EXISTS datasets.iso_country (
    name String,
    iso_2 String,
    iso_3 String
    ) ENGINE = MergeTree()
ORDER BY (name, iso_2, iso_3)