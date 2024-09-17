from typing import NamedTuple


class Buttons(NamedTuple):
    # Main menu
    create_task: str = 'create_note'
    get_task_for_tag: str = 'search'
    get_task: str = 'get_task'
    get_all_task: str = 'notes'


class Messages(NamedTuple):
    start: str = (
        'Добро пожаловать в бота "Taski".\n'
    )
    menu: str = 'Вот чем я могу Вам помочь:'


class Lexicon(NamedTuple):
    buttons: Buttons = Buttons()
    messages: Messages = Messages()


lexicon = Lexicon()
