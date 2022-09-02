# -*- coding: utf-8 -*-

# This script generates the pokedex based by parsing Bulbapedia data.
# Scraping received 403, so I manually extracted the single html page.
# NOTES - Processing Nidoran♂ and Nidoran♀, and Farfetch'd helped understand how character encoding works and how specific json formatting is.
from pokedex_html import html
from bs4 import BeautifulSoup

# This was manually extracted from 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_catch_rate'
parsed_text = BeautifulSoup(html, 'html.parser').get_text().split()

# Get ranges to parse off of
index_range = []
for item in parsed_text:
    if item == '001':
        index_range.append(parsed_text.index(item))
    elif item == '151':
        index_range.append(parsed_text.index(item) + 3)
# index_range is now populated with 622 & 1079

data_list = parsed_text[index_range[0]:index_range[-1]]
normalized_list = []
for i in range(0, len(data_list), 3):
    if 'Partner' not in data_list[i:i + 3][1]:
        normalized_list.append(data_list[i:i + 3])

# Creates json code and saves it in assets directory as pokedex.json
content = ''
content += '{\n'
for item in normalized_list:
    number = int(item[0])
    name = item[1]
    catch_rate = int(item[2])
    base_flee = int(125 - catch_rate / 255 * 100)
    if base_flee > 100:
        baited_flee = 2
    else:
        baited_flee = 1

    if base_flee == 25:
        angered_flee = 2
    elif 25 < base_flee <= 50:
        angered_flee = 6
    elif 50 < base_flee <= 75:
        angered_flee = 10
    elif 75 < base_flee <= 100:
        angered_flee = 14
    else:
        angered_flee = 18

    if number != 151:
        content += '\t\"{}\":{{\n\t\t\"pokemon_name\":\"{}\",\n\t\t\"pokedex_number\":{},\n\t\t\"catch_rate\":{},\n\t\t\"base_flee\":{},\n\t\t\"baited_flee\":{},\n\t\t\"angered_flee\":{}\n\t}},\n'.format(name,name, number, catch_rate, base_flee,baited_flee,angered_flee)
    else:
        content += '\t\"{}\":{{\n\t\t\"pokemon_name\":\"{}\",\n\t\t\"pokedex_number\":{},\n\t\t\"catch_rate\":{},\n\t\t\"base_flee\":125,\n\t\t\"baited_flee\":{},\n\t\t\"angered_flee\":{}\n\t}}\n}}\n'.format(name,name, number, catch_rate,baited_flee,angered_flee)

print(content)
with open('..\\assets\\pokedex.json','w',encoding='utf-8') as output_file:
    output_file.write(content)