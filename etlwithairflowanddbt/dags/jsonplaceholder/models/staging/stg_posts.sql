select
  id as post_id,
  user_id,
  title,
  body,
  ingested_at
from raw_jsonplaceholder_posts;