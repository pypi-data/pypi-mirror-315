# project_func/cli.py


def welcome():
    print("Первая попытка запустить проект!")
    print("***")

    while True:
        command = input("Введите команду: ").strip().lower()

        if command == "exit":
            print("Выход из программы.")
            break
        elif command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        else:
            print("Неизвестная команда. Введите 'help' для справки.")


if __name__ == "__main__":
    welcome()
