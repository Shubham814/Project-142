import csv

all = []

with open("articles.csv") as f:
    reader = csv.reader(f)
    data = list(reader)
    all = data[1:]

liked = []
unliked = []