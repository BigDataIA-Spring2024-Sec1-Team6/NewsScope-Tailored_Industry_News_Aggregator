{{ config(
    materialized='incremental',
    post_hook=[
      "TRUNCATE TABLE RAW_NEWSFEED.cnn.cnn_newsfeed;",
      "TRUNCATE TABLE RAW_NEWSFEED.cnbc.cnbc_newsfeed;",
      "TRUNCATE TABLE RAW_NEWSFEED.si.si_newsfeed;",
      "TRUNCATE TABLE RAW_NEWSFEED.wired.wired_newsfeed;",
      "DELETE FROM {{ this }} WHERE entry_date < DATEADD(week, -2, CURRENT_DATE());",      
      "DELETE FROM {{ this }} WHERE (headings, entry_date) NOT IN (
         SELECT headings, MAX(entry_date) 
         FROM {{ this }}
         GROUP BY headings
       );"
    ]
) }}

WITH cnn_newsfeed AS (
    SELECT * FROM {{ ref('stg_cnn') }}
),
cnbc_newsfeed AS (
    SELECT * FROM {{ ref('stg_cnbc') }}
),
si_newsfeed AS (
    SELECT * FROM {{ ref('stg_si') }}
),
wired_newsfeed AS (
    SELECT * FROM {{ ref('stg_wired') }}
),

combinedNewsFeed AS (
    SELECT * FROM cnn_newsfeed
    UNION
    SELECT * FROM cnbc_newsfeed
    UNION
    SELECT * FROM si_newsfeed
    UNION
    SELECT * FROM wired_newsfeed
)

SELECT *
FROM combinedNewsFeed
{% if is_incremental() %}
    WHERE entry_date > (SELECT MAX(entry_date) FROM {{ this }})
{% endif %}
