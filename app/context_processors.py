
from .models import Tag

def all_tags_processor(request):
    tags = Tag.objects.all()
    return {'all_tags' : tags}