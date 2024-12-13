# -*- coding: utf-8 -*-


# 斗金服务
class AdService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def find_dou_jin_cpc_solution(self, request):
        """
        查询斗金推广设置
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.findDouJinCpcSolution", {"request": request})

    def find_dou_jin_click_distribution_report(self, request):
        """
        查询斗金推广点击分布信息
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.findDouJinClickDistributionReport", {"request": request})

    def find_dou_jin_effect_report(self, request):
        """
        查询斗金推广效果数据
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.findDouJinEffectReport", {"request": request})

    def update_dou_jin_time(self, request):
        """
        设置斗金时段
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.updateDouJinTime", {"request": request})

    def update_dou_jin_target(self, request):
        """
        设置斗金定向
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.updateDouJinTarget", {"request": request})

    def update_dou_jin_budget(self, request):
        """
        设置斗金预算
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.updateDouJinBudget", {"request": request})

    def update_dou_jin_bid(self, request):
        """
        设置斗金出价
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.updateDouJinBid", {"request": request})

    def update_dou_jin_state(self, request):
        """
        设置斗金状态
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.updateDouJinState", {"request": request})

    def create_dou_jin_solution(self, request):
        """
        创建斗金计划
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.createDouJinSolution", {"request": request})

    def find_dou_jin_account_balance(self, request):
        """
        查询斗金最大可用余额
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpc.findDouJinAccountBalance", {"request": request})

    def find_account_balance(self, request):
        """
        查询账户余额
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.common.findAccountBalance", {"request": request})

    def find_dou_jin_cpc_solution(self, request):
        """
        分页查询斗金连锁计划
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.findDouJinCpcSolution", {"request": request})

    def create_dou_jin_solution(self, request):
        """
        创建斗金连锁计划
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.createDouJinSolution", {"request": request})

    def update_dou_jin_state(self, request):
        """
        设置斗金连锁计划状态
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.updateDouJinState", {"request": request})

    def update_dou_jin_time(self, request):
        """
        设置斗金连锁计划时段
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.updateDouJinTime", {"request": request})

    def update_dou_jin_date(self, request):
        """
        设置斗金连锁计划日期
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.updateDouJinDate", {"request": request})

    def update_dou_jin_title(self, request):
        """
        设置斗金连锁计划名称
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.updateDouJinTitle", {"request": request})

    def update_dou_jin_budget(self, request):
        """
        设置斗金连锁计划日预算
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.updateDouJinBudget", {"request": request})

    def update_dou_jin_bid(self, request):
        """
        设置斗金连锁计划门店出价
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.updateDouJinBid", {"request": request})

    def update_dou_jin_shop_budget(self, request):
        """
        设置斗金连锁计划门店预算
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.updateDouJinShopBudget", {"request": request})

    def update_dou_jin_target(self, request):
        """
        设置斗金连锁计划定向
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.updateDouJinTarget", {"request": request})

    def add_dou_jin_shop(self, request):
        """
        新增斗金连锁计划门店
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.addDouJinShop", {"request": request})

    def delete_dou_jin_shop(self, request):
        """
        删除斗金连锁计划门店
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.deleteDouJinShop", {"request": request})

    def find_shop_city_price(self, request):
        """
        查询门店的最低预算和最低出价
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.findShopCityPrice", {"request": request})

    def find_effect_report_with_campaign_and_date(self, request):
        """
        斗金连锁品牌资金计划维度效果数据
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.findEffectReportWithCampaignAndDate", {"request": request})

    def find_effect_report_with_shop_and_date(self, request):
        """
        斗金连锁分店资金门店x日期维度效果数据
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.findEffectReportWithShopAndDate", {"request": request})

    def find_effect_report_with_campaign_and_shop_and_date(self, request):
        """
        斗金连锁品牌资金门店x计划x日期维度效果数据
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.doujincpcchain.findEffectReportWithCampaignAndShopAndDate", {"request": request})

    def find_display_cpc_solution(self, request):
        """
        查询优享大牌推广设置
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.findDisplayCpcSolution", {"request": request})

    def find_display_effect_report(self, request):
        """
        查询优享大牌推广效果数据
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.findDisplayEffectReport", {"request": request})

    def update_display_time(self, request):
        """
        设置优享大牌时段
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.updateDisplayTime", {"request": request})

    def update_display_target(self, request):
        """
        设置优享大牌定向
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.updateDisplayTarget", {"request": request})

    def update_display_budget(self, request):
        """
        设置优享大牌预算
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.updateDisplayBudget", {"request": request})

    def update_display_bid(self, request):
        """
        设置优享大牌出价
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.updateDisplayBid", {"request": request})

    def update_display_state(self, request):
        """
        设置优享大牌状态
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.updateDisplayState", {"request": request})

    def create_display_solution(self, request):
        """
        创建优享大牌计划
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.createDisplaySolution", {"request": request})

    def find_display_account_balance(self, request):
        """
        查询优享大牌最大可用余额
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpc.findDisplayAccountBalance", {"request": request})

    def find_display_cpc_solution(self, request):
        """
        分页查询优享大牌连锁计划
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.findDisplayCpcSolution", {"request": request})

    def create_display_solution(self, request):
        """
        创建优享大牌连锁计划
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.createDisplaySolution", {"request": request})

    def update_display_state(self, request):
        """
        设置优享大牌连锁计划状态
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.updateDisplayState", {"request": request})

    def update_display_time(self, request):
        """
        设置优享大牌连锁计划时段
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.updateDisplayTime", {"request": request})

    def update_display_date(self, request):
        """
        设置优享大牌连锁计划日期
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.updateDisplayDate", {"request": request})

    def update_display_title(self, request):
        """
        设置优享大牌连锁计划名称
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.updateDisplayTitle", {"request": request})

    def update_display_budget(self, request):
        """
        设置优享大牌连锁计划日预算
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.updateDisplayBudget", {"request": request})

    def update_display_bid(self, request):
        """
        设置优享大牌连锁计划门店出价
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.updateDisplayBid", {"request": request})

    def update_display_shop_budget(self, request):
        """
        设置优享大牌连锁计划门店预算
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.updateDisplayShopBudget", {"request": request})

    def update_display_target(self, request):
        """
        设置优享大牌连锁计划定向
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.updateDisplayTarget", {"request": request})

    def add_display_shop(self, request):
        """
        新增优享大牌连锁计划门店
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.addDisplayShop", {"request": request})

    def delete_display_shop(self, request):
        """
        删除优享大牌连锁计划门店
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.deleteDisplayShop", {"request": request})

    def find_shop_city_price(self, request):
        """
        查询门店的最低预算和最低出价
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.findShopCityPrice", {"request": request})

    def find_effect_report_with_campaign_and_date(self, request):
        """
        优享cpc连锁品牌资金计划维度效果数据
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.findEffectReportWithCampaignAndDate", {"request": request})

    def find_effect_report_with_shop_and_date(self, request):
        """
        优享cpc连锁分店资金门店x日期维度效果数据
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.findEffectReportWithShopAndDate", {"request": request})

    def find_effect_report_with_campaign_and_shop_and_date(self, request):
        """
        优享cpc连锁品牌资金门店x计划x日期维度效果数据
        :param request:请求参数
        """
        return self.__client.call("eleme.ad.displaycpcchain.findEffectReportWithCampaignAndShopAndDate", {"request": request})

