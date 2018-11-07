from django.db.models import Avg, Q
import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import CustomerReports, CompanyReports


class CustomerReportsFilter(django_filters.FilterSet):
    class Meta:
        model = CustomerReports
        fields = ['company_name', 'user_rating', 'date', 'city', 'state']


class CustomerReportsType(DjangoObjectType):
    class Meta:
        model = CustomerReports
        interfaces = (graphene.relay.Node, )


class CompanyReportsFilter(django_filters.FilterSet):
    class Meta:
        model = CompanyReports
        fields = ['region', 'state', 'city',
                  'gender', 'age_range', 'company_name']


class CompanyReportsType(DjangoObjectType):
    class Meta:
        model = CompanyReports
        interfaces = (graphene.relay.Node, )


class Result(graphene.ObjectType):
    year = graphene.String()
    month = graphene.String()
    count = graphene.String()


class Query(graphene.ObjectType):
    customer_report = graphene.relay.Node.Field(CustomerReportsType)
    all_customer_reports = DjangoFilterConnectionField(
        CustomerReportsType, filterset_class=CustomerReportsFilter)

    company_report = graphene.relay.Node.Field(CompanyReportsType)
    all_company_reports = DjangoFilterConnectionField(
        CompanyReportsType, filterset_class=CompanyReportsFilter)

    companies_names = graphene.List(graphene.String)
    total_company_reports = graphene.Int(company_name=graphene.String())
    total_company_replies = graphene.Int(company_name=graphene.String())
    overall_company_rating = graphene.Float(company_name=graphene.String())
    reports_per_date = graphene.List(Result, company_name=graphene.String())

    def resolve_companies_names(self, info, **kwargs):
        return CompanyReports.objects.mongo_distinct('company_name')

    def resolve_total_company_reports(self, info, company_name, **kwargs):
        return CompanyReports.objects.mongo_count(
            {'company_name': company_name})

    def resolve_total_company_replies(self, info, company_name, **kwargs):
        return CompanyReports.objects.mongo_count(
            {'company_name': company_name, 'company_replied': True})

    def resolve_overall_company_rating(self, info, company_name, **kwargs):
        result = [i for i in CompanyReports.objects.mongo_aggregate([
            {
                '$match': {
                    'company_name': company_name
                }
            },
            {
                '$group': {
                    '_id': 'null',
                    'average_rating': {
                        '$avg': '$customer_rating'
                    }
                }
            }
        ])]

        return round(result[0]['average_rating'], 2)

    def resolve_reports_per_date(self, info, company_name, **kwargs):
        results = [i for i in CompanyReports.objects.mongo_aggregate([
            {
                '$match': {
                    'company_name': company_name
                }
            },
            {
                '$group': {
                    '_id': {
                        'month': {'$month': '$conclusion_date'},
                        'year': {'$year': '$conclusion_date'}
                    },
                    'count': {'$sum': 1}
                }
            }
        ])]

        results_as_obj_list = []

        for odict in results:
            for key, value in odict.items():
                if key == '_id':
                    month = value["month"]
                    year = value["year"]

                if key == 'count':
                    count = value

            result = Result(year, month, count)
            results_as_obj_list.append(result)

        return results_as_obj_list
