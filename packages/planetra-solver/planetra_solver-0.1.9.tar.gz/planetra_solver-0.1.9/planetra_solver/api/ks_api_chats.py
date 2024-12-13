from .ks_api_main import KsAPI
from setuptools import find_packages


def create_chat(name: str) -> None:
    """
    Создает чат с переданным названием.
    :param name: название чата.
    :return: None.
    """
    if not isinstance(name, str):
        raise TypeError('Название чата должен быть строкой')
    KsAPI(to_log_in=True).request(
        '/chats/create',
        {'Name': name}
    )


def delete_chat(chat_uuid: str) -> None:
    """
    Удаляет чат с переданными UUIDs.
    :param chat_uuid: UUIDs чата.
    :return: None.
    """
    if not isinstance(chat_uuid, str):
        raise TypeError('Uuid чата должно быть строкой')
    KsAPI(to_log_in=True).request(
        '/chats/delete',
        {'UUID': chat_uuid},
    )


def send_message(chat_uuid: str, body: str, comment: str) -> None:
    """
    Отправляет сообщение в чат с переданными UUIDs.
    :param chat_uuid: UUIDs чата.
    :param body: тело чата.
    :param comment: комментарий.
    :return: None.
    """
    if not isinstance(chat_uuid, str):
        raise TypeError('Uuid чата должно быть строкой')
    if not isinstance(body, str):
        raise TypeError('body чата должно быть строкой')
    if not isinstance(comment, str):
        raise TypeError('comment чата должен быть строкой')
    KsAPI(to_log_in=True).request(
        '/chats/add-message',
        {'ChatUUID': chat_uuid, 'Body': body, 'Comment': comment},
    )

