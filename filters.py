from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAdmin(BaseFilter):
    admin_lists = []
    def __init__(self, admin_lists):
        self.admin_lists = admin_lists
    async def __call__(self, message:Message):
        if message.from_user.id in self.admin_lists:
            return 1
        else:
            return 0

class InAddFront(BaseFilter):
    info:  dict
    def __init__(self, info):
        self.info = info
    async def __call__(self, message:Message):
        if not message.from_user.id in self.info:
            return 0
        else:
            if self.info[message.from_user.id]['state'] == 'in_add_front':
                return 1
            else:
                return 0



class InAddBack(BaseFilter):
    info:  dict
    def __init__(self, info):
        self.info = info
    async def __call__(self, message:Message):
        if not message.from_user.id in self.info:
            return 0
        else:
            if self.info[message.from_user.id]['state'] == 'in_add_back':
                return 1
            else:
                return 0


class InAddTicket(BaseFilter):
    info:  dict
    def __init__(self, info):
        self.info = info
    async def __call__(self, message:Message):
        if not message.from_user.id in self.info:
            return 0
        else:
            if self.info[message.from_user.id]['state'] == 'in_add_ticket':
                return 1
            else:
                return 0

class IsNumber(BaseFilter):
    def __init__(self):
        pass
    async def __call__(self, message:Message):
        if message.text.isnumeric():
            return 1
        else:
            return 0

class InTest(BaseFilter):
    info:  dict
    def __init__(self, info):
        self.info = info
    async def __call__(self, message:Message):
        if not message.from_user.id in self.info:
            return 0
        else:
            if self.info[message.from_user.id]['state'] == 'in_test':
                return 1
            else:
                return 0

class InTestTicket(BaseFilter):
    info:  dict
    def __init__(self, info):
        self.info = info
    async def __call__(self, message:Message):
        if not message.from_user.id in self.info:
            return 0
        else:
            if self.info[message.from_user.id]['state'] == 'in_test_ticket':
                return 1
            else:
                return 0