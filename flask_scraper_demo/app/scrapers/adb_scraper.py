def adb_scraper(search_term):
    
    import pandas as pd
    from parsel import Selector
    import requests

    site = 'https://www.adb.org/projects?terms='


    terms = search_term.replace(" ","+")

    site = site + terms + "&page="

    data = pd.DataFrame(columns=['Project Name','URL','Status','DFI'])

    for i in range(100000):
        url = site + str(i)
        page = requests.get(url)
        select = Selector(text = page.text)
        selection = select.css("div.item")
        if len(selection) > 0:
            #Get Title and URL String
            selection1 = selection.css('div.item-title')
            url_list = []
            title_list = []
            status_list = []
            for result in selection1:
                url_final = result.css("a").xpath("@href").extract_first()
                title_final = result.css("a").xpath("string()").extract_first()
                url_list.append(url_final)
                title_list.append(title_final)
            #Get Status String
            selection2 = selection.css("div.item-meta")
            for result in selection2:
                status_final = result.css("div.item-meta span[class]").xpath("string()").extract_first()
                status_list.append(status_final)
            #Add data to dataframe
            for r in range(len(url_list)):
                data_dic = {"Project Name":title_list[r],"Status":status_list[r],'URL':'https://www.adb.org' + url_list[r],
                        'DFI':"Asian Development Bank"}
                data = data.append(data_dic,ignore_index=True)   
        else:
            break
    return data
