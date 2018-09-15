from djongo import models


class CustomerReports(models.Model):
    _id = models.ObjectIdField()
    company_name = models.TextField()
    user_report = models.TextField()
    company_response = models.TextField()
    user_feedback = models.TextField()
    user_rating = models.IntegerField()
    date = models.BigIntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)


class CompanyReports(models.Model):
    _id = models.ObjectIdField()
    region = models.CharField(max_length=2)
    state = models.CharField(max_length=2)
    city = models.TextField()
    gender = models.CharField(max_length=1)
    age_range = models.IntegerField()
    conclusion_date = models.BigIntegerField()
    days_to_reply = models.IntegerField()
    company_name = models.TextField()
    market_segment = models.TextField()
    problem_reported = models.TextField()
    company_replied = models.BooleanField()
    customer_rating = models.IntegerField()
