Пациенты делятся на 2 типа: первичные и повторные

Тем, кто приходит к нам в первый раз — мы сейчас отправляем сообщение:

> **Здравствуйте! Вчера вы были на первичном приёме у врача-косметолога в нашей клинике. Пожалуйста, уделите 2 минуты и поделитесь впечатлением о приёме. Это анонимно.Ссылка: ""


По ссылке анкета, где есть вопросы, которые нам важны для того, чтобы первичный прием был вау, и пациент пришел повторно.


Откуда брать данные?

Врачи и администраторы ведут записи в сервисе Medesk. Это медицинская информационная система. Там все приёмы, пациенты и тд.

Логика такая

- Берем из Medesk список приёмов за вчера
- Фильтруем тех, кто был на первичном приёме
- Проверяем наличие тега BAD (это чтобы не писать неугодным)
- И делаем рассылку в WhatsApp
- Присылаем отчет о рассылке



Как работать с Medesk:

У него нет API. И это боль. Обещают допилить уже который год, но никак не могут.

Но есть выгрузка через вебхуки. 



Как работаем с WhatsApp?

API в WhatsAppe по сути нет. Есть для бизнес-аккаунтов, но там свои сложности. Мы работаем на обычном аккаунте.

Но это супер популярный инструмент, поэтому чтобы с ним как-то работать — разные разработчики пилят сервисы. По сути это эмуляторы, которые оборачивают в сервисы и вешают на них API. Один из таких сервисов — Pact.im. С ним мы и работаем. 

Через него можно отправлять сообщения по WhatsApp с нашего рабочего номера. Отправил команду — улетело сообщение. 

У него есть своя документация по тому как работать с ним. На сайте можешь у них найти. В целом там не сложно. По сути всего один метод тебе понадобится для этого. 

И чтобы обращаться к нему потребуется токен и ID компании



Куда и как присылаем отчет по рассылке?

Все уведомления, и в целом все рабочие процессы, мы ведем в Telegram. Соответственно, все уведомления тоже приходят туда. 

Есть специально созаднный для этого бот, его зовут Гиппократ) к нему точно также обращаться нужно с использованием токена
