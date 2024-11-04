# Практическое задание №4. Системы контроля версий

П.Н. Советов, РТУ МИРЭА

Работа с Git.

## Задача 1

На сайте https://onlywei.github.io/explain-git-with-d3 или http://git-school.github.io/visualizing-git/ (цвета могут отличаться, есть команды undo/redo) с помощью команд эмулятора git получить следующее состояние проекта (сливаем master с first, перебазируем second на master): см. картинку ниже. Прислать свою картинку.

![image](https://github.com/user-attachments/assets/a30846f0-f7f9-4aaf-aa22-6e7bd336ff2e)

## Решение:
```
git commit
git tag in
git branch first
git branch second
git commit
git commit
git checkout first
git commit
git commit
git checkout master
git merge first
git checkout second
git commit
git commit
git rebase master
git checkout master
git merge second
git checkout in
```

## Результат:

![Снимок экрана 2024-11-01 134805](https://github.com/user-attachments/assets/0242718c-5291-422f-9c34-9acff5d4d0db)

## Задача 2

Создать локальный git-репозиторий. Задать свои имя и почту (далее – coder1). Разместить файл prog.py с какими-нибудь данными. Прислать в текстовом виде диалог с git.

## Решение:

```
git init
git config user.name "coder1"
git config user.email "coder1@example.com"
echo print("Hello, World!") > prog.py
git add prog.py
git commit -m "first commit"
```

## Результат:

![image](https://github.com/user-attachments/assets/50b9da51-b4f5-4415-a81f-8a8f7634df73)

```
Microsoft Windows [Version 10.0.22631.4317]
(c) Корпорация Майкрософт (Microsoft Corporation). Все права защищены.

D:\repository>git init
Initialized empty Git repository in D:/repository/.git/

D:\repository>git config user.name "coder1"

D:\repository>git config user.email "coder1@example.com"

D:\repository>echo print("Hello, World!") > prog.py

D:\repository>git add prog.py

D:\repository>git commit -m "first commit"
[master (root-commit) ac451ff] first commit
 1 file changed, 1 insertion(+)
 create mode 100644 prog.py

D:\repository>git status
On branch master
nothing to commit, working tree clean

D:\repository>git log
commit ac451ff5ac0ed504be56e6d2d4b743bb7977b46d (HEAD -> master)
Author: coder1 <coder1@example.com>
Date:   Mon Nov 4 03:59:01 2024 +0300

    first commit

D:\repository>
```

## Задача 3

Создать рядом с локальным репозиторием bare-репозиторий с именем server. Загрузить туда содержимое локального репозитория. Команда git remote -v должна выдать информацию о server! Синхронизировать coder1 с server.

Клонировать репозиторий server в отдельной папке. Задать для работы с ним произвольные данные пользователя и почты (далее – coder2). Добавить файл readme.md с описанием программы. Обновить сервер.

Coder1 получает актуальные данные с сервера. Добавляет в readme в раздел об авторах свою информацию и обновляет сервер.

Coder2 добавляет в readme в раздел об авторах свою информацию и решает вопрос с конфликтами.

Прислать список набранных команд и содержимое git log.

Пример лога коммитов:

```
*   commit a457d748f0dab75b4c642e964172887de3ef4e3e
|\  Merge: 48ce283 d731ba8
| | Author: Coder 2 <coder2@corp.com>
| | Date:   Sun Oct 11 11:27:09 2020 +0300
| | 
| |     readme fix
| | 
| * commit d731ba84014d603384cc3287a8ea9062dbb92303
| | Author: Coder 1 <coder1@corp.com>
| | Date:   Sun Oct 11 11:22:52 2020 +0300
| | 
| |     coder 1 info
| | 
* | commit 48ce28336e6b3b983cbd6323500af8ec598626f1
|/  Author: Coder 2 <coder2@corp.com>
|   Date:   Sun Oct 11 11:24:00 2020 +0300
|   
|       coder 2 info
| 
* commit ba9dfe9cb24316694808a347e8c36f8383d81bbe
| Author: Coder 2 <coder2@corp.com>
| Date:   Sun Oct 11 11:21:26 2020 +0300
| 
|     docs
| 
* commit 227d84c89e60e09eebbce6c0b94b41004a4541a4
  Author: Coder 1 <coder1@corp.com>
  Date:   Sun Oct 11 11:11:46 2020 +0300
  
      first commit
```

## Решение:

```
git init
git config user.name "coder1"
git config user.email "coder1@example.com"
echo print("Hello, World!") > prog.py
git add prog.py
git commit -m "first commit"

cd D:\repository
git init --bare server

git remote add server D:\repository\server
git remote -v

git push server master

git clone D:\repository\server D:\repository\client
cd D:\repository\client
git config user.name "coder2"
git config user.email "coder2@example.com"

echo "Author Information:" > readme.md
git add readme.md
git commit -m "docs"

git remote rename origin server

git push server master

cd D:\repository
git pull server master

echo "Author: coder1" >> readme.md
git add readme.md
git commit -m "coder1 info"
git push server master

cd D:\repository\client
echo "Author: coder2" >> readme.md
git add readme.md
git commit -m "coder2 info"
git push server master

git pull server master

git add readme.md
git commit -m "readme fix"
git push server master

cd ..
cd server
git log -n 5 --graph --decorate --all
```

## Результат:

![image](https://github.com/user-attachments/assets/6410560b-5f35-49f9-a28d-d22363a4f2bb)

```
D:\repository\server>git log -n 5 --graph --decorate --all
*   commit 73a4759924d3c8f2ab582bd8f29a9e8b1fea1a78 (HEAD -> master)
|\  Merge: 8ebc7c1 b5f90b0
| | Author: coder2 <coder2@example.com>
| | Date:   Mon Nov 4 04:07:50 2024 +0300
| |
| |     readme fix
| |
| * commit b5f90b095e4917283fe8b96817ee606d812ff24a
| | Author: coder1 <coder1@example.com>
| | Date:   Mon Nov 4 04:06:06 2024 +0300
| |
| |     coder1 info
| |
* | commit 8ebc7c186983e9a5504a3e1bae035bd994fba577
|/  Author: coder2 <coder2@example.com>
|   Date:   Mon Nov 4 04:06:33 2024 +0300
|
|       coder2 info
|
* commit 0b8d1714592eac8dcb8bd4b165aa43fe58741c04
| Author: coder2 <coder2@example.com>
| Date:   Mon Nov 4 04:03:46 2024 +0300
|
|     docs
|
* commit ac451ff5ac0ed504be56e6d2d4b743bb7977b46d
  Author: coder1 <coder1@example.com>
  Date:   Mon Nov 4 03:59:01 2024 +0300

      first commit

D:\repository\server>
```

## Задача 4

Написать программу на Питоне (или другом ЯП), которая выводит список содержимого всех объектов репозитория. Воспользоваться командой "git cat-file -p". Идеальное решение – не использовать иных сторонних команд и библиотек для работы с git.

## Решение:
```

```

## Результат:

## Полезные ссылки

Git

Учебник (рус.): https://git-scm.com/book/ru/v2

Шпаргалка (рус.): https://training.github.com/downloads/ru/github-git-cheat-sheet/

Официальная документация: https://git-scm.com/docs

Эксцентричный доклад Л. Торвальдса о Git: https://www.youtube.com/watch?v=4XpnKHJAok8

Дерево Меркла: http://cryptowiki.net/index.php?title=Дерево_Merkle

Git for Windows: https://git-scm.com/download/win

Репозиторий chibicc: https://github.com/rui314/chibicc.git

Игра по git: https://learngitbranching.js.org/?locale=ru_RU

SHA-1

Описание алгоритма: https://ru.wikipedia.org/wiki/SHA-1

Вероятность хеш-коллизии: https://preshing.com/20110504/hash-collision-probabilities/

https://ru.m.wikipedia.org/wiki/Парадокс_дней_рождения

https://security.googleblog.com/2017/02/announcing-first-sha1-collision.html
