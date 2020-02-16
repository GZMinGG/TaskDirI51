import datetime
import os
from pathlib import Path
from time import sleep

##Если 'Timeout' > 5 сек = Авария
WARNING_TIMEOUT = 5 * 1000  # миллисекунд
## Чувствительность к колличеству строк с задержкой, что бы не выводить ложную тревогу
SENSITIVITY = 3
## Папка с исходными данными
SOURCE_FOLDER = Path('Input')
## Папка с отчетами
OUTPUT_FOLDER = Path('Output')


def main():
    os.system('chmod 777 -R Input')
    os.system('chmod 777 -R Output')
    files = set(os.listdir(SOURCE_FOLDER)) - set(os.listdir(OUTPUT_FOLDER))
    for file in files:
        with open(SOURCE_FOLDER / Path(file), 'r') as input_file:
            with open(OUTPUT_FOLDER / Path(file), 'w') as write_file:
                count_warning_timeout = 0
                max_timeout = 0
                for line in input_file:
                    split_line = line.strip().split(' ')
                    if not split_line or not split_line[-1].isdigit():
                        continue

                    timeout = int(split_line[-1])  # milliseconds
                    if timeout < WARNING_TIMEOUT and count_warning_timeout > SENSITIVITY:
                        date, time = split_line[:2]
                        datetime_line = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')

                        start_datetime_warning = datetime_line - datetime.timedelta(milliseconds=max_timeout)
                        duration_problem = (datetime_line - start_datetime_warning).seconds
                        write_file.write(f'Start problem: {start_datetime_warning.strftime("%Y:%m:%d %H:%M:%S")}' + f' Duration: {duration_problem} sec. \n')
                        count_warning_timeout = 0
                        max_timeout = 0
                    elif timeout > WARNING_TIMEOUT:
                        count_warning_timeout += 1
                        if timeout > max_timeout:
                            max_timeout = timeout
                    else:
                        count_warning_timeout = 0
                        max_timeout = 0


if __name__ == '__main__':
    while True:
        main()
        sleep(5)
