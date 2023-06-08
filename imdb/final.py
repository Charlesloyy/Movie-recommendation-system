from requests_html import HTMLSession
import csv
import numpy as np
import pandas as pd
s = HTMLSession()
ft = []
def movie_links(page):
    global lists, header, df, ft
    url = f"https://www.imdb.com/search/title/?title_type=feature&genres=Talk-Show&start={page}&explore=genres&ref_=adv_nxt"

    r =s.get(url)
    content = r.html.find("div.lister-list")
    content_list = r.html.find("div.lister-item.mode-advanced")
   
    lists = []
    
    l_list = np.array([])
    pt = {}
    header = ["Title","Length/genre", "Rating", "metascore", "story_genre_voter_length_director_star_gross"]
    df = pd.DataFrame(columns=header)
    for i in content_list:
        inner_list = []
        
        p = i.text.split("\n")
        
        try:
            title = i.find("h3.lister-item-header", first=True).text
            dip = title.split(".")
            dips = dip[1:]
            try:
                dp = ".".join(dips)
            except:
                dp = dips[0]
           
        except AttributeError as err:
            title = "None"
        
        try:
            length = i.find("span.runtime", first=True).text
        except AttributeError as err:
            length = "None"
        
        try:
            rating = i.find("div.inline-block.ratings-imdb-rating", first=True).text
        except AttributeError as err:
            rating = "None"
        


        
        try:
            meta = i.find("span.metascore.favorable", first=True).text
        except AttributeError as err:
            meta = "None"
        
        
        try:
            genre = i.find("p")
            for p in genre:
                inner_list.append(p.text)
            st = "-".join(inner_list)
            lists.append(st)
            arr = np.array(inner_list)
            genre = arr[0]
            try:
                tit = genre.split("|")[2]
            except IndexError:
                try:
                    tit = genre.split("|")[1]
                except:
                    tit = genre
            story = arr[1]
            
            director_stars = arr[2]
            ds = director_stars.split("|")
            try:
                star = ds[1]
            except IndexError:
                star = "None"
            
                
                 
        except AttributeError as err:
            genre = "None"
        try:
            new_genre = genre.spilt("|")[1]
        except:
            new_genre = "None"
        try:
            stars = star.split(":")[1]
        except:
            stars = "None"
        try:
            dss = ds[0].split(":")[1]
        except:
            dss = "None"
            
        

        
        pt = {
            "Title": dp,
            "Length/genre": length,
            "Rating": rating,
            "metascore": meta,
            "story": story,
            "genre": tit,
            "director": dss,
            "star": stars
            
        }
        
        
        ft.append(pt)

    
    return ft




result = []
dt = 1
while dt <= 301:
    print("Getting next page")
    links = movie_links(dt)
    result.append(links)
     
    dt+=50
key = ft[0].keys()

with open("movies4.csv", 'w', encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, key)
    dict_writer.writeheader()
    dict_writer.writerows(ft)
