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


class Query(graphene.ObjectType):
    customer_report = graphene.relay.Node.Field(CustomerReportsType)
    all_customer_reports = DjangoFilterConnectionField(
        CustomerReportsType, filterset_class=CustomerReportsFilter)

    company_report = graphene.relay.Node.Field(CompanyReportsType)
    all_company_reports = DjangoFilterConnectionField(
        CompanyReportsType, filterset_class=CompanyReportsFilter)

    companies_names = graphene.List(graphene.String)

    total_company_reports = graphene.Int(company_name=graphene.String())

    def resolve_companies_names(self, info, **kwargs):
        return CompanyReports.objects.mongo_distinct('company_name')

    def resolve_total_company_reports(self, info, company_name, **kwargs):
        return CompanyReports.objects.mongo_count({'company_name': company_name})
