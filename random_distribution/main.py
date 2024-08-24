import random
import json
from munkres import Munkres

countOfStudents = 30
sumOfMiss_1 = 0
sumOfMiss_2 = 0


class Student:
    def __init__(self, name, choice, computedChoice):
        self.name = name
        self.choice = choice
        self.computedChoice = computedChoice

    def to_dict(self):
        return {
            "name": self.name,
            "choice": self.choice,
            "computedChoice": self.computedChoice
        }

    @staticmethod
    def from_dict(data):
        return Student(name=data["name"], choice=data["choice"], computedChoice=data["computedChoice"])

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return Student.from_dict(data)

    @staticmethod
    def students_to_json(students):
        dict_list = [student.to_dict() for student in students]
        return json.dumps(dict_list, indent=4)

    @staticmethod
    def students_from_json(json_str):
        dict_list = json.loads(json_str)
        return [Student.from_dict(data) for data in dict_list]


def initJson():
    arr = []
    for i in range(countOfStudents):
        arr.append(
            Student(str(i+1), random.randint(1, countOfStudents), 0))
    with open('input.json', 'w') as file:
        file.write(Student.students_to_json(arr))


def solve_with_custom():
    with open('input.json', 'r') as file:
        data = file.read()
    arr = Student.students_from_json(data)
    choicesSet = set(range(1, countOfStudents+1))
    numbersSet = set(range(1, countOfStudents+1))

    for i in range(0, countOfStudents):
        randomIndex = random.choice(list(numbersSet))
        tmp = getClosest(choicesSet, arr[randomIndex-1].choice)
        choicesSet.discard(tmp)
        numbersSet.discard(randomIndex)
        arr[randomIndex-1].computedChoice = tmp
    with open('output.json', 'w') as file:
        file.write(Student.students_to_json(arr))


def getClosest(choicesSet: set, choice: int):
    global sumOfMiss_1
    min = countOfStudents
    res = -1
    for i in choicesSet:
        if abs(choice - i) < min:
            min = choice - i
            res = i
    sumOfMiss_1 += abs(choice - res)
    return res


def solve_with_Munkres():
    m = Munkres()
    with open('input.json', 'r') as file:
        data = file.read()
    arr = Student.students_from_json(data)
    size = len(arr)
    matrix = []
    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[-1].append(abs(arr[i].choice-j-1))
    result = m.compute(matrix)
    global sumOfMiss_2
    for i in range(size):
        sumOfMiss_2 += abs(result[i][1] - arr[i].choice + 1)


for i in range(100):
    initJson()
    solve_with_custom()
    solve_with_Munkres()
print(sumOfMiss_1/2000)
print(sumOfMiss_2/2000)

