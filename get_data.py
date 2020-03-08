import json
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def file1(name):
    file = open(name, "r")
    dict = json.load(file)
    file.close()
    return [[k, v] for k, v in dict.items()]


def file2(name):
    file = open(name, "r")
    text = file.readlines()[0]
    file.close()
    pattern = r"(?<=\:).+?(?=\')"  # an alternative: https://stackoverflow.com/questions/9889635/regular-expression-to-return-all-characters-between-two-special-characters
    match = re.findall(pattern, text)
    res = []
    for i in range(0, len(match), 2):
        res.append([match[i][1:], match[i + 1][1:]])
    return res


def file3(name):
    file = open(name, "r")
    res = []
    for line in file:
        line2 = next(file, None)
        res.append([line[6:-1], line2[9:-1]])
    file.close()
    return res


def file4(name):
    file = open(name, "r")
    pattern1 = r".*(?=" + re.escape(",Purpose:") + ")"
    pattern2 = r"((?<=" + re.escape(",Purpose: ") + ").*)"
    res = []
    for line in file:
        if line != "\n":
            name = re.search(pattern1, line[6:]).group(0)
            purpose = re.search(pattern2, line[6:]).group(0)
            res.append([name, purpose])
    file.close()
    return res


def file5(name):
    file = open(name, "r")
    dict = json.load(file)
    file.close()
    res = []
    for item in dict:
        res.append([item["name"], item["purpose"]])
    return res


def file6(name):
    file = open(name, "r")
    res = []
    pattern1 = r"((?<=" + re.escape("Name: ") + ").*)"
    pattern2 = r"((?<=" + re.escape("Purpose: ") + ").*)"  # one line purpose
    pattern3 = r"((?<=" + re.escape("('Purpose: ") + ").*)"  # two line purpose
    for line in file:
        name = re.search(pattern1, line)
        line2 = next(file)
        purpose = re.search(pattern3, line2)
        if purpose is None:
            purpose = re.search(pattern2, line2).group(0)[:-1]
        else:
            purpose = purpose.group(0)[:-1] + next(file)[2:-3]
        res.append([name.group(0)[:-1], purpose])
    file.close()
    return res


def file7(name):
    file = open(name, "r")
    res = []
    for line in file:
        line2 = next(file, None)
        res.append([line[6:-1], line2[9:-1]])
    file.close()
    return res


def file8(name):
    """
    Assume first name assosciated with first purpose and so on
    """
    file = open(name, "r")
    res = []
    count = 0
    for line in file:
        if count < 50:  # names
            res.append([line[6:-1]])
        else:  # purposes
            res[count - 50].append(line[9:-1])
        count += 1
    file.close()
    return res


def file9(name):
    file = open(name, "r")
    res = []
    for line in file:
        pattern = r"((?<=" + re.escape(")") + ").*)"
        company = re.search(pattern, line).group(0)
        line2 = next(file)
        res.append([company, line2[2:-1]])
    file.close()
    return res


def file10(name):
    file = open(name, "r")
    res = []
    for line in file:
        line2 = next(file)
        next(file)  # skip blank lines
        res.append([line[6:-1], line2[9:-1]])
    file.close()
    return res


if __name__ == "__main__":
    master = (
        file1("data/Webscrp_company.txt")
        + file2("data/text_scrap.txt")
        + file3("data/result.txt")
        + file4("data/output_Webscrap_HW2.txt")
        + file5("data/output.json")
        + file6("data/name_purpose.txt")
        + file7("data/myfile.txt")
        + file8("data/foryou4.txt")
        + file9("data/Company.txt")
        + file10("data/595_HW2.txt")
    )

    mc = open("master_companies.txt", "w")
    text = ""
    for company in master:
        text = text + "Name: " + company[0] + "\nPurpose: " + company[1] + "\n"
    mc.write(text)
    mc.close()

    for company in master:
        getSentiment = SentimentIntensityAnalyzer()
        company.append(getSentiment.polarity_scores(company[1])["compound"])

    master_by_sentiment = sorted(master, key=lambda x: x[2])
    negative_companies = master_by_sentiment[0:10]
    positive_companies = master_by_sentiment[-10:]

    neg = open("negative.txt", "w")
    text = ""
    neg.write("10 Most Negative Companies" + "\n\n")
    for c in negative_companies:
        text = (
            text
            + "Name: "
            + c[0]
            + "\nPurpose: "
            + c[1]
            + "\nSentiment Score: "
            + str(c[2])
            + "\n\n"
        )
    neg.write(text)
    neg.close()

    pos = open("positive.txt", "w")
    pos.write("10 Most Positive Companies" + "\n\n")
    text = ""
    for c in reversed(positive_companies):
        text = (
            text
            + "Name: "
            + c[0]
            + "\nPurpose: "
            + c[1]
            + "\nSentiment Score: "
            + str(c[2])
            + "\n\n"
        )
    pos.write(text)
    pos.close()
