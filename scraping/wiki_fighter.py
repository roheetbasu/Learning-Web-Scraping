
from parsel import Selector
from requests import get

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
        'Style' : None
    }  
    for tr in trs[2:]:
        key : str = tr.xpath("./th//text()").get()
        value = tr.xpath("./td//text()").get()
        
        if key == 'Nickname':
            fighter_info['Nickname'] = value
        elif key == 'Nationality':
            fighter_info['Nationality'] = value
        elif key == 'Style':
            fighter_info['Style'] = value
            
    return fighter_info