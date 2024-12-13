# -*- coding: utf-8 -*-


# 开票服务
class InvoiceService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def accept_success(self, request):
        """
        受理成功
        :param request:开具单受理成功通知入参
        """
        return self.__client.call("eleme.invoice.issue.acceptSuccess", {"request": request})

    def accept_failure(self, request):
        """
        受理失败
        :param request:开具单受理失败通知入参
        """
        return self.__client.call("eleme.invoice.issue.acceptFailure", {"request": request})

    def issue_success(self, request):
        """
        开具成功
        :param request:开具单开具成功通知入参
        """
        return self.__client.call("eleme.invoice.issue.issueSuccess", {"request": request})

    def issue_failure(self, request):
        """
        开具失败
        :param request:开具单开具失败通知入参
        """
        return self.__client.call("eleme.invoice.issue.issueFailure", {"request": request})

    def register_success(self, request):
        """
        闪电开票服务注册成功
        :param request:注册成功通知入参
        """
        return self.__client.call("eleme.invoice.flash.registerSuccess", {"request": request})

    def register_failure(self, request):
        """
        闪电开票服务注册失败
        :param request:注册失败通知入参
        """
        return self.__client.call("eleme.invoice.flash.registerFailure", {"request": request})

    def renew_success(self, request):
        """
        闪电开票服务有效期更新
        :param request:续签通知入参
        """
        return self.__client.call("eleme.invoice.flash.renewSuccess", {"request": request})

    def terminate_success(self, request):
        """
        闪电开票服务退订
        :param request:退订通知入参
        """
        return self.__client.call("eleme.invoice.flash.terminateSuccess", {"request": request})

    def batch_query_shop_settings(self, request):
        """
        批量查询店铺开票设置
        :param request:查询请求
        """
        return self.__client.call("eleme.invoice.seller.batchQueryShopSettings", {"request": request})

    def batch_update_shop_settings(self, request):
        """
        批量更新店铺开票设置
        :param request:更新请求
        """
        return self.__client.call("eleme.invoice.seller.batchUpdateShopSettings", {"request": request})

    def batch_query_shop_application(self, request):
        """
        批量查询店铺开票申请
        :param request:查询请求
        """
        return self.__client.call("eleme.invoice.seller.batchQueryShopApplication", {"request": request})

    def batch_update_shop_application(self, request):
        """
        批量更新店铺开票申请
        :param request:更新请求
        """
        return self.__client.call("eleme.invoice.seller.batchUpdateShopApplication", {"request": request})

