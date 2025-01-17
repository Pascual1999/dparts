from datetime import date
import json


from django.db.models import Sum, Count, Max
from django.db.models.functions import ExtractMonth, ExtractDay, ExtractYear


from orders.models import Order, OrderItem


def total_orders(request):
    if request.user.is_authenticated:
        return {'total_orders': Order.objects.all().count()}
    else:
        return {'total_orders': 0}


def total_completed_orders(request):
    if request.user.is_authenticated:
        filterBy = request.GET.get('filterBy')
        data = 0

        if filterBy == 'this-month':
            data = Order.objects.filter(
                status=Order.COMPLETED,
                updated_at__year=date.today().year,
                updated_at__month=date.today().month
            ).count()

        elif filterBy == 'this-year':
            data = Order.objects.filter(
                status=Order.COMPLETED,
                updated_at__year=date.today().year
            ).count()

        elif filterBy == 'all':
            data = Order.objects.filter(
                status=Order.COMPLETED
            ).count()

        return {'total_completed_orders': data}

    else:
        return {'total_completed_orders': 0}


def total_pending_orders(request):
    if request.user.is_authenticated:
        filterBy = request.GET.get('filterBy')
        data = 0
        if filterBy == 'this-month':
            data = Order.objects.filter(
                status=Order.IN_PROGRESS,
                updated_at__year=date.today().year,
                updated_at__month=date.today().month
            ).count()

        elif filterBy == 'this-year':
            data = Order.objects.filter(
                status=Order.IN_PROGRESS,
                updated_at__year=date.today().year
            ).count()
        
        elif filterBy == 'all':
            data = Order.objects.filter(
                status=Order.IN_PROGRESS
            ).count()

        return {'total_pending_orders': data}

    else:
        return {'total_pending_orders': 0}


def total_cancelled_orders(request):
    if request.user.is_authenticated:
        filterBy = request.GET.get('filterBy')
        data = 0
        if filterBy == 'this-month':
            data = Order.objects.filter(
                status=Order.CANCELLED,
                updated_at__year=date.today().year,
                updated_at__month=date.today().month
            ).count()
        
        elif filterBy == 'this-year':
            data = Order.objects.filter(
                status=Order.CANCELLED,
                updated_at__year=date.today().year
            ).count()
        
        elif filterBy == 'all':
            data = Order.objects.filter(
                status=Order.CANCELLED
            ).count()
        
        return {'total_cancelled_orders': data}
    else:
        return {'total_cancelled_orders': 0}


def total_paid_orders(request):
    if request.user.is_authenticated:
        filterBy = request.GET.get('filterBy')
        data = 0

        if filterBy == 'this-month':
            data = Order.objects.filter(
                status=Order.PAID,
                updated_at__year=date.today().year,
                updated_at__month=date.today().month
            ).count()

        elif filterBy == 'this-year':
            data = Order.objects.filter(
                status=Order.PAID,
                updated_at__year=date.today().year
            ).count()
        
        elif filterBy == 'all':
            data = Order.objects.filter(
                status=Order.PAID
            ).count()

        return {'total_paid_orders': data}
    else:
        return {'total_paid_orders': 0}


def top10_products(request):
    if request.user.is_authenticated:
        filterBy = request.GET.get('filterBy')
        datalist = []

        if filterBy == 'this-month':
            queryset = OrderItem.objects.filter(
                order__status=Order.COMPLETED,
                order__updated_at__month=date.today().month,
                order__updated_at__year=date.today().year
                )
            data = queryset.values('product_name').annotate(
                total_quantity=Sum('quantity')
                ).order_by('-total_quantity')[:10]
            for item in data:
                datalist.append(
                    {
                        'x': item['product_name'],
                        'y': item['total_quantity']
                    })
        elif filterBy == 'this-year':
            queryset = OrderItem.objects.filter(
                order__status=Order.COMPLETED,
                order__updated_at__year=date.today().year
            )
            data = queryset.values('product_name').annotate(
                total_quantity=Sum('quantity')
                ).order_by('-total_quantity')[:10]
            for item in data:
                datalist.append(
                    {
                        'x': item['product_name'],
                        'y': item['total_quantity']
                    })
        
        elif filterBy == 'all':
            queryset = OrderItem.objects.filter(
                order__status=Order.COMPLETED,
                )
            data = queryset.values('product_name').annotate(
                total_quantity=Sum('quantity')
                ).order_by('-total_quantity')[:10]
            for item in data:
                datalist.append(
                    {
                        'x': item['product_name'],
                        'y': item['total_quantity']
                    })
        return {'top10_products': json.dumps(datalist)}
    else:
        return {'top10_products': 0}


MONTHS = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
          'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

FILTERS = {
    "this-month": "Este Mes",
    "this-year": "Este Año",
    "all": "Todos Los Tiempos"
}


def orders_through_year(request,):
    if request.user.is_authenticated:

        year = date.today().year
        filterBy = request.GET.get('filterBy') or 'all'
        dataframe = []
        datadict = {}
        if filterBy == 'this-month':
            orders = Order.objects.filter(
                status=Order.COMPLETED,
                updated_at__gte=date.today().replace(day=1)
            )

            dataframe = orders.annotate(
                day=ExtractDay('updated_at')
                ).values('day').annotate(
                    count=Count('id')
                )
            dataframe = dataframe.order_by('day').values(
                'day', 'count')
            max = dataframe.aggregate(Max('day')).get('day__max')
            for index in range(dataframe.count()):
                count = 0
                entry = dataframe[index:index + 1].get()
                count = entry['count']
                day = entry['day']
                datadict.update({
                    day: count
                })
            for i in range(1, max):
                if i not in datadict:
                    datadict.update({i: 0})
            datadict = dict(sorted(datadict.items()))

        elif filterBy == 'this-year':
            orders = Order.objects.filter(
                status=Order.COMPLETED,
                updated_at__year=year
            )
            
            dataframe = orders.annotate(
                month=ExtractMonth('updated_at')
                ).values('month').annotate(
                    count=Count('id')
                ).order_by('month')
            for i in range(dataframe.count()):
                datadict.update({
                    MONTHS[dataframe[i]['month'] - 1]: dataframe[i]['count']
                })
        elif filterBy == 'all':
            orders = Order.objects.filter(
                status=Order.COMPLETED
            )
            
            dataframe = orders.annotate(
                year=ExtractYear('updated_at')
                ).values('year').annotate(
                    count=Count('id')
                ).order_by('year')
            for i in range(dataframe.count()):
                datadict.update({
                    dataframe[i]['year']: dataframe[i]['count']
                })

        return {'orders_through_year': json.dumps(list(datadict.values())),
                'labels': json.dumps(list(datadict.keys())),
                'filterBy': filterBy,
                'currentMonth': MONTHS[date.today().month - 1],
                'currentYear': year,
                'filterText': FILTERS[filterBy]}
    else:
        return {'orders_through_year': 0}
