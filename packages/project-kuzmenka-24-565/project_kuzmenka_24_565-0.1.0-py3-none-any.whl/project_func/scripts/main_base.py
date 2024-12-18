# project_func/scripts/main_base.py
# !/usr/bin/env python3


from project_func.scripts.cli import welcome


def main():
    print('>>>poetry run python -m project_func.scripts.main_base')
    print('Первая попытка запустить проект!!!!')
    welcome()


if __name__ == "__main__":
    main()
