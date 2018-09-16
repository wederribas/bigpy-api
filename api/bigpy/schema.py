import graphene
from graphene_django import DjangoObjectType

from .models import CustomerReports


class CustomerReportsType(DjangoObjectType):
    class Meta:
        model = CustomerReports


class Query(graphene.ObjectType):
    all_customer_reports = graphene.List(CustomerReportsType)

    def resolve_all_customer_reports(self, info, **kwargs):
        return CustomerReports.objects.all()
