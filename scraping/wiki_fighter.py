
from parsel import Selector
from requests import get
import re

def get_opponent_with_info(html):
    
    opponents = get_opponent(html)
    for o in opponents:
        if link :=o.get('link'):
            response = get(o['link'])
            o['info'] = get_fighter_info(response.text)
        
    return opponents
        
    

def get_opponent(text):
    
    soup = Selector(text=text)

    # tables = soup.find_all("table", "wikitable")
    matches = soup.xpath('//table[@class="wikitable"]')[0]
    trs = matches.xpath('.//tr')
    
    opponents = []
    for tr in trs[1:]:
        opponent = {
            'link' : None,
            'name' : None,
            'outcome' : None
        }
        opponent_node = tr.xpath('./td[3]')
        outcome = tr.xpath('./td[1]/text()').get()
        opponent_name = opponent_node.xpath('.//text()').get()
        opponent_link = opponent_node.xpath('.//@href').get()
        if opponent_link is not None:
            opponent['link'] = f"https://en.wikipedia.org/{opponent_link}"
            
        opponent['name'] = opponent_name.strip('\n')
        opponent['outcome'] = outcome.strip('\n')
        opponents.append(opponent)
    return opponents

def get_fighter_info(html):
    
    selector = Selector(text = html)
    trs = selector.xpath('//table[@class="infobox ib-martial-artist vcard"]/tbody/tr')
    link = trs[1].xpath(".//a/@href").get()
    fighter_info = {
        'Name' : trs[0].xpath("./th/span/text()").get(),
        'Image' : f"https://en.wikipedia.org/{link}",
        'Nickname' : None,
        'Nationality' : None,
        'Style' : None,
        'Height' : None,
        'Weight' : None,
        'BirthDate' : None 
    }  
    for tr in trs[2:]:
        key : str = tr.xpath("./th//text()").get()
        value = tr.xpath("./td//text()").get()
        
        if key is None or value is None:
            continue
        if key.startswith('Nickname'):
            fighter_info['Nickname'] = value
        elif key.startswith('Nationality'):
            fighter_info['Nationality'] = value
        elif key.startswith('Style'):
            fighter_info['Style'] = value
        elif key.startswith('Height'):
            value = value.replace('\u00a0', ' ') 
            pattern = r'(?P<imper>\d+\s*ft\s*\d+\s*in)\s*\(\s*(?P<metric>[\d.]+\s*c?m)\s*\)'
            match = re.search(pattern, value)
            if not match:
                print(value)
            if match:   
                fighter_info['Height'] = {
                    'Imperial' : match.group('imper'),
                    'Metric' : match.group('metric')
                }
        elif key.startswith('Weight'):
            value = value.replace('\u00a0', ' ') 
            pattern = r'(?P<imper>\d+\s*lb)\s*\((?P<metric>\d+\s*kg);\s*(?P<stone>[\d.]+\s*st)(?:\s*\d+\s*lb)?\)'
            match = re.search(pattern, value)
            if not match:
                print(value)
            if match:   
                fighter_info['Weight'] = {
                    'Imperial' : match.group('imper'),
                    'Metric' : match.group('metric'),
                    'Stone': match.group('stone')
                }
        elif key.startswith('Born'):
            date = tr.xpath(".//span[@class='bday']/text()").get()
            if date:
                fighter_info['BirthDate'] = date
            
            
    return fighter_info

