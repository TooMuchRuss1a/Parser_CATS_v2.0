import streamlit as st
import pandas as pd
import urllib.request
import re

st.set_page_config(page_title="CatsParser_PIE",
                   page_icon=":rocket:",
                   # layout= "wide"
                   )

st.title("Б9121-09.03.03пиэ")

with st.spinner('Работаем...'):

    f = urllib.request.urlopen("https://imcs.dvfu.ru/cats/?f=rank_table_content;cache=1;cid=5398025;clist=5398025;hide_virtual=1").read()
    f = f.decode("utf8")

    group = [
"Бабинцева Алина Павловна",
"Баздуков Валентин Александрович",
"Баков Артём Николаевич",
"Бирюков Данил Александрович",
"Бирюков Игорь Сергеевич",
"Богинский Денис Анатольевич",
"Борденюк Анастасия Денисовна",
"Борсук Дмитрий Денисович",
"Бортников Сергей Вячеславович",
"Будникова Елена Романовна",
"Волкова Мария Владимировна",
"Галаганов Никита Сергеевич",
"Гарунов Даниил Алексеевич",
"Гельман Анатолий Олегович",
"Глушак Валерия Евгеньевна",
"Гомбоев Зандан Зоригтоевич",
"Григорьева Софья Васильевна",
"Григурко Андрей Сергеевич",
"Давыденко Максим Дмитриевич",
"Демьянов Виктор Витальевич",
"Ермак-Ермашко Алексей Алексеевич",
"Иванов Дмитрий Владимирович",
"Ивашев Тимофей Дмитриевич",
"Игнатьев Павел Егорович",
"Исаков Елисей Николаевич",
"Калашников Андрей Владимирович",
"Карагодин Максим Дмитриевич",
"Киптилов Никита Сергеевич",
"Клещёв Савелий Васильевич",
"Константинов Эдуард Александрович",
"Кошельков Иван Владимирович",
"Кривогин Алексей Олегович",
"Кузьмина Наталия Александровна",
"Легков Алексей Романович",
"Лу Яньтин",
"Лукьянец Евгений Сергеевич",
"Мациева Анна Магомедовна",
"Меркушев Игорь Евгеньевич",
"Миронов Борис Олегович",
"Михайлов Сергей Сергеевич",
"Михайлова Камила Александровна",
"Окольникова Александра Павловна",
"Олийник Дарья Александровна",
"Петров Юрий Святославович",
"Платонов Вячеслав Дмитриевич",
"Попович Александр Русланович",
"Пяк Денис Сергеевич",
"Реутова Любовь Алексеевна",
"Романов Александр Александрович",
"Рыбаков Никита Андреевич",
"Семишова Анна Григорьевна",
"Симаненков Иван Андреевич",
"Скрипальщиков Семён Игоревич",
"Сокирка Артём Владимирович",
"Соломоненко Алексей Александрович",
"Тарбаев Тимур Саянович",
"Топоева Милена Яковлевна",
"Трушникова Анжелика Витальевна",
"Туровец Владислав Юрьевич",
"Ферулев Александр Николаевич",
"Хазыгалиев Артемий Валерьевич",
"Холод Ирина Владимировна",
"Хоменко Данила Антонович",
"Чернятьев Никита Сергеевич",
"Шашкова Наталия Евгениевна",
"Шварц Анжелика Александровна",
"Янович Яков Валерьевич"
]

    gsheetid = "1FiFjESIA7lY3zSY65wHnY-7BdAVhQoIEaDX7N_ycV-g"
    sheet_name = "%D0%919121-09.03.03%D0%BF%D0%B8%D1%8D"
    gsheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, sheet_name)
    sheet = pd.read_csv(gsheet_url)
    sheet = sheet[['Unnamed: 18']]

    name = (re.findall(r'(?<=n: ")(.*)(?=", fl)',f))
    score = (re.findall(r'(?<=ts: )(.*)(?=, ttm:)',f))
    nameclear = []
    groupclear = []
    NAME = []
    SCORE = []
    RATING = []
    DATA = []
    ID = []
    ZACHET = []
    MARK = []
    k=0

    for i in range(2, len(group)+2):
        if (str(sheet.values[i]) == "[nan]") or ((str(int(sheet.values[i])) == "2")):
            ZACHET.append("НЕЗАЧЕТ")
        else:
            ZACHET.append(str(int(sheet.values[i])))

    for i in range(0, len(group)):
        groupclear.append(re.sub(' ', '', group[i]))
    for i in range(0, len(name)):
        nameclear.append(re.sub(' ', '', name[i]))
        if nameclear[i] in groupclear:
            k+=1
            RATING.append(str(i + 1))
            NAME.append(name[i])
            SCORE.append(score[i])

    for i in range(0, len(group)):
        if groupclear[i] not in nameclear:
            RATING.append("N/A")
            NAME.append(group[i])
            SCORE.append("0")

    for i in range(0, len(NAME)):
        for k in range(0, len(group)):

            if (re.sub(' ', '', group[k]) == re.sub(' ', '', NAME[i])):
                MARK.append(ZACHET[k])

    for i in range(0, len(NAME)):
        DATA.append([RATING[i], NAME[i], SCORE[i], MARK[i]])
        ID.append(i+1)

######################################################
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden; }
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)
#####################################################

    df = pd.DataFrame(
        DATA,
        columns=['РЕЙТИНГ', 'ФИО', 'РЕШЕНО', 'ОЦЕНКА'],
        index=ID
    )

st.success('Готово!')


st.table(df)
st.caption('@toomuchrussia')
