from abc import ABC, abstractmethod
import random
import requests
import os


class Engine(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass

    @staticmethod
    def connect_two_lists(first_list, second_list):
        third_list = first_list + second_list
        random.shuffle(third_list)
        return third_list


class HeadHunter(Engine):
    api = 'https://api.hh.ru/vacancies'

    def __init__(self, job_name=None, page_count=None):
        self.vacancies = None
        self.job_name = job_name
        self.page_count = page_count
        if page_count == 0:
            self.page_count = 20

    def get_vacancies(self):
        response = requests.get(HeadHunter.api, f'text={self.job_name}&per_page={self.page_count}')
        self.vacancies = response.json()['items']
        return self.vacancies


class SuperJob(Engine):
    api = os.getenv('SJ_API_KEY').replace('\t', '')

    def __init__(self, job_name=None, page_count=None):
        self.vacancies = None
        self.job_name = job_name
        self.page_count = page_count
        if page_count == 0:
            self.page_count = 20

    def get_vacancies(self):
        response = requests.get(f'https://api.superjob.ru/2.0/vacancies', headers={"X-Api-App-Id": SuperJob.api},
                                params={'keyword': self.job_name, 'count': self.page_count})
        self.vacancies = response.json()['objects']
        new_vac_list = list()
        for sj_vac in self.vacancies:
            if sj_vac['payment_from'] == 0 and sj_vac['payment_to'] == 0:
                sj_vac['salary'] = None
            else:
                sj_vac['salary'] = {'from': sj_vac['payment_from'], 'to': sj_vac['payment_to'],
                                    'currency': sj_vac['currency'].upper()}
            del sj_vac['payment_from']
            del sj_vac['payment_to']
            del sj_vac['currency']
            new_vac_list.append(sj_vac)
        return new_vac_list
