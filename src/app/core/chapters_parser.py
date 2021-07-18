import epub_meta
from .models import Chapter

def parse_chapters(path):
    data = epub_meta.get_epub_metadata(path, read_toc=True)
    chapters = data['toc']
    result = []
    for c in chapters:
        result.append({
            'index': c['index'],
            'title': c['title']
        })
    return result


def create_chapters(path):
    data = parse_chapters(path)
    for c in data:
        Chapter.objects.create(name=c['title'], index=int(c['index'])) 