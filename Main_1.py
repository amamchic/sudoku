import time, os, sys

# словарь, присваивающий значение номеру квадрата в зависимости от индексов ячеек:
square_dict = {'11': 1, '12': 1, '13': 1, '21': 1, '22': 1, '23': 1, '31': 1, '32': 1, '33': 1,
               '14': 2, '15': 2, '16': 2, '24': 2, '25': 2, '26': 2, '34': 2, '35': 2, '36': 2,
               '17': 3, '18': 3, '19': 3, '27': 3, '28': 3, '29': 3, '37': 3, '38': 3, '39': 3,
               '41': 4, '42': 4, '43': 4, '51': 4, '52': 4, '53': 4, '61': 4, '62': 4, '63': 4,
               '44': 5, '45': 5, '46': 5, '54': 5, '55': 5, '56': 5, '64': 5, '65': 5, '66': 5,
               '47': 6, '48': 6, '49': 6, '57': 6, '58': 6, '59': 6, '67': 6, '68': 6, '69': 6,
               '71': 7, '72': 7, '73': 7, '81': 7, '82': 7, '83': 7, '91': 7, '92': 7, '93': 7,
               '74': 8, '75': 8, '76': 8, '84': 8, '85': 8, '86': 8, '94': 8, '95': 8, '96': 8,
               '77': 9, '78': 9, '79': 9, '87': 9, '88': 9, '89': 9, '97': 9, '98': 9, '99': 9}

# Список экземпляров всех ячеек
Cell_list = []

# список нерешенных ячеек
Nonlist = []

# Словарь для решенных ячеек
Val_dict = {}

# Список сохраненных точек ветвления, содержащих ячейку с вариативными значениями
SavePoints = []

# Флаг, говорящий о том, что решение сейчас находится в вариативном цикле
Variating = False

# Флаг, свидетельствующий о наличии ошибки
Error = False

def Main():
    start = time.perf_counter()  # Фиксация времени старта
    sudoku()  # Формирование исходных данных
    neighbours_call()  # Оценка соседей для каждой ячейки
    creating()  # Создание квадратов, строк и столбцов.
    print('Исходное количество неизвестных ячеек: ' + str(len(Nonlist)))

    # Решение происходит до тех пор, пока не останется неизвестных значений ячеек.
    while len(Nonlist) != 0:
        Solver_1 = len(Nonlist)  # Переменная нужна для перехода на более сложный решатель.
        print('Попытка решения простым алгоритмом...')
        for cell in Nonlist:
            # Попытка поиска решения для каждой ячейки простым способом.
            cell.cell_solve_1()
        print('Количество неизвестных ячеек после итерации: ' + str(len(Nonlist)))

        # Если количество неизвестных ячеек после итерации не изменилось, следует переход к усложненному решателю.
        if Solver_1 == len(Nonlist):
            print('Простой алгоритм не справился с итерацией. Переход к усложненному алгоритму...')
            changing()  # Обновление информации в квадратах, строках и столбцах
            Solver_2 = len(Nonlist)
            for cell in Nonlist:
                cell.cell_solve_2()
                if Solver_2 != len(Nonlist):
                    break
            print('Количество неизвестных ячеек после итерации усложненного алгоритма: ' + str(len(Nonlist)))

            # Если количество неизвестных ячеек после итерации не изменилось, следует переход к вариативному
            # решателю.
            if Solver_2 == len(Nonlist):
                print('Усложненный алгоритм не справился с итерацией. Переход к вариативному алгоритму...')
                Variating = True
                # cell_solve_3()
                print('Значения ячеек:' + str(Val_dict))
                finish = time.perf_counter()  # Фиксация времени финиша
                print('Затраченное время:' + str(finish - start) + ' секунд(ы)')
                for cell in Cell_list:
                    if cell.value == None:
                        print(cell.name)
                        print(cell.eva_set)
                sys.exit()
    print('Значения ячеек:' + str(Val_dict))
    finish = time.perf_counter()  # Фиксация времени финиша
    print('Затраченное время:' + str(finish - start) + ' секунд(ы)')


def sudoku_case():
    """ Поле судоку"""

    sudoku_path = os.getcwd()
    N = None
    Case = {'Cell111': N, 'Cell112': N, 'Cell113': 3, 'Cell214': N, 'Cell215': N, 'Cell216': N, 'Cell317': 4,
            'Cell318': N, 'Cell319': 5,
            'Cell121': N, 'Cell122': N, 'Cell123': 1, 'Cell224': N, 'Cell225': N, 'Cell226': 4, 'Cell327': N,
            'Cell328': N, 'Cell329': 2,
            'Cell131': N, 'Cell132': N, 'Cell133': N, 'Cell234': N, 'Cell235': 8, 'Cell236': N, 'Cell337': 3,
            'Cell338': 1, 'Cell339': N,
            'Cell441': 1, 'Cell442': N, 'Cell443': 7, 'Cell544': N, 'Cell545': N, 'Cell546': 9, 'Cell647': N,
            'Cell648': N, 'Cell649': N,
            'Cell451': 3, 'Cell452': N, 'Cell453': N, 'Cell554': N, 'Cell555': 2, 'Cell556': N, 'Cell657': N,
            'Cell658': 4, 'Cell659': 7,
            'Cell461': N, 'Cell462': N, 'Cell463': 4, 'Cell564': 3, 'Cell565': N, 'Cell566': N, 'Cell667': N,
            'Cell668': N, 'Cell669': 1,
            'Cell771': N, 'Cell772': N, 'Cell773': N, 'Cell874': N, 'Cell875': N, 'Cell876': 6, 'Cell977': N,
            'Cell978': N, 'Cell979': 3,
            'Cell781': N, 'Cell782': 2, 'Cell783': N, 'Cell884': 4, 'Cell885': 3, 'Cell886': N, 'Cell987': N,
            'Cell988': N, 'Cell989': 5,
            'Cell791': N, 'Cell792': 6, 'Cell793': 3, 'Cell894': N, 'Cell895': 1, 'Cell896': N, 'Cell997': 9,
            'Cell998': N, 'Cell999': N, }

    if os.path.exists(sudoku_path + '/sudoku.txt'):
        with open('sudoku.txt', 'r') as file:
            line_num = 1
            for line in file:
                val_list = line.rstrip()
                col_num = 1
                for val in val_list:
                    sq_num = square_dict[str(line_num) + str(col_num)]
                    if val == '-':
                        Case['Cell' + str(sq_num) + str(line_num) + str(col_num)] = None
                    else:
                        Case['Cell' + str(sq_num) + str(line_num) + str(col_num)] = int(val)
                    col_num += 1
                line_num += 1

    return Case


def sudoku():
    """ Создание пустого судоку с объектами в виде ячеек """

    cell_list = []
    line = 1
    for line_val in range(9):
        column = 1
        for column_val in range(9):
            square = square_dict[str(line) + str(column)]
            cell_list.append(
                Cell(square, line, column, sudoku_case()["Cell" + str(square) + str(line) + str(column)],
                     "Cell" + str(square) + str(line) + str(column)))
            column += 1
        line += 1
    return cell_list


# Заполняет список соседей для каждой ячейки
def neighbours_call():
    for cell in Cell_list:
        cell.sq_call()
        cell.line_call()
        cell.col_call()


# Создает 9 квадратов, строк и столбцов, содержащих информацию о своих ячейках.
def creating():
    for num in range(9):
        Square(num + 1)
        Line(num + 1)
        Column(num + 1)
    changing()


def changing():
    for square in Square.sq_o_dict:
        Square.sq_o_dict[square].changing()
        Line.ln_o_dict[square].changing()
        Column.cl_o_dict[square].changing()


def cell_solve_3():
    """ Вариативное решение. Выбирается ячейка с двумя возможными значениями, которой присваивается первое из них.
    При этом создается переменная, содержащая поле до начала входа в вариативное решение. Появляется механизм
    отслеживания ошибки, который проверяет множество доступных значений для ячеек. Как только у ячейки такое множество
    становится равно нулю - производится откат к предыдущему полю и выбирается второе из возможных значений."""


    for cell in Cell_list:
        if len(cell.eva_set) == 2:
            SavePoints.append(cell)
            cell.value = list(cell.eva_set)[0]
            break
    

# Откат всех ячеек к предыдущему значению при ошибке
def returnsp():
    for cell in Cell_list:
        if not cell.validated and cell.value is not None:
            cell.value = None
            Val_dict[cell.name] = cell.value
            Nonlist.append(cell)

#           !!! КЛАССЫ !!!

class Cell:
    """ Ячейка поля судоку. Она должна иметь номер квадрата(sq), строки(line) и столбца(col)."""

    def __init__(self, sq, line, col, value, name):

        #       !!!     Атрибуты    !!!
        self.my_square = None  # Привязка к своему квадрату.
        self.neva_sq_set_nei = None  # Невозможные значения для соседей по квадрату.
        self.my_line = None  # Привязка к своей строке.
        self.neva_ln_set_nei = None  # Невозможные значения для соседей по строке.
        self.my_column = None  # Привязка к своему столбцу.
        self.neva_cl_set_nei = None  # Невозможные значения для соседей по столбцу.
        self.name = name  # Имя ячейки формата "Сell111", где первая цифра - номер квадрата.
        # вторая цифра - номер строки, а третья - номер столбца.
        self.sq = sq  # Номер квадрата.
        self.line = line  # Номер строки.
        self.col = col  # Номер столбца.
        self.value = value  # Значение ячейки. При отсутствии значения - None.
        self.neighbours_list = []  # Список всех соседей.
        self.eva_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # Множество доступных ячеек.
        self.neva_set = set()  # Множество недоступных ячеек.
        self.validated = False  # Уверенность в значении ячейки. True - если точное.
        self.variate = False  # Маркер варьируемой ячейки. True - если сейчас в нее подставляется случайное значение.
        self.erroredVal = set()  # Значения, которые были обследованы и привели к ошибке.

        #       !!! Методы  !!!

        # Заполнение списков при создании ячеек
        # Добавление экземпляра в список ячеек при создании.
        Cell_list.append(self)

        # Добавление экземпляра в список нерешенных ячеек при создании, если value == None.
        if self.value is None:
            Nonlist.append(self)
        else:
            Val_dict[self.name] = self.value
            self.neva_set = self.eva_set - {value}
            self.eva_set = {self.value}

    # Получение списка соседей по квадрату      !!!     Оптимизировать поиск    !!!
    def sq_call(self):
        for cell in Cell_list:
            if cell != self and cell.sq == self.sq and cell not in self.neighbours_list:
                self.neighbours_list.append(cell)

    # Получение списка соседей по строке      !!!     Оптимизировать поиск    !!!
    def line_call(self):
        for cell in Cell_list:
            if cell != self and cell.line == self.line and cell not in self.neighbours_list:
                self.neighbours_list.append(cell)

    # Получение списка соседей по столбцу      !!!     Оптимизировать поиск    !!!
    def col_call(self):
        for cell in Cell_list:
            if cell != self and cell.col == self.col and cell not in self.neighbours_list:
                self.neighbours_list.append(cell)

    # Попытка поиска значения в ячейке по простому алгоритму
    def cell_solve_1(self):
        """ Алгоритм основан на оценке не хватающих в квадрате/строке/столбце ячейках."""

        # Оценка значений в соседних ячейках.
        for cell in self.neighbours_list:
            if cell.value is not None and cell.value in self.eva_set:
                self.eva_set.remove(cell.value)
                self.neva_set.add(cell.value)

            # Если доступно только одно значение, значит оно и является решением для текущей ячейки.
            if len(self.eva_set) == 1:
                self.value = list(self.eva_set)[0]
                if not Variating:
                    self.validated = True
                if self in Nonlist:
                    Nonlist.remove(self)
                Val_dict[self.name] = self.value

    # Попытка поиска значения в ячейке по усложненному алгоритму, основанному на оценке невозможных для соседей
    # значений.
    def cell_solve_2(self):
        # ДЛЯ КВАДРАТА.
        self.my_square = Square.sq_o_dict[self.sq]  # Привязка квадрата.
        self.neva_sq_set_nei = self.eva_set

        # Проход по всем соседним по квадрату ячейкам.
        for cell in self.my_square.cell_list:
            if cell != self and cell.value is None:

                # Убираем из множества недоступных для соседей ячеек доступные для них ячейки.
                self.neva_sq_set_nei = self.neva_sq_set_nei - cell.eva_set

            # Если в цикле все ячейки уже убраны - нет смысла смотреть дальше.
            if len(self.neva_sq_set_nei) == 0:
                break

        # Если после выполнения цикла осталось только одно невозможное для соседей по квадрату значение …
        if len(self.neva_sq_set_nei) == 1:

            # … То именно оно и является значением текущей ячейки.
            self.value = list(self.neva_sq_set_nei)[0]
            if not Variating:
                self.validated = True
            if self in Nonlist:
                Nonlist.remove(self)
            Val_dict[self.name] = self.value

        # ДЛЯ СТРОКИ.
        if self.value is None:
            self.my_line = Line.ln_o_dict[self.line]  # Привязка строки.
            self.neva_ln_set_nei = self.eva_set

            # Проход по всем соседним по строке ячейкам.
            for cell in self.my_line.cell_list:
                if cell != self and cell.value is None:

                    # Убираем из множества недоступных для соседей ячеек доступные для них ячейки.
                    self.neva_ln_set_nei = self.neva_ln_set_nei - cell.eva_set

                # Если в цикле все ячейки уже убраны - нет смысла смотреть дальше.
                if len(self.neva_ln_set_nei) == 0:
                    break

            # Если после выполнения цикла осталось только одно невозможное для соседей по строке значение …
            if len(self.neva_ln_set_nei) == 1:

                # … То именно оно и является значением текущей ячейки.
                self.value = list(self.neva_ln_set_nei)[0]
                if not Variating:
                    self.validated = True
                if self in Nonlist:
                    Nonlist.remove(self)
                Val_dict[self.name] = self.value

        # ДЛЯ СТОЛБЦА.
        if self.value is None:
            self.my_column = Column.cl_o_dict[self.col]  # Привязка столбца.
            self.neva_cl_set_nei = self.eva_set

            # Проход по всем соседним по столбцу ячейкам.
            for cell in self.my_column.cell_list:
                if cell != self and cell.value is None:

                    # Убираем из множества недоступных для соседей ячеек доступные для них ячейки.
                    self.neva_cl_set_nei = self.neva_cl_set_nei - cell.eva_set

                # Если в цикле все ячейки уже убраны - нет смысла смотреть дальше.
                if len(self.neva_cl_set_nei) == 0:
                    break

            # Если после выполнения цикла осталось только одно невозможное для соседей по столбцу значение …
            if len(self.neva_cl_set_nei) == 1:

                # … То именно оно и является значением текущей ячейки.
                self.value = list(self.neva_cl_set_nei)[0]
                if not Variating:
                    self.validated = True
                if self in Nonlist:
                    Nonlist.remove(self)
                Val_dict[self.name] = self.value

    def error_check(self):
        if len(list(self.eva_set)) == 0:
            Error = True

class Square:
    """ Класс, отвечающий за оценку квадратов"""

    # Словарь для экземпляров квадратов.
    sq_o_dict = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}

    def __init__(self, number):

        #       !!!     Атрибуты    !!!
        self.number = number  # Номер квадрата.
        Square.sq_o_dict[number] = self
        self.eva_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # Доступные ячейки.
        self.cell_list = []  # Список ячеек в квадрате.

        #       !!! Методы  !!!

    # Добавление ячеек в список ячеек квадрата.
    def changing(self):
        for cell in Cell_list:
            if cell.sq == self.number:
                self.cell_list.append(cell)

                # Удаление доступных для квадрата значений, если они есть у его ячеек.
                if cell.value is not None and cell.value in self.eva_set:
                    self.eva_set.remove(cell.value)


class Line:
    """ Класс, отвечающий за оценку строк"""

    # Словарь для экземпляров строк.
    ln_o_dict = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}

    def __init__(self, number):

        #       !!!     Атрибуты    !!!
        self.number = number  # Номер строки.
        Line.ln_o_dict[number] = self
        self.eva_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # Доступные ячейки.
        self.cell_list = []  # Список ячеек в строке.

        #       !!! Методы  !!!

    # Добавление ячеек в список ячеек строки.
    def changing(self):
        for cell in Cell_list:
            if cell.line == self.number:
                self.cell_list.append(cell)

                # Удаление доступных для строки значений, если они есть у ее ячеек.
                if cell.value is not None and cell.value in self.eva_set:
                    self.eva_set.remove(cell.value)


class Column:
    """ Класс, отвечающий за оценку столбцов"""

    # Словарь для экземпляров столбцов.
    cl_o_dict = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: None}

    def __init__(self, number):

        #       !!!     Атрибуты    !!!
        self.number = number  # Номер столбца.
        Column.cl_o_dict[number] = self
        self.eva_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}  # Доступные ячейки.
        self.cell_list = []  # Список ячеек в строке.

        #       !!! Методы  !!!

    # Добавление ячеек в список ячеек столбца.
    def changing(self):
        for cell in Cell_list:
            if cell.col == self.number:
                self.cell_list.append(cell)

                # Удаление доступных для столбца значений, если они есть у ее ячеек.
                if cell.value is not None and cell.value in self.eva_set:
                    self.eva_set.remove(cell.value)

# Main()
