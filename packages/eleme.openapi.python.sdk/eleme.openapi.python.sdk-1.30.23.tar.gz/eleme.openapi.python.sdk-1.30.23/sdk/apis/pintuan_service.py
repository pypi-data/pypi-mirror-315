# -*- coding: utf-8 -*-


# 拼团服务
class PintuanService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def query_pin_item_by_ext_code(self, shop_id, ext_code):
        """
        查询单个拼团商品
        :param shopId:店铺ID
        :param extCode:商品extCode
        """
        return self.__client.call("eleme.pintuan.queryPinItemByExtCode", {"shopId": shop_id, "extCode": ext_code})

    def get_all_pin_items(self, shop_id):
        """
        批量查询店铺拼团商品
        :param shopId:店铺ID
        """
        return self.__client.call("eleme.pintuan.getAllPinItems", {"shopId": shop_id})

    def update_on_shelf_by_ext_code(self, shop_id, ext_code, on_shelf):
        """
        操作拼团商品上下架
        :param shopId:店铺ID
        :param extCode:商品extCode
        :param onShelf:上下架-1上架,0下架
        """
        return self.__client.call("eleme.pintuan.updateOnShelfByExtCode", {"shopId": shop_id, "extCode": ext_code, "onShelf": on_shelf})

    def update_pin_tuan_stock(self, shop_id, request):
        """
        修改拼团商品库存
        :param shopId:店铺ID
        :param request:库存信息
        """
        return self.__client.call("eleme.pintuan.updatePinTuanStock", {"shopId": shop_id, "request": request})

    def update_pin_item_mapping(self, request):
        """
        创建拼团商品映射，更新商品ext_code字段
        :param request:拼团商品映射信息
        """
        return self.__client.call("eleme.pintuan.updatePinItemMapping", {"request": request})

