from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum


def read_add_numm(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' %(ct.model, obj.pk)
    if not request.COOKIES.get(key):
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            # 存在这个字段
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
    return key
