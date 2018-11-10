from django.db.models import Avg, Q
import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import CustomerReports, CompanyReports
from .utils import parse_as_graphene_object


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


class CompanyReportsPerDate(graphene.ObjectType):
    year = graphene.String()
    count = graphene.String()


class CompanyReportsCount(graphene.ObjectType):
    company_name = graphene.String()
    count = graphene.String()


class CompanyReportsPerRegion(graphene.ObjectType):
    region = graphene.String()
    count = graphene.String()


class CompanyReportsPerAgeRange(graphene.ObjectType):
    age_range = graphene.String()
    count = graphene.String()


class CompanyRatingPerYear(graphene.ObjectType):
    year = graphene.String()
    average = graphene.String()


class CompanyReportsPerGender(graphene.ObjectType):
    gender = graphene.String()
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

    reports_per_date = graphene.List(
        CompanyReportsPerDate,
        company_name=graphene.String())

    companies_reports_count = graphene.List(CompanyReportsCount)

    company_reports_per_region = graphene.List(
        CompanyReportsPerRegion,
        company_name=graphene.String())

    company_reports_per_age = graphene.List(
        CompanyReportsPerAgeRange,
        company_name=graphene.String())

    company_rating_per_year = graphene.Int(company_name=graphene.String())

    company_rating_per_year = graphene.List(
        CompanyRatingPerYear,
        company_name=graphene.String())

    company_reports_per_gender = graphene.List(
        CompanyReportsPerGender,
        company_name=graphene.String())

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
                        'year': {'$year': '$conclusion_date'}
                    },
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'year': -1}}
        ])]

        return parse_as_graphene_object(
            'year',
            'count',
            results,
            CompanyReportsPerDate
        )

    def resolve_companies_reports_count(self, info, **kwargs):
        results = [i for i in CompanyReports.objects.mongo_aggregate([
            {
                '$group': {
                    '_id': {
                        'company_name': '$company_name'
                    },
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ])]

        return parse_as_graphene_object(
            'company_name',
            'count',
            results,
            CompanyReportsCount
        )

    def resolve_company_reports_per_region(self, info, company_name, **kwargs):
        results = [i for i in CompanyReports.objects.mongo_aggregate([
            {
                '$match': {
                    'company_name': company_name
                }
            },
            {
                '$group': {
                    '_id': {
                        'region': '$region'
                    },
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'count': -1}}
        ])]

        return parse_as_graphene_object(
            'region',
            'count',
            results,
            CompanyReportsPerRegion
        )

    def resolve_company_reports_per_age(self, info, company_name, **kwargs):
        results = [i for i in CompanyReports.objects.mongo_aggregate([
            {
                '$match': {
                    'company_name': company_name
                }
            },
            {
                '$group': {
                    '_id': {
                        'age_range': '$age_range'
                    },
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'count': -1}}
        ])]

        return parse_as_graphene_object(
            'age_range',
            'count',
            results,
            CompanyReportsPerAgeRange
        )

    def resolve_company_rating_per_year(self, info, company_name, **kwargs):
        results = [i for i in CompanyReports.objects.mongo_aggregate([
            {
                '$match': {
                    'company_name': company_name
                }
            },
            {
                '$group': {
                    '_id': {
                        'year': {'$year': '$conclusion_date'},
                    },
                    'average': {'$avg': '$customer_rating'}
                }
            },
            {'$sort': {'year': -1}}
        ])]

        return parse_as_graphene_object(
            'year',
            'average',
            results,
            CompanyRatingPerYear
        )

    def resolve_company_reports_per_gender(self, info, company_name, **kwargs):
        results = [i for i in CompanyReports.objects.mongo_aggregate([
            {
                '$match': {
                    'company_name': company_name
                }
            },
            {
                '$group': {
                    '_id': {
                        'gender': '$gender',
                    },
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'gender': -1}}
        ])]

        return parse_as_graphene_object(
            'gender',
            'count',
            results,
            CompanyReportsPerGender
        )
