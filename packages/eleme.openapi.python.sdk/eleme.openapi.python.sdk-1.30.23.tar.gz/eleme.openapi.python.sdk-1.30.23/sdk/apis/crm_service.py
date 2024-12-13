# -*- coding: utf-8 -*-


# CRM会员开放平台-权益服务
class CrmService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def query_member_benefit_by_poi(self, request):
        """
        根据经纬度查询范围内的会员权益
        :param request:请求入参
        """
        return self.__client.call("eleme.crm.queryMemberBenefitByPoi", {"request": request})

    def exit_membership(self, request):
        """
        会员退会
        :param request:请求参数
        """
        return self.__client.call("eleme.crm.exitMembership", {"request": request})

