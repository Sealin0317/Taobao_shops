# -*- coding: utf-8 -*-
import scrapy
from ky import *
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from taobaoproject.items import ShopItem

# washing keywords2
shoe = shoe.split('\t')
toy = toy.split('\t')
appliance = appliance.split('\t')
makeup = makeup.split('\t')
jewelry = jewelry.split('\t')
flower = flower.split('\t')
furniture = furniture.split('\t')
car = car.split('\t')
supplies = supplies.split('\t')
stuff = stuff
study = study.split('\t')
men = men.split('\t')
bag = bag.split('\t')
digital = digital.split('\t')
washing = washing.split('\t')
comic = comic.split('\t')
fresh = fresh.split('\t')
pet = pet.split('\t')
homeware = homeware
DIY = DIY.split('\t')
kitchen = kitchen.split('\t')
bonouce = bonouce.split('\t')
underware = underware.split('\t')
accessory = accessory.split('\t')
health_product = health_product.split('\t')
agricultural = agricultural.split('\t')
building_materials = building_materials.split('\t')
textiles = textiles.split('\t')
hardware = hardware.split('\t')
home_care = home_care.split('\t')
service = service.split('\t')
chr_shoe = chr_shoe.split('\t')
chr_clothes = chr_clothes.split('\t')
pregnant = pregnant.split('\t')
infant = infant.split('\t')
special_shoe = special_shoe.split('\t')
fitness = fitness.split('\t')
outdorrs = outdorrs.split('\t')
swimming = swimming.split('\t')
instrument = instrument.split('\t')
game = game.split('\t')
snacks = snacks.split('\t')
dessert = dessert.split('\t')
staple = staple.split('\t')
tea = tea.split('\t')
medic = medic.split('\t')
wine = wine.split('\t')
sports = sports.split('\t')

keywords_2 = [dress, shoe, toy, appliance, makeup, jewelry, flower, furniture, car, supplies, stuff, study,
              men, bag, digital, washing, comic, fresh, pet, homeware, DIY, kitchen, bonouce, underware, accessory,
              health_product, agricultural, building_materials, textiles, hardware, home_care, service,
              chr_shoe, chr_clothes, pregnant, infant, special_shoe, fitness, outdorrs, swimming, instrument,
              game, snacks, dessert, staple, tea, medic, wine, sports]
keywords_1 = ['女装', '鞋靴', '童装玩具', '家电', '美妆', '珠宝', '鲜花', '家具', '汽车', '办公', '百货', '学习', '男装', '箱包',
              '数码', '洗护', '动漫', '生鲜', '宠物', '家饰', 'DIY', '餐厨', '卡券', '内衣', '服装配件', '保健品', '农资',
              '建材', '家纺', '五金电子', '家庭保健', '本地服务', '童鞋', '童装', '孕产用品', '母婴用品', '潮鞋', '健身',
              '户外', '游泳', '乐器', '游戏', '零食', '甜点', '主食', '茶叶', '中药材', '白酒', '运动']

# 地址
locations = ['北京', '上海', '广州', '深圳', '杭州', '长沙', '长春', '成都', '重庆', '大连', '东莞', '佛山', '福州', '贵阳', '合肥', '金华', '济南', '嘉兴',
             '昆明', '宁波', '南昌', '南京', '青岛', '泉州', '沈阳', '苏州', '天津', '温州', '无锡', '武汉', '西安', '厦门', '郑州', '中山', '石家庄',
             '哈尔滨', '安徽', '福建', '甘肃', '广东', '广西', '贵州', '海南', '河北', '河南', '湖北', '湖南', '江苏', '江西', '吉林', '辽宁', '宁夏',
             '青海', '山东', '山西', '陕西', '云南', '四川', '西藏', '新疆', '浙江', '澳门', '香港', '台湾', '内蒙古', '黑龙江']

# merging keywords
dic = dict(zip(keywords_1, keywords_2))
dic2 = dict().fromkeys(locations,keywords_1)


class TaobaoProductSpider(scrapy.Spider):
    name = 'taobao_product'
    allowed_domains = ['shopsearch.taobao.com']
    start_urls = []

    def start_requests(self):
        for k in dic.keys():
            k1 = k
            for v in dic.get(k1):
                k2 = v
                for loc in dic2.keys():
                    location = loc
                    base_url = 'https://shopsearch.taobao.com/search?'
                    data = {
                        'app': 'shopsearch',
                        'q': k1 + k2,
                        'js': 1,
                        'initiative_id': 'staobaoz_20170806',
                        'ie': 'utf8',
                        'loc': location,
                        'sort': 'sale-desc',
                        's': 0
                    }
                    queries = urlencode(data)
                    url = base_url + queries
                    request = scrapy.Request(url=url, callback=self.parse_index, dont_filter=True, meta={'cp': 1})
                    request.meta['k1'] = k1
                    request.meta['k2'] = k2
                    request.meta['location'] = location
                    yield request

    def parse(self, response):
        pass

    def parse_index(self, response):
        print('Here is method parse_index ---------------------------')
        # store_number = response.meta['store_number']
        # page_numbers = response.meta['page_numbers']
        k1 = response.meta['k1']
        k2 = response.meta['k2']
        location = response.meta['location']
        try:
            doc = pq(response.body)
            store_number = int(doc('#J_Filter > div > span > b').text())
            print(
                'The store number of %s+%s in %s is %d ---------------------------' % (k1, k2, location, store_number))
            if store_number <= 20:
                for i in range(0, store_number):
                    print('count~~~~~~~~~~~store_number:', i)
                    title = doc('#list-container .list-item .list-info h4 .shop-name').eq(i).text()
                    if doc('#list-container li h4 .rank').eq(i):
                        rank = doc('#list-container li h4 .rank').eq(i).attr['class'][17:]
                        rate = doc('#list-container li .good-comt').eq(i).text()[5:]
                    else:
                        rank = '100'
                        rate = '100'
                    sales = doc('#list-container li .info-sale em').eq(i).text()
                    amount = doc('#list-container li .info-sum em').eq(i).text()
                    print(k1, k2, title, location, rank, rate, sales, amount)
                    if title:
                        item = ShopItem()
                        item['k1'] = k1
                        item['k2'] = k2
                        item['title'] = title
                        item['location'] = location
                        item['rank'] = rank
                        item['rate'] = rate
                        item['sales'] = sales
                        item['amount'] = amount
                        yield item
                    else:
                        pass
            else:
                for i in range(0, 20):
                    print('count~~~~~~~~~~~store_number:', i)
                    title = doc('#list-container .list-item .list-info h4 .shop-name').eq(i).text()
                    if doc('#list-container li h4 .rank').eq(i):
                        rank = doc('#list-container li h4 .rank').eq(i).attr['class'][17:]
                        rate = doc('#list-container li .good-comt').eq(i).text()[5:]
                    else:
                        rank = '100'
                        rate = '100'
                    sales = doc('#list-container li .info-sale em').eq(i).text()
                    amount = doc('#list-container li .info-sum em').eq(i).text()
                    if title:
                        print(k1, k2, title, location, rank, rate, sales, amount)
                        item = ShopItem()
                        item['k1'] = k1
                        item['k2'] = k2
                        item['title'] = title
                        item['location'] = location
                        item['rank'] = rank
                        item['rate'] = rate
                        item['sales'] = sales
                        item['amount'] = amount
                        yield item
                    else:
                        pass
                request = scrapy.Request(url=response.url, callback=self.parse_info, meta={'cp': 2}, dont_filter=True)
                request.meta['store_number'] = store_number
                # request.meta['page_numbers'] = page_numbers
                request.meta['k1'] = response.meta['k1']
                request.meta['k2'] = response.meta['k2']
                request.meta['location'] = response.meta['location']
                yield request
        except Exception as e:
            print('fail in getting info', e.args)

    def parse_info(self, response):
        print('Here is method parse_info ---------------------------')
        k1 = response.meta['k1']
        k2 = response.meta['k2']
        location = response.meta['location']
        store_number = response.meta['store_number']
        try:
            doc = pq(response.body)
            for i in range(0, 20):
                print('count~~~~~~~~~~~store_number:', i)
                title = doc('#list-container .list-item .list-info h4 .shop-name').eq(i).text()
                if doc('#list-container li h4 .rank').eq(i):
                    rank = doc('#list-container li h4 .rank').eq(i).attr['class'][17:]
                    rate = doc('#list-container li .good-comt').eq(i).text()[5:]
                else:
                    rank = '100'
                    rate = '100'
                sales = doc('#list-container li .info-sale em').eq(i).text()
                amount = doc('#list-container li .info-sum em').eq(i).text()
                if title:
                    print(k1, k2, title, location, rank, rate, sales, amount)
                    item = ShopItem()
                    item['k1'] = k1
                    item['k2'] = k2
                    item['title'] = title
                    item['location'] = location
                    item['rank'] = rank
                    item['rate'] = rate
                    item['sales'] = sales
                    item['amount'] = amount
                    yield item
                else:
                    pass
            if doc('#shopsearch-pager > div > div > div > ul > li.item.next > a > span.icon.icon-btn-next-2'):
                request = scrapy.Request(url=response.url, callback=self.parse_info, meta={'cp': 2}, dont_filter=True)
                request.meta['store_number'] = store_number
                request.meta['k1'] = response.meta['k1']
                request.meta['k2'] = response.meta['k2']
                request.meta['location'] = response.meta['location']
                yield request
            else:
                print(k1, k2, location, 'is finished NOW')
                return None
        except Exception as e:
            print('fail in getting info', e.args)
