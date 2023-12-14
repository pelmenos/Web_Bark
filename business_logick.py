from collections import OrderedDict
from datetime import datetime
import sys
import requests
from abc import ABC, abstractmethod

from database import DatabaseManager

db = DatabaseManager('bookmark.db')


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        pass


class CreateBookmarksTableCommand(Command):
    def execute(self, data=None):
        db.create_table('bookmarks', {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            'url': "text not null",
            'notes': 'text',
            'date_added': 'text not null'
        })


class AddBookmarkCommand(Command):
    def execute(self, data, timestamp=None):
        data['date_added'] = timestamp or datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Закладка добавлена!'


class ListBookmarksCommand(Command):
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self, data=None):
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand(Command):
    def execute(self, id):
        db.delete('bookmarks', {'id': id})
        return 'Закладка удалена'


class EditBookmarkCommand(Command):
    def execute(self, data):
        db.update('bookmarks', data)
        return 'Закладка изменена'


class ImportGitHubStarsCommand(Command):
    def _extract_bookmark_info(self, repo):
        return {
            'title': repo['name'],
            'url': repo['html_url'],
            'notes': repo['description']
        }

    def execute(self, data):
        bookmarks_imported = 0
        github_username = data['github_username']
        page_of_result = f'https://api.github.com/users/{github_username}/starred'

        while page_of_result:
            stars = requests.get(page_of_result, headers={'Accept': 'application/vnd.github.v3.star+json'})
            page_of_result = stars.links.get('next', {}).get('url')

            for repo_info in stars.json():
                repo = repo_info['repo']

                if data['preserve_time']:
                    timestamp = datetime.strftime(repo_info['starred_at'], '%Y-%m-%dT-%H:%M:%SZ')
                else:
                    timestamp = None

                bookmarks_imported += 1

                AddBookmarkCommand().execute(self._extract_bookmark_info(repo), timestamp)

        return f'Импортировано {bookmarks_imported} закладок из помеченных звёздами репо'


class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()
