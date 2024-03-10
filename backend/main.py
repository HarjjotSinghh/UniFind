# from bs4 import BeautifulSoup
# import json

# def extract_table_data(html_file):
#     """Extracts data from the HTML table and converts it into a list of JSON objects."""

#     with open(html_file, "r", encoding="utf-8") as f:
#         html_content = f.read()

#     soup = BeautifulSoup(html_content, "html.parser")
#     tables_rows = soup.find_all(class_="table-row")  # get all tables rows
#     print(tables_rows)
# if __name__ == "__main__":
#     extract_table_data("./site.html")

# V1
# from bs4 import BeautifulSoup
# import json

# def extract_table_data(html_file):
#     """Extracts data from the HTML table and converts it into a list of JSON objects."""
#     result = []

#     with open(html_file, "r", encoding="utf-8") as f:
#         html_content = f.read()

#     soup = BeautifulSoup(html_content, "html.parser")
#     tables_rows = soup.find_all(class_="table-row")  # get all tables rows

#     for row in tables_rows:
#         rank_td = row.find("td", class_="font-weight-medium")
#         rank = rank_td.get_text(strip=True) if rank_td else None

#         college_name_h3 = row.find("h3", class_="font-weight-medium")
#         college_name = college_name_h3.get_text(strip=True) if college_name_h3 else None

#         location_span = row.find("span", class_="location")
#         location = location_span.get_text(strip=True) if location_span else None

#         fees_span = row.find("span", class_="text-lg text-green")
#         fees = fees_span.get_text(strip=True) if fees_span else None

#         reviews_span = row.find("span", class_="text-lg text-primary")
#         reviews = reviews_span.get_text(strip=True) if reviews_span else None

#         json_object = {
#             "rank": rank,
#             "college_name": college_name,
#             "location": location,
#             "fees": fees,
#             "reviews": reviews
#         }
#         result.append(json_object)

#     return result

# if __name__ == "__main__":
#     data = extract_table_data("./site.html")
#     print(json.dumps(data, indent=2))


from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client, Client
import re

url: str = os.environ["SUPABASE_PROJECT_URL"]
key: str = os.environ["SUPABASE_ANON_KEY"]
supabase: Client = create_client(url, key)

def extract_table_data(html_file):
    """Extracts data from the HTML table and converts it into a list of JSON objects."""
    result = []

    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    tables_rows = soup.find_all(class_="table-row")  # get all tables rows

    for row in tables_rows:
        
        rank_td = row.find("td", class_="font-weight-medium")
        rank = rank_td.get_text(strip=True) if rank_td else None

        college_name_h3 = row.find("h3", class_="font-weight-medium")
        college_name = college_name_h3.get_text(strip=True) if college_name_h3 else None

        location_span = row.find("span", class_="location")
        location = location_span.get_text(strip=True) if location_span else None

        fees_span = row.find("td", class_="col-fees").a.span
        fees = fees_span.get_text(strip=True) if fees_span.get_text(strip=True) != "--" else None
        # print(fees)

        reviews_span = row.find("td", class_="col-reviews").a.span.find(class_="lr-key") if row.find("td", class_="col-reviews") else None
        reviews = reviews_span.get_text(strip=True).replace(" ", "") if reviews_span else None
        # print(reviews)
        
        cutoff_span = row.find("div", class_="col-popular-course").button.find_all("span")[-1] if row.find("div", class_="col-popular-course") else None
        cutoff = cutoff_span.get_text(strip=True) if cutoff_span else None
        # print(cutoff)
        
        course_span = row.find("div", class_="col-popular-course").button.find(class_="course-name") if row.find("div", class_="col-popular-course") else None
        course = course_span.get_text(strip=True) if course_span else None
        # print(course)
        
        json_object = {
            "rank": re.sub(' +', ' ', rank.strip().replace("\n", " ")) if type(rank) is str else None,
            "name": re.sub(' +', ' ', college_name.strip().replace("\n", " ")) if type(college_name) is str else None,
            "location": re.sub(' +', ' ', location.strip().replace("\n", " ")) if type(location) is str else None,
            "fees": re.sub(' +', ' ', fees.strip().replace("\n", " ")) if type(fees) is str else None,
            "reviews": re.sub(' +', ' ', reviews.strip().replace("\n", " ")) if type(reviews) is str else None,
            "popular_course": re.sub(' +', ' ', course.strip().replace("\n", " ")) if type(course) is str else None,
            "cutoff": re.sub(' +', ' ', cutoff.strip().replace("\n", " ")) if type(cutoff) is str else None
        }
        result.append(json_object)

    return result



if __name__ == "__main__":
    data = extract_table_data("./site2.html")
    for i, row in enumerate(data):
        supabase.table("colleges").insert(row).execute()
        print(f"inserted row #{i+1}, {row['name']}")
    # print(json.dumps(data, indent=4))
