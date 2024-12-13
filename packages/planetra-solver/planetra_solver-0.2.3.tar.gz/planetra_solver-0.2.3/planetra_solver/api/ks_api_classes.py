from .ks_api_main import KsAPI


def create_class(name: str) -> None:
    """
    Создает класс с переданным названием.
    :param name: название класса.
    :return: None.
    """
    if not isinstance(name, str):
        raise TypeError('Название должно быть строкой')
    KsAPI(to_log_in=True).request(
        '/classes/create-node',
        {'name': name, 'type': 'class'}
    )


def delete_class(class_id: str) -> None:
    """
    Удаляет класс с переданным UUID.
    :param class_id: UUID класса.
    :return: None.
    """
    if not isinstance(class_id, str):
        raise TypeError('ID класса должен быть строкой')
    KsAPI(to_log_in=True).request(
        '/classes/delete',
        {'UUID': class_id}
    )


def get_class_tree() -> None:
    """
    Возвращает дерево классов. В нем содержатся все классы и их показатели.
    :param None.
    :return: None.
    """
    request = KsAPI(to_log_in=True).request(
        '/classes/get-tree'
    )
    for obj in request['data']:
        print(obj)


def create_classes(name: list) -> None:
    """
    Создает класс с переданными названиями.
    Названия должны передаваться списком.
    :param name: список названий классов.
    :return: None.
    """
    if not isinstance(name, list):
        raise TypeError('name должен быть list')
    for names in name:
        KsAPI(to_log_in=True).request(
            '/classes/create-node',
            {'name': names, 'type': 'class'}
        )


def rename_class(class_id: str, name: str) -> None:
    """
    Переименовывает class с переданным UUID.
    :param class_id: UUID класса.
    :param name: Название класса.
    :return: None.
    """
    if not isinstance(class_id, str):
        raise TypeError('ID класса должен быть строкой')
    if not isinstance(name, str):
        raise TypeError('Название класса должно быть строкой')
    KsAPI(to_log_in=True).request(
        '/classes/update',
        {'name': name, 'UUID': class_id}
    )


def update_class_policy(class_id: str, denied_edit: bool = False, denied_read: bool = False) -> None:
    """
    Изменяет права доступа к классу.
    :param class_id: UUID класса.
    :param denied_edit: Запретить изменения(True/False)).
    :param denied_read: Запретить чтение(True/False)).
    :return: None.
    """
    if not isinstance(class_id, str):
        raise TypeError('ID класса должно быть строкой')
    if not isinstance(denied_edit, bool):
        raise TypeError('bool')
    if not isinstance(denied_read, bool):
        raise TypeError('bool')
    KsAPI(to_log_in=True).request(
        '/classes/update',
        {'UUID': class_id, 'DeniedEdit': denied_edit, 'DeniedRead': denied_read}
    )

