# USE AT YOUR OWN RISK
# pip install tika
# pip install wordcloud
from tika import parser
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# read PDF, download from https://www.stsci.edu/jwst/science-execution/approved-programs/general-observers/cycle-4-go
raw = parser.from_file('jwst.pdf')

# loop to skip some garbage
doc = []
for d in raw['content'].split("\n"):
    if d.strip() == "":
        continue
    if "2025-" in d:
        continue
    skip = False
    for b in ["Program", "PI", "ID", "Principal", "Proposal", "Alternate", "Scientific category", "category", "abstract"]:
        if d.strip().lower().startswith(b.lower()):
            skip = True
            break
    if skip:
        continue
    doc.append(d)

# back to single string
text = " ".join(doc)

# remove double spaces
while "  " in text:
    text = text.replace("  ", " ")

# remove punctuation
for p in ".,!?'-;:_)([]><":
    text = text.replace(p, "")

# everything is lower case
text = text.lower()

# count words
count = Counter(text.split(" "))

# select words to be removed
remove = "can a at an than the to and of in with is this will for that we by as have its these from are on which our be".split()
remove += "abstract while their but into between they has only over also where other or one two three".split()
remove += "however such both more all would within us thus if may use due how it not ii iii".split()

count = {k: v for k, v in count.items() if k not in remove}

# remove single characters
count = {k: v for k, v in count.items() if len(k) > 1}

# check if number
def is_number(x):
    try:
        float(x)
        return True
    except:
        return False

count = {k: v for k, v in count.items() if not is_number(k)}

wds = sorted([[k, v] for k, v in count.items()], key=lambda x:x[1])[::-1]

for w in wds:
    c = count[w[0]]
    if c < 1:
        continue
    print(w[0].ljust(50), c)


# now plot
fig = plt.figure(figsize=(10, 10))
# remove margins
fig.subplots_adjust(bottom=0, top=1, left=0, right=1)

# generate cloud
wordcloud = WordCloud(width=1000, height=1000, include_numbers=False, repeat=False).generate_from_frequencies(count)

# plot cloud
plt.imshow(wordcloud, interpolation='bilinear')

# no axis
plt.axis("off")

# save and show
plt.savefig("cloud.png")
plt.show()
