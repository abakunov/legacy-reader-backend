import epub_meta

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
    print('jdnfhdbvhnbfdvfb')
    data = parse_chapters(path)
    print(1111111)
    for c in data:
        print(222222222)
        Chapter.objects.create(name=c['title'], index=int(c['index'])) 