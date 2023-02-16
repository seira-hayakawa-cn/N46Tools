import datetime
import json
from typing import List, Dict, Optional

import requests


from .utils.Member import MemberData
from .exception.ArgsException import ArgsException


MEMBER_DATA = MemberData()

CATEGORY_LIST: List[str] = [
        'meet'      , 'live'        ,
        'goods'     , 'release'     ,
        'tv'        , 'radio'       ,
        'musical'   , 'book'        ,
        'web'       , 'others'
]

__HOST: str = 'https://www.nogizaka46.com/s/n46'

__HEADER: Dict[str, str] = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'ja-JP;q=1.0, zh-Hans-JP;q=0.9, en-JP;q=0.8',
    'referer': 'https://www.nogizaka46.com/s/n46',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36'
}


def __api_request(
        api_name: str,
        param: str,
        header: Dict[str, str] = None
) -> requests.Response:
    api_url: str = f'{__HOST}/api/list/{api_name}?{param}&callback=res'

    print(api_url)
    print(header['referer'])
    response: requests.Response = requests.get(api_url, headers=header)
    return response


def get_member() -> List[Dict[str, str]]:
    """
    Get all members' info.
    """
    api_name: str = 'member'

    current_timestamp: str = datetime.datetime.now().strftime('%M%S')
    referer_url: str = f'{__HOST}/?ima={current_timestamp}'

    __HEADER['referer'] = referer_url
    response: requests.Response = __api_request(
        api_name=api_name,
        param='',
        header=__HEADER
    )

    ret_list: Dict[str, str] = json.loads(response.text[4:-2])['data']
    return ret_list


def get_news(
        date: str = None,
        category: str = None,
        count: int = 10,
        start: int = 0
) -> List[Dict[str, str]]:
    """
    Get Nogizaka46 news.
    @param date: Time Range of the news. The format of date is 'YYYYMM', 
        which represents the year and month.
    @param category: Category of news. There are 10 categories: 
        'meet', 'live', 'goods', 'release', 'tv', 'radio', 'musical', 'book', 'web', 'others'.
    @param count: Count of news.
    @param start: Start index of news.
    @return: List of news dict.
    """
    api_name: str = 'news'

    current_timestamp: str = datetime.datetime.now().strftime('%M%S')
    param_list: List[str] = list()
    param: Optional[str] = None
    referer_url: Optional[str] = None

    if date is None and category is None:
        param_list.append(f'rw={count}')
        param_list.append(f'st={start}')
        param = '&'.join(param_list)

        referer_url = f'{__HOST}/?ima={current_timestamp}'
    else:
        param_list.append(f'ima={current_timestamp}')
        if date is not None:
            if not date.isdigit():
                err_msg: str = f'Date \'{date}\' is illegal: Not a digit string.'
                raise Exception(err_msg)
            elif len(date) != 6 and len(date) != 8:
                err_msg: str = f'Date \'{date}\' is illegal: length of date is illegal.'
                raise ArgsException(err_msg)
            elif len(date) == 6:
                try:
                    datetime.datetime.strptime(f'{date}01', '%Y%m%d')
                    param_list.append(f'dy={date}')
                except ValueError:
                    err_msg: str = f'Date \'{date}\' is illegal: month format error.\'.'
                    raise ArgsException(err_msg)
            elif len(date) == 8:
                try:
                    datetime.datetime.strptime(date, '%Y%m%d')
                    param_list.append(f'dy={date}')
                except ValueError:
                    err_msg: str = f'Date \'{date}\' is illegal: date format error.'
                    raise ArgsException(err_msg)
        if category is not None:
            if category not in CATEGORY_LIST:
                err_msg: str = f'Category \'{category}\' is illegal.'
                raise ArgsException(err_msg)
            else:
                param_list.append(f'ct={category}')
        param = '&'.join(param_list)
        referer_url = f'{__HOST}/{api_name}/list?{param}'

    __HEADER['referer'] = referer_url
    response: requests.Response = __api_request(
        api_name=api_name,
        param=param,
        header=__HEADER
    )

    ret_list: Dict[str, str] = json.loads(response.text[4:-2])['data']
    return ret_list


def get_schedule(
        member_name: str = None,
        date: str = None,
        category: str = None,
) -> List[Dict[str, str]]:
    """
    Get Nogizaka46 schedule.
    @param member_name: Member's English name.
    @param date: Time Range of the schedule. The format of date is 'YYYYMM', 
        which represents the year and month.
    @param category: Category of schedule. There are 10 categories: 
        'meet', 'live', 'goods', 'release', 'tv', 'radio', 'musical', 'book', 'web', 'others'.
    @return: List of schedule dict.
    """
    api_name: str = 'schedule'

    current_timestamp: str = datetime.datetime.now().strftime('%M%S')
    param: Optional[str] = None
    referer_url: Optional[str] = None
    param_list: List[str] = list()

    if member_name is None and date is None and category is None:
        date_param: str = datetime.datetime.now().strftime('%Y%m%d')
        param_list.append(f'dy={date_param}')
        param = '&'.join(param_list)

        referer_url = f'{__HOST}/?ima={current_timestamp}'
    else:
        date_param: Optional[str] = None
        category_param: Optional[str] = None
        if date is not None:
            if not date.isdigit():
                err_msg: str = f'Date \'{date}\' is illegal: Not a digit string.'
                raise Exception(err_msg)
            elif len(date) != 6 and len(date) != 8:
                err_msg: str = f'Date \'{date}\' is illegal: length of date is illegal.'
                raise ArgsException(err_msg)
            elif len(date) == 6:
                try:
                    datetime.datetime.strptime(f'{date}01', '%Y%m%d')
                    date_param = f'dy={date}'
                except ValueError:
                    err_msg: str = f'Date \'{date}\' is illegal: month format error.\'.'
                    raise ArgsException(err_msg)
            elif len(date) == 8:
                try:
                    datetime.datetime.strptime(date, '%Y%m%d')
                    date_param = f'dy={date}'
                except ValueError:
                    err_msg: str = f'Date \'{date}\' is illegal: date format error.'
                    raise ArgsException(err_msg)
        else:
            date_param = datetime.datetime.now().strftime('%Y%m')
            date_param = f'dy={date_param}'
        
        if category is not None:
            if category not in CATEGORY_LIST:
                err_msg: str = f'Category \'{category}\' is illegal.'
                raise ArgsException(err_msg)
            else:
                category_param = f'ct={category}'
        
        if member_name is not None:
            homepage_id: int = MEMBER_DATA.get_member_info(member_name).homepage_id
            param_list.append(f'list[]={homepage_id}')
            param_list.append(date_param)
            if category_param is not None:
                param_list.append(category_param)

            param = '&'.join(param_list)
            referer_url = f'{__HOST}/artist/{homepage_id}?ima={current_timestamp}'
        else:
            param_list.append(f'ima={current_timestamp}')
            param_list.append(date_param)
            if category_param is not None:
                param_list.append(category_param)

            param = '&'.join(param_list)
            referer_url = f'{__HOST}/media/list?{param}'

    __HEADER['referer'] = referer_url
    response: requests.Response = __api_request(
        api_name=api_name,
        param=param,
        header=__HEADER
    )

    ret_list: Dict[str, str] = json.loads(response.text[4:-2])['data']
    return ret_list

def get_blog(
        member_name: str = None,
        count: int = 8,
        start: int = 0
) -> List[Dict[str, str]]:
    """
    Get Nogizaka46 Member's blog.

    @param member_name: Member's English Name.
    @param count: Count of news.
    @param start: Start index of news.
    @return: List of blog dict.
    """
    api_name: str = 'blog'
    current_timestamp: str = datetime.datetime.now().strftime('%M%S')
    referer_url: Optional[str] = None

    param_list: List[str] = [
        f'ima={current_timestamp}'
    ]

    if member_name is None:
        count, start = 32, 0
        param_list.append(f'rw={count}')
        param_list.append(f'st={start}')
        referer_url = f'{__HOST}/diary/MEMBER?ima={current_timestamp}'
    else:
        param_list.append(f'rw={count}')
        param_list.append(f'st={start}')
        
        homepage_id: int = MEMBER_DATA.get_member_info(member_name).homepage_id
        param_list.append(f'ct={homepage_id}')

        referer_url = f'{__HOST}/artist/{homepage_id}?ima={current_timestamp}'

    param: str = '&'.join(param_list)

    __HEADER['referer'] = referer_url
    response: requests.Response = __api_request(
        api_name=api_name,
        param=param,
        header=__HEADER
    )

    ret_list = json.loads(response.text[4:-2])['data']
    return ret_list
