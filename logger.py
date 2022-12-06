from datetime import datetime as dt

def log(oper):
    with open('log.csv', 'a', encoding='utf8') as file:
        time = dt.now().strftime('%d-%m-%Y %H:%M')
        file.write('Время обращения {}; операция: {}\n'.format(time, oper))