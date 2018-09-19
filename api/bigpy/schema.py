import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import CustomerReports


class CustomerReportsFilter(django_filters.FilterSet):
    class Meta:
        model = CustomerReports
        fields = ['company_name', 'user_rating', 'date', 'city', 'state']


class CustomerReportsType(DjangoObjectType):
    class Meta:
        model = CustomerReports
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    customer_report = graphene.relay.Node.Field(CustomerReportsType)
    all_customer_reports = DjangoFilterConnectionField(
        CustomerReportsType, filterset_class=CustomerReportsFilter)
