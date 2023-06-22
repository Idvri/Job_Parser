class Vacancy:

    def __init__(self, vacancy: dict):
        self.__properties = vacancy
        try:
            vacancy['id']
        except KeyError:
            pass
        else:
            self.__id = vacancy['id']
        try:
            vacancy['name']
        except KeyError:
            self.name = vacancy['profession']
        else:
            self.name = vacancy['name']
        if vacancy['salary']:
            self.__salary = vacancy['salary']
        else:
            self.__salary = None
        try:
            vacancy['snippet']
        except KeyError:
            self.__responsibility = vacancy['candidat'].replace('\n•', '').replace('\n', '').replace('\t', ''). \
                                        replace('  ', '')[:150] + '...'
        else:
            self.__responsibility = vacancy['snippet']['responsibility']
        try:
            vacancy['alternate_url']
        except KeyError:
            self.__url = vacancy['link']
        else:
            self.__url = vacancy['alternate_url']

    @property
    def id(self):
        return self.__id

    @property
    def properties(self):
        return self.__properties

    @property
    def salary(self):
        return self.__salary

    def __str__(self):
        if self.__salary and self.__salary['from'] and self.__responsibility:
            return f'''\nНазвание вакансии: {self.name}.
Зарплата от {self.__salary['from']} {self.__salary['currency']}.
Подробнее - {self.__responsibility.replace(' .', '.')}
Прямая ссылка на вакансию: {self.__url}\n'''
        elif self.__salary and self.__salary['from'] and not self.__responsibility:
            return f'''\nНазвание вакансии: {self.name}.
Зарплата от {self.__salary['from']} {self.__salary['currency']}.
Обязанности не указаны.
Прямая ссылка на вакансию: {self.__url}\n'''
        elif self.__salary and not self.__salary['from'] and self.__responsibility:
            return f'''\nНазвание вакансии: {self.name}.
Зарплата до {self.__salary['to']} {self.__salary['currency']}.
Подробнее - {self.__responsibility.replace(' .', '.')}
Прямая ссылка на вакансию: {self.__url}\n'''
        elif self.__salary and not self.__salary['from'] and not self.__responsibility:
            return f'''\nНазвание вакансии: {self.name}.
Зарплата до {self.__salary['to']} {self.__salary['currency']}.
Обязанности не указаны.
Прямая ссылка на вакансию: {self.__url}\n'''
        elif not self.__salary and self.__responsibility:
            return f'''\nНазвание вакансии: {self.name}.
Зарплата не указана.
Подробнее - {self.__responsibility.replace(' .', '.')}
Прямая ссылка на вакансию: {self.__url}\n'''
        else:
            return f'''\nНазвание вакансии: {self.name}.
Зарплата не указана.
Обязанности не указаны.
Прямая ссылка на вакансию: {self.__url}\n'''

    def __lt__(self, other):
        if self.__salary['from'] is None and self.__salary['to'] is None:
            min_self_salary = 0
        elif self.__salary['from'] is None:
            min_self_salary = self.__salary['to']
        elif self.__salary['to'] is None:
            min_self_salary = self.__salary['from']
        elif self.__salary['from'] < self.__salary['to']:
            min_self_salary = self.__salary['to']
        else:
            min_self_salary = self.__salary['from']

        if other.__salary['from'] is None and other.__salary['to'] is None:
            min_other_salary = 0
        elif other.__salary['from'] is None:
            min_other_salary = other.__salary['to']
        elif other.__salary['to'] is None:
            min_other_salary = other.__salary['from']
        if other.__salary['from'] < other.__salary['to']:
            min_other_salary = other.__salary['to']
        else:
            min_other_salary = other.__salary['from']

        return min_self_salary < min_other_salary

    def __le__(self, other):
        if self.__salary is None or other.__salary is None:
            return 'Не получится сравнить, так как у одной из вакансий не указана зарплата'
        else:
            return self.__salary <= other.salary

    def __gt__(self, other):
        if self.__salary['from'] is None and self.__salary['to'] is None:
            max_self_salary = 0
        elif self.__salary['from'] is None:
            max_self_salary = self.__salary['to']
        elif self.__salary['to'] is None:
            max_self_salary = self.__salary['from']
        elif self.__salary['from'] > self.__salary['to']:
            max_self_salary = self.__salary['from']
        elif self.__salary['from'] < self.__salary['to']:
            max_self_salary = self.__salary['to']
        else:
            max_self_salary = self.__salary['from']

        if other.__salary['from'] is None and other.__salary['to'] is None:
            max_other_salary = 0
        elif other.__salary['from'] is None:
            max_other_salary = other.__salary['to']
        elif other.__salary['to'] is None:
            max_other_salary = other.__salary['from']
        elif other.__salary['from'] > other.__salary['to']:
            max_other_salary = other.__salary['from']
        elif other.__salary['from'] < other.__salary['to']:
            max_other_salary = other.__salary['to']
        else:
            max_other_salary = other.__salary['from']

        return max_self_salary > max_other_salary

    def __ge__(self, other):
        if self.__salary is None or other.salary is None:
            return 'Не получится сравнить, так как у одной из вакансий не указана зарплата'
        else:
            return self.__salary > other.salary
