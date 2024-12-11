##Line-clipp-app

Данное приложение на Python с использованием библиотеки Tkinter иллюстрирует работу алгоритмов отсечения отрезков и многоугольников. Целью данной работы является закрепление теоретического материала и практическое освоение основных методов и алгоритмов отсечения.
Формат входного файла

###Программа принимает входной файл с данными в следующем формате:
```bash
n *число отрезков*
X1_1 Y1_1 X2_1 Y2_1
X1_2 Y1_2 X2_2 Y2_2
…
X1_n Y1_n X2_n Y2_n *координаты отрезков*
Xmin Ymin Xmax Ymax *координаты отсекающего прямоугольного окна*
```
###Требования

1.Вывести систему координат (в соответствующем масштабе).
2.Отобразить отсекающее окно одним цветом, исходные отрезки (многоугольники) – другим цветом.
3.Выполнить отсечение соответствующими алгоритмами.
4.Визуализировать видимые части отрезков (многоугольников).

###Алгоритмы
####Алгоритм Сазерленда-Коэна

Данный алгоритм используется для отсечения отрезков относительно прямоугольного окна. Он основан на кодировании концов отрезков и определении, видны ли они относительно окна.
Алгоритм отсечения отрезков выпуклым многоугольником

Этот алгоритм позволяет отсекать отрезки относительно произвольного выпуклого многоугольника, определяя, какие части отрезков попадают внутрь многоугольника.
Установка

Убедитесь, что у вас установлен Python версии 3.7 или выше.
Установите необходимые зависимости:
```bash
pip install tkinter
```
###Использование

Сохраните код в файл, например clipping_app.py.
Запустите приложение:
```bash
python clipping_app.py
```
###Шаги использования

1.Загрузите входной файл с данными о отрезках и координатах отсекающего окна.
2.Программа визуализирует систему координат, отсекающее окно и отрезки.
3.Выполняется отсечение, и видимые части отрезков отображаются на экране.

###Пример входного файла

```bash
3
100 100 300 300
150 50 250 350
50 200 350 200
100 100 250 250
```
###Обратная связь

Если у вас возникли вопросы, предложения или вы обнаружили ошибку, пожалуйста, свяжитесь с разработчиком:

Email: 2709400@gmail.com
GitHub: [Pechenka6]

Лицензия

Этот проект распространяется под лицензией MIT. Вы можете свободно использовать, изменять и распространять код в соответствии с условиями лицензии.
