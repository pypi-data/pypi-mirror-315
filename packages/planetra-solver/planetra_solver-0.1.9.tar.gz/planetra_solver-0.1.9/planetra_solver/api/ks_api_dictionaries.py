from .ks_api_main import KsAPI


def create_dict(name: str) -> None:
    """
    Создает справочник с переданным названием.
    :param name: название класса.
    :return: None.
    """
    if not isinstance(name, str):
        raise TypeError('Название справочника должно быть строкой')
    KsAPI(to_log_in=True).request(
        '/dictionaries/create-node',
        {'name': name, 'type': 'dictionary'}
    )


def create_dict_element(dict_uuid: str, name: str, shortname: str | None = None) -> None:
    """
    Создает элемент справочника с переданным названием.
    :param name: название элемента справочника.
    :param dict_uuid: uuid справочника.
    :param shortname: краткое название показателя.
    :return: None.
    """
    if not isinstance(dict_uuid, str):
        raise TypeError('Uuid справочника должен быть строкой')
    if not isinstance(name, str):
        raise TypeError('Название справочника должно быть строкой')
    KsAPI(to_log_in=True).request(
        '/dictionary-elements/create',
        {'name': name, 'dictionaryUuid': dict_uuid, 'shortName': shortname}
    )


def create_dict_elements(dict_uuid: str, names: list) -> None:
    """
    Создает элементы справочника с переданными названиями.
    :param names: названия элементов справочника.
    :param dict_uuid: uuid справочника.
    :return: None.
    """
    if not isinstance(dict_uuid, str):
        raise TypeError('ID справочника должен быть строкой')
    if not isinstance(names, list):
        raise TypeError('Название справочника должно быть строкой')
    for name in names:
        KsAPI(to_log_in=True).request(
            '/dictionary-elements/create',
            {'name': name, 'dictionaryUuid': dict_uuid}
        )


def delete_dict(dict_uuid: str) -> None:
    """
    Удаляет справочник с переданными UUIDs.
    :param dict_uuid: UUIDs справочника.
    :return: None.
    """
    if not isinstance(dict_uuid, str):
        raise TypeError('Uuid справочника должно быть строкой')
    KsAPI(to_log_in=True).request(
        '/dictionaries/delete-node',
        {'uuid': dict_uuid},
    )


def delete_dict_elements(elem_uuid: list) -> None:
    """
    Удаляет элементы справочника с переданными UUIDs.
    :param elem_uuid: UUIDs элементов.
    :return: None.
    """
    if not isinstance(elem_uuid, list):
        raise TypeError('список Uuid элементов должен быть list')
    for elem in elem_uuid:
        KsAPI(to_log_in=True).request(
            '/dictionary-elements/delete',
            {'UUID': elem},
        )


def delete_dict_element(elem_uuid: str) -> None:
    """
    Удаляет элемент справочника с переданным UUIDs.
    :param elem_uuid: UUIDs элементa.
    :return: None.
    """
    if not isinstance(elem_uuid, str):
        raise TypeError('Uuid элементa должен быть str')
    KsAPI(to_log_in=True).request(
        '/dictionary-elements/delete',
        {'UUID': elem_uuid},
    )


def get_dict_elements_list(dict_uuid: str) -> None:
    """
    Выводит список элементов справочника.
    :param dict_uuid: UUIDs справочника.
    :return: None.
    """
    if not isinstance(dict_uuid, str):
        raise TypeError('Uuid справочника должен быть str')
    request = KsAPI(to_log_in=True).request(
        '/dictionary-elements/get-list',
        {'UUID': dict_uuid},
    )
    for dict in request['data']:
        print(dict)

