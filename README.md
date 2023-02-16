# N46Tools

An Python API wrapper for [Nogizaka46 Official Website](https://www.nogizaka46.com/).


## How to use

```python
from N46Tools import Homepage

news_list = Homepage.get_news(
    category='radio'
)

# schedule
schedule_list = Homepage.get_schedule(
    member_name='seira hayakawa',
    date='20230210'
)

# blog
blog_list = Homepage.get_blog(
    member_name='seira hayakawa'
)
```