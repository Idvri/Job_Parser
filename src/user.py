import json

from src.api import HeadHunter, SuperJob, Engine


class User:

    def __init__(self, job_name: str, job_count: int, job_platform: int):
        self.job_name = job_name
        try:
            int(job_count)
        except ValueError:
            self.job_count = 20
        else:
            if job_count == 0:
                self.job_count = 20
            else:
                self.job_count = job_count
        self.job_platform = job_platform

    def get_job(self):
        if int(self.job_platform) == 1:
            vacancies = HeadHunter(self.job_name, self.job_count).get_vacancies()
            print('\nВы выбрали HeadHunter.')
            return vacancies
        elif int(self.job_platform) == 2:
            vacancies = SuperJob(self.job_name, self.job_count).get_vacancies()
            print('\nВы выбрали SuperJob.')
            return vacancies
        elif int(self.job_platform) == 3:
            vac_first = HeadHunter(self.job_name, self.job_count).get_vacancies()
            vac_second = SuperJob(self.job_name, self.job_count).get_vacancies()
            print('\nВы выбрали обе платформы.')
            return Engine.connect_two_lists(vac_first, vac_second)
        else:
            print('\nВы указали неверный номер платформы. Сеанс завершается.')
            quit()

    @classmethod
    def open_vacancies(cls):
        try:
            open('data/vacancies.json', 'r', encoding='utf-8')
        except FileNotFoundError:
            quit('\nФайл отсутсвует! Сессия завершается.')
        else:
            vacancies = json.load(open('data/vacancies.json', 'r', encoding='utf-8'))
            return vacancies

    @classmethod
    def get_decide(cls):
        decide = input('Ввод: ').lower()
        return decide
