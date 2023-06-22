from src.vacancy import Vacancy
from src.user import User
from src.json_handler import JsonHandler
import json

if __name__ == "__main__":

    print('''Привет! Данная утилита поможет собрать нужные вам вакансии в одном месте и редактировать их.
Вам доступны несколько дейстивий:
1. Собрать вакансии, для начала формирования запросов нажмите "Enter";
2. Обработать вакансии, для этого напишите "Обработка";
3. Выйти из программы, напишите "Выйти".''')

    decide = User.get_decide()

    if decide == '':
        print('\nВыбран 1 пункт.')
        job_name = input('\nВведите наименование желаемой вакансии либо нажмите "Enter" и будут выгружены '
                         'вакансии "по умолчанию": ')
        job_count = input('\nУкажите кол-во вакансий для вывода (по умолчанию 20 шт.). '
                          'Примечание - при выборе 2 сервисов, будет выгружено в 2 раза больше вакансий: ')
        job_platform = input('\nДля поиска вакансий доступны 2 платформы - HeadHunter и SuperJob.'
                             '\nУкажите, пожалуйста, нужную платформу цифрами 1 и 2 соответсвенно, '
                             '\nлибо напишите 3, если хотите, чтобы вакансии предоставлялись с двух '
                             'платформ: ')
        user = User(job_name, job_count, job_platform)
        vacancies = user.get_job()
        print('\nВыгружаем вакансии...')

        for vacancy in vacancies:
            vac = Vacancy(vacancy)
            print(vac)
            print('Сохраним вакансию? Укажите ответ "да" или "нет", можно так же "Выйти": ')
            decide = User.get_decide()
            if decide == 'да':
                JsonHandler(vac.id, vac.properties).save_data()
            elif decide == 'нет':
                continue
            else:
                quit('\nСессия завершена.')
        print('\nВыгрузка вакансий завершена!')

    elif decide == 'обработка':
        print('\nВыбран 2 пункт.')

        try:
            User.open_vacancies()
        except json.decoder.JSONDecodeError:
            quit('\nФайл пуст. Сессия завершается.')
        else:
            saved_vacancies = User.open_vacancies()
            if len(saved_vacancies) == 0:
                quit('\nФайл пуст. Сессия завершается.')
            else:
                print('''\nОбработка вакансий. Выберите, что хотите сделать и укажите цифру варианта, 
либо вы можете "Выйти":
1. Вывести список вакансий;
2. Удаление вакансий;
3. Вывести вакансию с наибольшей зарплатой из сохранённых;
4. Вывести вакансию с наименьшей зарплатой из сохранённых.''')
                decide = User.get_decide()
                if decide == '1':
                    for sv in saved_vacancies:
                        print(Vacancy(sv))
                elif decide == '2':
                    for sv in saved_vacancies:
                        print(str(Vacancy(sv)))
                        print('Напишите "да", чтобы удалить вакансию или "нет", чтобы оставить и продолжить.')
                        del_decide = input('Ввод: ').lower()
                        if del_decide == 'да':
                            JsonHandler.delete_data(sv)
                        elif del_decide == 'нет':
                            continue
                        else:
                            quit('\nСессия завершена')
                elif decide == '3':
                    max_salary = 0
                    for sv in saved_vacancies:
                        if max_salary == 0:
                            max_salary = Vacancy(sv)
                        elif Vacancy(sv).salary is None:
                            continue
                        elif Vacancy(sv) > max_salary:
                            max_salary = Vacancy(sv)
                        else:
                            continue
                    print(f'\nВакансия с потанциально наибольшей зарплатой, с учётом верхней и нижней планки:'
                          f'\n{max_salary}')
                elif decide == '4':
                    min_salary = 1000000000000
                    for sv in saved_vacancies:
                        if min_salary == 1000000000000:
                            min_salary = Vacancy(sv)
                        elif Vacancy(sv).salary is None:
                            continue
                        elif Vacancy(sv) < min_salary:
                            min_salary = Vacancy(sv)
                        else:
                            continue
                    print(f'\nВакансия с потанциально наименьшей зарплатой, с учётом верхней и нижней планки:'
                          f'\n{min_salary}')
                else:
                    quit('\nСессия завершена')
    else:
        quit('\nСессия завершена.')
