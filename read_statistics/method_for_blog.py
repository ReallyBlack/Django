from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum, ReadDetail
from django.utils import timezone
from django.db.models import Sum
import datetime


def read_add_numm(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' %(ct.model, obj.pk)
    if not request.COOKIES.get(key):
        # 阅读数增加
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        date = timezone.now().date()
        # 日阅读数增加
        read_detail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        read_detail.read_num += 1
        read_detail.save()
    return key


def get_a_week_read_date(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m-%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum']or 0)
    return dates, read_nums


def get_hot_blog(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[0:3]
