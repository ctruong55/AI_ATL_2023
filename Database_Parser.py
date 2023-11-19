import requests
from bs4 import BeautifulSoup
import json
import time
import csv
import ast
import re



class Database_Parser():
    ret = []
    headers = {
        # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'en-US,en;q=0.9',
        # 'cache-control': 'no-cache',
        # 'cookie': 'zguid=24|%247c534f30-ae51-4b95-a9f1-a073ce047483; zgsession=1|605dd98c-84fc-421e-9e0c-dd4ebb41b740; _ga=GA1.2.777559362.1700269765; _gid=GA1.2.408979259.1700269765; pxcts=1e1bc4f8-85af-11ee-b1cb-404d23653c6d; _pxvid=1e1bb624-85af-11ee-b1cb-dcfd1a950357; zjs_user_id=null; zg_anonymous_id=%22a4c6b401-4329-4a0f-b722-cb43dc8f2938%22; _gcl_au=1.1.607156370.1700269766; DoubleClickSession=true; _fbp=fb.1.1700269766605.757669649; __pdst=13f35418dbcd498fb0f4db905d1e4b55; _clck=153zyri%7C2%7Cfgt%7C0%7C1417; _pin_unauth=dWlkPU1EUm1ZbUUxTVRrdFpHWmpZeTAwWVRZeExUa3haRFV0WlRRNE5qRmtZbUk1TUdNdw; zjs_anonymous_id=%227c534f30-ae51-4b95-a9f1-a073ce047483%22; _gac_UA-21174015-56=1.1700279352.CjwKCAiAu9yqBhBmEiwAHTx5p-T52ZwTySRBJAks-DTaZh_4izoACTFH2BcJ8Bdbsf7v6xlLkdVbyhoCwCwQAvD_BwE; _gcl_aw=GCL.1700279352.CjwKCAiAu9yqBhBmEiwAHTx5p-T52ZwTySRBJAks-DTaZh_4izoACTFH2BcJ8Bdbsf7v6xlLkdVbyhoCwCwQAvD_BwE; g_state={"i_p":1700411700124,"i_l":2}; _hp2_id.1215457233=%7B%22userId%22%3A%224743395633785566%22%2C%22pageviewId%22%3A%228903715124670291%22%2C%22sessionId%22%3A%227804836779862794%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; JSESSIONID=36B85D6AAE9C3EC622D7733A2DC9D797; AWSALB=st+U4xufQcBNtjB9UOwGtUBGtqxxnYK1yBt11uyPF15162o6rfgVt5E3HunooSy5sTEowRnDp0qOIeeZaZ8G4S7ThQOPMDBOUSV89IrtopbioNRpRnS3xkJgvwWX; AWSALBCORS=st+U4xufQcBNtjB9UOwGtUBGtqxxnYK1yBt11uyPF15162o6rfgVt5E3HunooSy5sTEowRnDp0qOIeeZaZ8G4S7ThQOPMDBOUSV89IrtopbioNRpRnS3xkJgvwWX; _uetsid=1e20bba085af11ee9c22bdf21ffb1812; _uetvid=1e20d4a085af11ee996bd1a503360c23; tfpsi=daa176b7-6264-45d8-8f74-c400fc5376bb; __gads=ID=3e2ef9db3f9d5820:T=1700276203:RT=1700331432:S=ALNI_MZFRkwOSAQLU8_Ot5kBK5TFAmdHpg; __gpi=UID=00000da27a4132d5:T=1700276203:RT=1700331432:S=ALNI_MavNAPpzlqJ1E7l2TynAAIwRNdjgA; _px3=0ce8645c4be5394df33aa7d3f580a9694940c918945220b5ad1c64c3359bbff9:FyCfCcVGPXuXBK9NaIaAaOPdaR0m6waLKH6li6apymITYh9iCO6oT7t+jmMdkubkSVH6suGcPpUvWe/Dy2efvg==:1000:RZK7VxuY5KauGc3v9V5lc9XVojAOvAfHfPEFRKbCrG6vXUV6ion1wi6dXRjEDeoYtSmXBy6eKGL6y6/HgBSN+mFtK2xvbdyJu7xCbgiNgDqDaXOawJHfWSHFhVfNRg7SIjgwdmRbeOcNDKJHGqPwTh3lAqL78Wxgn0tSD/ZJCpuWoL6RsVhYCqRvgsQKko0Xn2rS3/M93VGhVqh9q36TqQXnX4m1T69ESsLy4uEXYcM=; x-amz-continuous-deployment-state=AYABeOPrRTnmgLJuYEbRn4775ScAPgACAAFEAB1kM2Jsa2Q0azB3azlvai5jbG91ZGZyb250Lm5ldAABRwAVRzA3MjU1NjcyMVRZRFY4RDcyVlpWAAEAAkNEABpDb29raWUAAACAAAAADENJ8Rdr7HFOu0HtqAAw%2FL+1XSl3eK1IK+Bva5+JqcMzwSKcwZPCZvSQ20yTcUPVy6T6NDiggtHhj0hN4QjYAgAAAAAMAAQAAAAAAAAAAAAAAAAAABTlQYZ3l7JeGbDl3mboz6T%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAAAySmCUK35ycQtTopxl9bfo35Ux1So1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vkSo1mIbSWd5vk; _clsk=1wg4x6o%7C1700331725367%7C28%7C0%7Cs.clarity.ms%2Fcollect; search=6|1702923726177%7Crect%3D33.995592701592905%2C-84.19833840820314%2C33.55325407049238%2C-84.68997659179689%26rid%3D37211%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0937211%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09',
        # 'pragma': 'no-cache',
        # 'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform':'"Windows"',
        # 'sec-fetch-dest': 'document',
        # 'sec-fdetch-mode': 'navigate',
        # 'sec-fetch-site': 'same-origin',
        # 'sec-fetch-user': '?1',
        # 'upgrade-insecure-requests': '1',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Cookie': 'zguid=24|%247c534f30-ae51-4b95-a9f1-a073ce047483; zgsession=1|605dd98c-84fc-421e-9e0c-dd4ebb41b740; _ga=GA1.2.777559362.1700269765; _gid=GA1.2.408979259.1700269765; pxcts=1e1bc4f8-85af-11ee-b1cb-404d23653c6d; _pxvid=1e1bb624-85af-11ee-b1cb-dcfd1a950357; zjs_user_id=null; zg_anonymous_id=%22a4c6b401-4329-4a0f-b722-cb43dc8f2938%22; _gcl_au=1.1.607156370.1700269766; DoubleClickSession=true; _fbp=fb.1.1700269766605.757669649; __pdst=13f35418dbcd498fb0f4db905d1e4b55; _clck=153zyri%7C2%7Cfgt%7C0%7C1417',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    def get(self, url):
        give = requests.get(url, headers=self.headers)
        return give

    def parse(self, response):
        # houseData = BeautifulSoup(response, 'lxml')
        #print(response.text[:-100000])
        try:
            holdJSON = json.loads(response)
        except Exception:
            return None
        print(holdJSON)
        for item in self.ret:
            if len(self.ret) != 0 and holdJSON['addressStreet'] == self.ret[0]['Address']:
                return None
        if 'carouselPhotos' not in holdJSON.keys():
            self.ret.append({
                        'Price': holdJSON['price'],
                        'Address': holdJSON['addressStreet'],
                        'City': holdJSON['addressCity'],
                        'State': holdJSON['addressState'],
                        'Postal': holdJSON['addressZipcode'],
                        'Floor Size': holdJSON['area'],
                        'Longitude': holdJSON['hdpData']['homeInfo']['latitude'],
                        'Latitude': holdJSON['hdpData']['homeInfo']['longitude'],
                        'URL': holdJSON['detailUrl']
            })
        elif 'area' not in holdJSON.keys():
            self.ret.append({
                        'Price': holdJSON['price'],
                        'Address': holdJSON['addressStreet'],
                        'City': holdJSON['addressCity'],
                        'State': holdJSON['addressState'],
                        'Postal': holdJSON['addressZipcode'],
                        'Longitude': holdJSON['hdpData']['homeInfo']['latitude'],
                        'Latitude': holdJSON['hdpData']['homeInfo']['longitude'],
                        'URL': holdJSON['detailUrl'],
                        'Picture': holdJSON['carouselPhotos']
            })
        else: self.ret.append({
                        'Price': holdJSON['price'],
                        'Address': holdJSON['addressStreet'],
                        'City': holdJSON['addressCity'],
                        'State': holdJSON['addressState'],
                        'Postal': holdJSON['addressZipcode'],
                        'Floor Size': holdJSON['area'],
                        'Longitude': holdJSON['hdpData']['homeInfo']['latitude'],
                        'Latitude': holdJSON['hdpData']['homeInfo']['longitude'],
                        'URL': holdJSON['detailUrl'],
                        'Picture': holdJSON['carouselPhotos']
            })

        # imageList = holdJSON.find('ul', {'class': 'List-c11n-8-84-3__sc-1smrmqp-0 StyledSearchListWrapper-srp__sc-1ieen0c-0 doa-doM fgiidE photo-cards'})
        # if imageList:
        #     for image in imageList.contents:
        #         hold = image.find('script', {'type', 'application/ld+json'})
        #         if hold:
        #             holdJSON = json.loads(hold.contents[0])
        #             print(holdJSON)
        #             self.ret.append({
        #                 'Price': hold.find('div', {'class': 'list-card-price'}).text,
        #                 'Address': holdJSON['address']['streetAddress'],
        #                 'City': holdJSON['address']['addressLocality'],
        #                 'State': holdJSON['address']['addressRegion'],
        #                 'Postal': holdJSON['address']['postalCode'],
        #                 'Floor Size': holdJSON['floorSize']['value'],
        #                 'Longitude': holdJSON['geo']['longitude'],
        #                 'Latitude': holdJSON['geo']['latitude'],
        #                 'URL': holdJSON['url'],
        #                 'Picture': image.find('picture', {'source': 'srcset'})
        #             })
        # else:
        #     print("No data found for the specified class.")

    def convert(self):
        if self.ret:
            with open('Open_Housing_ForSale_numb#2.csv', 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.ret[0].keys())
                writer.writeheader()
                for row in self.ret:
                    writer.writerow(row)
        else:
            print('No Data to Write to CSV')

    def start(self):
        url = 'https://www.zillow.com/homes/for_sale/'

        for page in range(14, 21):
            # params = {
            #     'searchQueryState': '{"pagination":{%s},"isMapVisible":true,"mapBounds":{"west":-84.70817269775392,"east":-84.18014230224611,"south":33.55525685737029,"north":33.99360018262278},"filterState":{"sort":{"value":"globalrelevanceex"},"ah":{"value":true},"isListVisible":true,"mapZoom":11}' %page

            # }
            url+='%s_p/' %page
            res = self.get(url)
            out = ""
            index = res.text.find("{\"zpid\"")
            r = res.text
            while index != -1:
                index = r.find("{\"zpid\"")
                index2 = r[index:].find("\"rooms")
                out = r[index:index + index2 + 11]
                print(out)
                self.parse(out)
                r = r[index2:]
            print(url)
            url = 'https://www.zillow.com/homes/for_sale/'
            time.sleep(2)
        self.convert()

if __name__ == '__main__':
    web_parser = Database_Parser()
    web_parser.start()
