from django.http.response import HttpResponseBadRequest


def clean_tag(uncleaned_tag):
    cleaned_tag = str(uncleaned_tag)
    cleaned_tag = cleaned_tag.lower()
    cleaned_tag = cleaned_tag.strip()
    return cleaned_tag

def get_filename(filename, request):
    return filename.upper()