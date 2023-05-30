import csv

all_articles = []
liked_articles = []
unliked_articles = []

with open("articles.csv", encoding = 'utf8') as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]