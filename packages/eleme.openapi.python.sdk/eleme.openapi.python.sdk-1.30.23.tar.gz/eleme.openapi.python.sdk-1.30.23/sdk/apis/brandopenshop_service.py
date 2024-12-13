# -*- coding: utf-8 -*-


# 品牌建店服务
class BrandopenshopService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def get_chain_node_tree(self):
        """
        查询当前账号归属的连锁树结构
        """
        return self.__client.call("eleme.brandOpenShop.getChainNodeTree", {})

    def get_all_catering_category(self):
        """
        查询所有餐饮品类信息
        """
        return self.__client.call("eleme.brandOpenShop.getAllCateringCategory", {})

    def upload_image(self, request):
        """
        上传图片
        :param request:图片上传请求
        """
        return self.__client.call("eleme.brandOpenShop.uploadImage", {"request": request})

    def create_shop_batch_task(self, request):
        """
        创建批量开店任务
        :param request:批量开店任务创建/更新请求
        """
        return self.__client.call("eleme.brandOpenShop.createShopBatchTask", {"request": request})

    def create_shop_apply(self, request):
        """
        创建/更新开店申请单
        :param request:开店申请单创建/更新请求
        """
        return self.__client.call("eleme.brandOpenShop.createShopApply", {"request": request})

    def batch_submit_audit(self, request):
        """
        开店任务提交审核
        :param request:提交审核请求
        """
        return self.__client.call("eleme.brandOpenShop.batchSubmitAudit", {"request": request})

    def submit_audit(self, request):
        """
        开店申请单提交审核
        :param request:提交审核请求
        """
        return self.__client.call("eleme.brandOpenShop.submitAudit", {"request": request})

    def query_shop_batch_task(self, request):
        """
        查询开店任务详情
        :param request:查询条件
        """
        return self.__client.call("eleme.brandOpenShop.queryShopBatchTask", {"request": request})

    def query_apply_detail(self, request):
        """
        查询开店申请单详情
        :param request:查询条件
        """
        return self.__client.call("eleme.brandOpenShop.queryApplyDetail", {"request": request})

    def obtain_all_catering_license_config(self):
        """
        获取所有支持的餐饮证照配置
        """
        return self.__client.call("eleme.brandOpenShop.obtainAllCateringLicenseConfig", {})

    def support_brand_list(self):
        """
        获取当前账号支持的品牌信息
        """
        return self.__client.call("eleme.brandOpenShop.supportBrandList", {})

