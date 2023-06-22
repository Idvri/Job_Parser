import json


class JsonHandler:

    def __init__(self, job_id, job_data):
        self.job_id = job_id
        self.job_data = job_data

    def save_data(self):
        try:
            open('data/vacancies.json', 'r', encoding='utf-8')
        except FileNotFoundError:
            print('\nСоздаём новый файл для сохранения вакансий "vacancies.json".')
            with open('data/vacancies.json', 'w', encoding='utf-8') as empty_file:
                job_list = []
                job_dict = self.job_data
                job_list.append(job_dict)
                empty_file.write(json.dumps(job_list, ensure_ascii=False, indent=4))
                return print('Вакансия сохранена')
        else:
            with open('data/vacancies.json', 'r', encoding='utf-8') as file:
                file_if = file.read()
                if len(file_if) == 0:
                    with open('data/vacancies.json', 'w', encoding='utf-8') as empty_file:
                        job_list = []
                        job_dict = self.job_data
                        job_list.append(job_dict)
                        empty_file.write(json.dumps(job_list, ensure_ascii=False, indent=4))
                        return print('Вакансия сохранена')
                else:
                    with open('data/vacancies.json', 'r', encoding='utf-8') as data_file_o:
                        job_list = json.load(data_file_o)
                    with open('data/vacancies.json', 'w', encoding='utf-8') as data_file_w:
                        job_dict = self.job_data
                        if job_dict not in job_list:
                            job_list.append(job_dict)
                            data_file_w.write(json.dumps(job_list, ensure_ascii=False, indent=4))
                            return print('Вакансия сохранена')

    @staticmethod
    def delete_data(job):
        with open('data/vacancies.json', 'r', encoding='utf-8') as data_file_o:
            job_list = json.load(data_file_o)
        with open('data/vacancies.json', 'w', encoding='utf-8') as data_file_w:
            job_list.remove(job)
            data_file_w.write(json.dumps(job_list, ensure_ascii=False, indent=4))
            return print('Вакансия удалена.')
