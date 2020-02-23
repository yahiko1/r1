import re

fruits = {'яблуко': 0,
          'груша': 0,
          'банан': 0,
          'апельсин': 0,
          'мандарин': 0,
          'фрукти': 0}
operations = {"з'їв": [],
              'забрав': [],
              'поклав': [],
              'залишилось': []}
question1 = """На столі було 10 апельсинів та 3 груші та 4 апельсини та 8 бананів, 1 мандарина та 2 яблука та 1 банан. 
Хлопчик з'їв 3 апельсини, 6 апельсин та 1 грушу, поклав 2 груші та забрав 1 мандарину, з'їв 1 яблуко та поклав 5 бананів. 
Скільки всього фруктів залишилось на столі?
Скыльки апельсиныв з'їв хлопчик?"""
question2 = """3 апельсини 5 яблук, 10 мандарин та 4 олівці лежали на столі. Хлопчик з'їв 4 мандарини та 2 апельсини. 
Скільки всього фруктів з'їв хлопчик? 
Скільки залишилось мандарин на столі? """
questionarie = [question1, question2]


def set_initial_data(first_sent):
    for f in fruits:
        f_shorted = f[:len(f) - 1]
        match_list = re.findall('[0-9]+ ' + f_shorted, first_sent)
        if match_list:
            for point in match_list:
                fruits[f] += int(re.findall('[0-9]+', point)[0])
                fruits['фрукти'] += int(re.findall('[0-9]+', point)[0])


def make_moves(second_sent):
    for op in operations:

        ss = second_sent
        ms_list = []

        ms = re.search(' ' + op, ss)
        if ms is not None:
            while ms is not None:
                ms_list.append(ms)
                ss = ss.replace(ms.group(), ' ', 1)
                ms = re.search(op, ss)

        for i in range(len(ms_list)):
            pos = ms_list[i].end()
            sent_in_words = second_sent[pos + (len(ms_list[i].group()) * i):len(second_sent)].split(' ')
            for w in sent_in_words:
                if w in operations:
                    break
                for f in fruits:
                    f_shorted = f[:len(f) - 1]
                    if re.search(f_shorted, w):
                        operations[op].append([f, int(sent_in_words[sent_in_words.index(w)-1])])
                        if op == "з'їв" or op == 'забрав':
                            fruits[f] -= int(sent_in_words[sent_in_words.index(w)-1])
                            fruits['фрукти'] -= int(sent_in_words[sent_in_words.index(w)-1])
                        else:
                            fruits[f] += int(sent_in_words[sent_in_words.index(w)-1])
                            fruits['фрукти'] += int(sent_in_words[sent_in_words.index(w)-1])
    for key, value in fruits.items():
        operations['залишилось'].append([key, value])


def make_answer(questions):
    answer_list = []

    for sent in questions:
        answer = ''
        number = 0
        sent = sent.lstrip()
        s = sent.split(' ')
        # if s[0] == 'Скільки' and s[0] != '\nСкільки':
        #     raise AttributeError
        for op in operations:
            op_match = re.search(' ' + op + ' ', sent)
            if op_match:
                if re.search('хлопчик', sent):
                    answer += 'Хлопчик'
                elif re.search('на столі', sent):
                    answer += 'Нa столі'
                answer += op_match.group()
                for f in fruits:
                    f_shorted = f[:len(f) - 1]
                    f_match = re.search(f_shorted, sent)
                    if f_match:
                        moves = operations[op]
                        for m in moves:
                            if f == 'фрукти' and op != 'залишилось':
                                number += m[1]
                            else:
                                if m[0] == f:
                                    number += m[1]
                        answer += str(number)
                        answer += ' '
                        answer += f
                        answer += '.'

        answer_list.append(answer)

    return answer_list


def play(question=str()):

    print('Task: ')
    print(question)
    q_in_sent = question.split('.')
    set_initial_data(q_in_sent[0])
    print('\nfruits status after initialization: ')
    print(fruits)
    make_moves(q_in_sent[1])
    print('\nlist of operations: ')
    print(operations)
    print('\nfruits status after manipulations: ')
    print(fruits)
    questions = q_in_sent[2].split('?')
    answers = make_answer(questions)
    print('\nAnswers: ')
    for i in range(len(answers)-1):
        print(str(i + 1) + '. ' + questions[i] + '\n' + answers[i])
    print("________________________________________________________\n\n")


#play(question1)


def interface():
    inp = -1
    print("""Hi! Here we can solve some easy child mathematics.\nYou can chose prepared task or write your own. 
But be careful we can deal only with specifically designed tasks.""")
    while True:
        print('------------------------------')
        print("Tasks:")
        i = 0
        for q in questionarie:
            print('\n' + str(i) + '. ' + q)
            i += 1
        print('\n\nType number of question to solve prepared one, or type -1 to write you own. Type -2 to leave.')
        inp = input()
        if inp == -1:
            qw = input()
            play(qw)
        elif inp == -2:
            break
        else:
            play(questionarie[int(inp)])
        for key, value in fruits.items():
            fruits[key] = 0
        for key, value in operations.items():
            operations[key] = []

interface()
