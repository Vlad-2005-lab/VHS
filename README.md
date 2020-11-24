# VSN
# Социальная сеть
Название проекта - VSN(Vlad's Social Network)

Авторы проекта - Казанцев Владислав (8 класс, 2-ой курс Яндекс.Лицея, город Тюмень), Аниканов Владислав (8 класс, 2-ой курс Яндекс.Лицея, город Тюмень)

Идея проекта заключается в создании простой в использовании и рабочей социальной сети. Сначала надо зайти и зарегистрироваться, указав при этом фамилию, имя, возраст. Далее идёт проверка почты, а потом авторизация (если вы уже зарегистрированы, то сразу авторизация). В проекте есть возможность выкладывать новости, изображения и видео. Также вы можете просматривать новости других пользователей, их основную информацию и искать их видео. Основная возможность это общение с людьми, то есть в проекте присутсвуют переписки.

[Фото](https://github.com/Vlad-2005-lab/VHS/raw/master/photos/photo1.png)

[Фото](https://github.com/Vlad-2005-lab/VHS/raw/master/photos/photo2.png)


Реализация состоит из двух частей - backend и frontend. Backend полностью писался на python, его структура содержит классы для выполнения различныхх задач (отправка сообщений, создание новостей и т.д.) и функций для передачи информации в frontend. Frontend же реализован на html, то есть все странички, то что мы видим, всё на html.

[Фото](https://github.com/Vlad-2005-lab/VHS/raw/master/photos/photo3.png)

[Фото](https://github.com/Vlad-2005-lab/VHS/raw/master/photos/photo4.png)


В проекте использовались библиотеки flask (взаимодействие с frontend-ом), flask-wtf (WTForms), sqlalchemy (взаимодействие с базой данных), datetime (для даты и времени отправки сообщений), os (проверка существования путей), pillow (сохранение изображений), smtplib (отправка писем на почту)

[Фото](https://github.com/Vlad-2005-lab/VHS/raw/master/photos/photo5.png)
