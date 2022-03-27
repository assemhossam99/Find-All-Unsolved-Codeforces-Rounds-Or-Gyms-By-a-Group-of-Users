import time
import os
from bs4 import BeautifulSoup
import requests

# Taking the handles of the users and storing them in a list
users_number = int(input('Please enter the number of users: '))
users = []
print('Please enter the users handles (one handle per each line): ')
for i in range(0, users_number):
    user = input()
    users.append(user)
print('')

# Search for contests or gyms
contest_or_gym = int(input('Do you want to search for codeforces rounds or gyms?\nEnter 1 for round, or 2 for gym: \n'))

# Storing the solved or tried problems from at least one user
solvedOrTried = set()
for user in users:
    print(f'Collecting solved problems of the user ({user})')
    pagination = requests.get(f'https://codeforces.com/submissions/{user}/page/1').text
    soup = BeautifulSoup(pagination, 'lxml')
    manyPages = soup.find_all('span', class_='page-index')
    number_of_pages = 0
    if len(manyPages) == 0:
        number_of_pages = 1
    else:
        number_of_pages = int(manyPages[-1].text)
    number_of_pages += 1
    # iterate over the pages of submissions of the user
    for page in range(1, number_of_pages):
        print(f'Collecting solved Problems for user {user}...{int((page * 100) / number_of_pages)}%')
        html = requests.get(f'https://codeforces.com/submissions/{user}/page/{page}').text
        soup = BeautifulSoup(html, 'lxml')
        submissions = soup.find_all('td')

        #iterate over user's submissions in the current page
        for idx, submission in enumerate(submissions):
            if idx % 8 == 3:
                problem_number = ''
                problem = str(submission.a['href'])
                while problem[-1] is not '/':
                    problem = problem[:-1]
                for c in problem:
                    if c >= '0' and c <= '9':
                        problem_number += c
                solvedOrTried.add(problem_number)
    print(f'Done collecting ({user}) solved problems')
    print('')
# done adding problems of all users

output_contests = []

# find contests
if contest_or_gym == 1:
    pagination = requests.get(f'https://codeforces.com/contests/page/1').text
    soup = BeautifulSoup(pagination, 'lxml')
    manyPages = soup.find_all('span', class_='page-index')
    number_of_pages = int(manyPages[-1].text)
    number_of_pages += 1
    for page in range(1, number_of_pages):
        print(f'Finding the unsolved rounds .. {int((page * 100) / number_of_pages)}%')
        html = requests.get(f'https://codeforces.com/contests/page/{page}').text
        soup = BeautifulSoup(html, 'lxml')
        contest_table = soup.find('div', class_='contests-table')
        contests_data = contest_table.find_all('td')
        for idx, contest in enumerate(contests_data):
            if idx % 6 == 0:
                contest_link = contest.a['href']
                contest_id = ''
                for c in contest_link:
                    if c <= '9' and c >= '0':
                        contest_id += c
                if contest_id not in solvedOrTried:
                    output_contests.append(contest_link)

# find gyms
elif contest_or_gym == 2:
    pagination = requests.get(f'https://codeforces.com/contests/page/1').text
    soup = BeautifulSoup(pagination, 'lxml')
    manyPages = soup.find_all('span', class_='page-index')
    number_of_pages = int(manyPages[-1].text)
    number_of_pages += 1
    for page in range(1, number_of_pages):
        print(f'Finding the unsolved gyms .. {int((page * 100) / number_of_pages)}%')
        html = requests.get(f'https://codeforces.com/gyms/page/{page}').text
        soup = BeautifulSoup(html, 'lxml')
        contest_table = soup.find('div', class_='contests-table')
        contests_data = contest_table.find_all('td')
        for idx, contest in enumerate(contests_data):
            if idx % 5 == 0:
                contest_link = contest.a['href']
                contest_id = ''
                for c in contest_link:
                    if c <= '9' and c >= '0':
                        contest_id += c
                if contest_id not in solvedOrTried:
                    output_contests.append(contest_link)

else:
    print('Your choice is not valid.')
    exit()
# save all the contests
number_of_saved_contests = 0
with open(f'Contests.txt', 'w') as f:
    for cur_contest in output_contests:
        number_of_saved_contests += 1
        f.write(f'https://codeforces.com{cur_contest}')
        f.write('\n')
        f.write('\n')

print(f'{number_of_saved_contests} contests successfully saved to the file.')