import os

import business_logick as commands


class Option:
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data)
        print(message)

    def __str__(self):
        return self.name


def print_options(data):
    for word, option in data.items():
        print(f'({word}) ({option})')
    print()


def correct_choice(choice, options):
    return choice.upper() in options


def get_option_choice(options):
    choice = input('Выберите действие: ')
    while not correct_choice(choice, options):
        print('Недопустимый вариант')
        choice = input('Выберите действие: ')
    return options[choice.upper()]


def get_user_input(label, required=True):
    answer = input(f'{label}: ') or None
    while required and None:
        answer = input(f'{label}: ') or None
    return answer


def get_github_options():
    return {'github_username': get_user_input('Пользовательское имя GitHub'),
            'preserve_time': get_user_input('Сохранить метки времени [Y/n]', required=False) in ['Y', 'y', None]}


def get_new_bookmark_data():
    return {
        'title': get_user_input('Название'),
        'url': get_user_input('Url'),
        'notes': get_user_input('Примечание', required=False)
    }


def get_criteria_for_delete():
    return get_user_input('Введи id закладки')


def get_criteria_for_update():
    data = dict()
    id = get_user_input('Введите id закладки')
    column = get_user_input('-title\n-url\n-note\nЧто нужно изменить')
    value = get_user_input('Новое значение') if column != 'note' else get_user_input('Новое значение', required=False)
    data[column] = value
    column = get_user_input('Изменить что-то ещё(Enter если нет)')
    while column:
        value = get_user_input('Новое значение') if column != 'note' else get_user_input('Новое значение', required=False)
        data[column] = value
        column = get_user_input('Изменить что-то ещё(Enter если нет)')
    return data, id


def clear_screen():
    clear = 'cls'
    os.system(clear)


def loop():
    option = {
        'A': Option('Добавить закладку', commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data),
        'B': Option('Показать список закладок по дате', commands.ListBookmarksCommand()),
        'T': Option('Показать список закладок по названию', commands.ListBookmarksCommand(order_by='title')),
        'U': Option('Изменить закладку', commands.EditBookmarkCommand(), prep_call=get_criteria_for_update),
        'D': Option('Удалить закладку', commands.DeleteBookmarkCommand(), prep_call=get_criteria_for_delete),
        'G': Option('Добавить закладки из GitHub', commands.ImportGitHubStarsCommand(), prep_call=get_github_options),
        'Q': Option('Выйти', commands.QuitCommand()),
    }

    clear_screen()
    print_options(option)
    chosen_option = get_option_choice(option)
    clear_screen()
    chosen_option.choose()

    _ = input('Нажмите ENTER для возврата в меню.')


if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute()

    while True:
        loop()
