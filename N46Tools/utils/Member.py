import json
import os

from N46Tools.exception.ArgsException import ArgsException


class MemberInfo:
    """
    This object provides member's info.
    """
    def __init__(self, member_info: dict) -> None:
        self.__name = member_info['name']
        self.__last_name_jp = member_info['last_name_jp']
        self.__first_name_jp = member_info['first_name_jp']
        self.__last_name_kana = member_info['last_name_kana']
        self.__first_name_kana = member_info['first_name_kana']
        self.__homepage_id = member_info['homepage_id']
        self.__message_id = member_info['message_id']
        self.__birthday = member_info['birthday']
        self.__generation = member_info['generation']

    @property
    def name(self) -> str:
        """English Name."""
        return self.__name

    @property
    def name_jp(self) -> str:
        """Japanese Name."""
        return f'{self.__last_name_jp}{self.__first_name_jp}'

    @property
    def last_name_jp(self) -> str:
        """Japanese Last Name."""
        return self.__last_name_jp

    @property
    def first_name_jp(self) -> str:
        """Japanese First Name."""
        return self.__first_name_jp

    @property
    def last_name_kana(self) -> str:
        """Japanese Last Name (Kana)."""
        return self.__last_name_kana

    @property
    def first_name_kana(self) -> str:
        """Japanese First Name (Kana)."""
        return self.__first_name_kana

    @property
    def homepage_id(self) -> int:
        """Homepage ID."""
        return self.__homepage_id

    @property
    def message_id(self) -> int:
        """Message ID."""
        return self.__message_id

    @property
    def birthday(self) -> str:
        """Birthday"""
        return self.__birthday

    @property
    def generation(self) -> int:
        """Generation."""
        return self.__generation


class MemberData:
    """
    This object loads all member's info from a JSON file.

    This object also provide a method to get a member's info.
    """
    def __init__(self) -> None:
        self.__data_path = os.path.join(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    os.path.pardir
                )
            ),
            'data/member_data.json'
        )
        self.__member_data_dict = dict()
        self.__member_data_dict_homepage_id = dict()
        self.__member_data_dict_message_id = dict()

        self.__load_data()

    def __load_data(self) -> None:
        """
        Load Member's data.
        """
        _member_info_list = None
        with open(self.__data_path, encoding='utf8') as file:
            _member_info_list = json.load(file)
        if not _member_info_list:
            _member_info_list = list()
        for _member_info in _member_info_list:
            self.__member_data_dict[_member_info['name']] = _member_info
            self.__member_data_dict_homepage_id[_member_info['homepage_id']] = _member_info
            self.__member_data_dict_message_id[_member_info['message_id']] = _member_info

    def get_member_info(self, name: str) -> MemberInfo:
        """
        Get member's info by member's English name.

        @param name: Member's English name.
        @return: Object of Member Info.
        """
        if name not in self.__member_data_dict.keys():
            err_msg = f"Member's name '{name}' does not exist."
            raise ArgsException(err_msg)
        return MemberInfo(self.__member_data_dict[name])

    def get_member_info_by_homepage_id(self, homepage_id: int) -> MemberInfo:
        """
        Get member's info by member's homepage ID.

        @param homepage_id: Member's homepage ID.
        @return: Object of Member Info.
        """
        if homepage_id not in self.__member_data_dict_homepage_id.keys():
            err_msg = f"Member's homepage id '{homepage_id}' does not exist."
            raise ArgsException(err_msg)
        return MemberInfo(self.__member_data_dict_homepage_id[homepage_id])

    def get_member_info_by_message_id(self, message_id: int) -> MemberInfo:
        """
        Get member's info by member's homepage ID.

        @param message_id: Member's English name.
        @return: Object of Member Info.
        """
        if message_id not in self.__member_data_dict_message_id.keys():
            err_msg = f"Member's message id '{message_id}' does not exist."
            raise ArgsException(err_msg)
        return MemberInfo(self.__member_data_dict_message_id[message_id])
