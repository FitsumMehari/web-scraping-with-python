import requests

from bs4 import BeautifulSoup

root_link = 'https://www.airlinequality.com/airline-reviews/british-airways'

root_page = requests.get(root_link)

root_soup = BeautifulSoup(root_page.content, 'html.parser')

links = root_soup.find_all('a')

pagination_link = "airline-reviews/british-airways/page"
paginations = []

for link in links:
    
    if pagination_link in link.get('href'):
        paginations.append((link.get('href')))
    else: continue

last_page_link = paginations[len(paginations)-2].split('/')
last_page = last_page_link[-2]

print(last_page, "pages found on the website.")

# variables for the data of each page

not_recommended = 0
is_recommended = 0

business_class = 0
economy_class = 0
premium_economy = 0

solo_leisure = 0
business = 0
family_leisure = 0
couple_leisure = 0

for page_num in range(1, int(last_page)):
    print("\n\nGetting data from page", str(page_num), "...")

    r = requests.get(root_link+"/page/" + str(page_num))
    soup = BeautifulSoup(r.content, 'html.parser')

    # Now we get the ratings from each page

    reviews = soup.find_all('div', class_='text_content')

    ratings = soup.find_all('td')

    my_dict = {}

    for i in range(0, len(ratings)):
        if i == 0 or i % 2 == 0:
            if ratings[i].text in my_dict:
                my_dict[ratings[i].text].append(ratings[i + 1].text)
                continue
            my_dict[ratings[i].text] = [ratings[i + 1].text]

    if "Recommended" in my_dict:
        for answer in my_dict["Recommended"]:
            if answer == "no": not_recommended += 1
            elif answer == "yes": is_recommended += 1

    if "Seat Type" in my_dict:
        for answer in my_dict["Seat Type"]:
            if answer == "Business Class": business_class += 1
            elif answer == "Economy Class": economy_class += 1
            elif answer == "Premium Economy": premium_economy += 1

    if "Type Of Traveller" in my_dict:
        for answer in my_dict["Type Of Traveller"]:
            if answer == "Solo Leisure": solo_leisure += 1
            elif answer == "Business": business += 1
            elif answer == "Family Leisure": family_leisure += 1
            elif answer == "Couple Leisure": couple_leisure += 1

total_recommendations = is_recommended + not_recommended
total_passengers = premium_economy + business_class + economy_class
total_travellers = solo_leisure + business + family_leisure + couple_leisure
print("It is recommeded", is_recommended, "times, and it is not recommeded", not_recommended, "times out of", total_recommendations)
print("Premium Economy passengers are", premium_economy, ", Business Class passengers are ", business_class, ", and Economy Class passengers are ", economy_class, "out of", total_passengers)
print("Solo Leisure travellers are", solo_leisure, ", Business travellers are ", business, ", Family Leisure travellers are ", family_leisure, ", and Couple Leisure travellers are ", couple_leisure, "out of", total_travellers)