#-*- encoding:utf-8 -*-

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length = 100, blank = True, null = True)
    jenkins_test_url = models.CharField(max_length = 500, blank = True, null = True)
    jenkins_publish_url = models.CharField(max_length = 500, blank = True, null = True)

    @property
    def get_update_url(self):
        return "/update_product/%d/" % self.id

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    class Meta:
        #verbose_name = "徐德东"
        #verbose_name_plural = verbose_name
        ordering = ["-id"]

class Product_Management(models.Model):
    product = models.ForeignKey(Product, related_name = "product_management_set")
    username = models.CharField(max_length = 50, blank = True, null = True)
    #product = models.CharField(max_length = 100, blank = True, null = True)

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-id"]

class SubManager(models.Manager):
    """ 自定义Manager的子类，没什么实际意义 """
    def get_query_set(self):
        return super(self.__class__, self).get_query_set()

class Publish(models.Model):
    product = models.ForeignKey(Product, related_name = "product_set")
    pre_imagename = models.CharField(max_length = 500, blank = True, null = False)
    main_imagename = models.CharField(max_length = 500, blank = True, null = False)
    pub_user = models.CharField(max_length = 50, blank = True, null = False)
    pub_date = models.CharField(max_length = 50, blank = True, null = False)
    pub_status = models.CharField(max_length = 50, blank = True, null = False)
    pub_flag = models.CharField(max_length = 50, blank = True, null = False)
    changelog = models.CharField(max_length = 500, blank = True, null = False)
    test_flag = models.CharField(max_length = 10, blank = True, null = False)
    inner_failed = models.CharField(max_length = 500, blank = True, null = False)
    outer_failed = models.CharField(max_length = 500, blank = True, null = False)

    objects = models.Manager()
    objects = SubManager()

    def get_query_set(self):
        return super(self.__class__, self).get_query_set()

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-pub_date", "-id"]
        #ordering = ["-id"]
