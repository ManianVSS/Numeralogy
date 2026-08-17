import csv
import os
import re
from pathlib import Path

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from docx import Document
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NameEntry
from .serializers import NameEntrySerializer, UploadSerializer


def parse_text_file(path):
    with open(path, encoding='utf-8') as handle:
        return [line.strip() for line in handle if line.strip()]


def parse_csv_file(path):
    with open(path, encoding='utf-8') as handle:
        reader = csv.reader(handle)
        return [row[0].strip() for row in reader if row and row[0].strip()]


def parse_docx_file(path):
    document = Document(path)
    names = []
    for para in document.paragraphs:
        text = para.text.strip()
        if text:
            names.append(text)
    return names


def normalize_name(name):
    cleaned = re.sub(r'[^A-Za-z\s]', '', name)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def parse_uploaded_file(file_path):
    suffix = Path(file_path).suffix.lower()
    if suffix == '.txt':
        return [normalize_name(name) for name in parse_text_file(file_path) if normalize_name(name)]
    if suffix == '.csv':
        return [normalize_name(name) for name in parse_csv_file(file_path) if normalize_name(name)]
    if suffix == '.docx':
        return [normalize_name(name) for name in parse_docx_file(file_path) if normalize_name(name)]
    return []


def parse_names_text(names_text):
    return [normalize_name(line) for line in names_text.splitlines() if normalize_name(line)]


def build_existing_name_keys():
    return {name.casefold() for name in NameEntry.objects.values_list('name', flat=True)}


def create_name_entry_if_new(name, source_file, existing_name_keys):
    if not name:
        return False
    normalized_key = name.casefold()
    if normalized_key in existing_name_keys:
        return False
    NameEntry.objects.create(name=name, source_file=source_file)
    existing_name_keys.add(normalized_key)
    return True


class NameEntryList(generics.ListCreateAPIView):
    serializer_class = NameEntrySerializer

    def get_queryset(self):
        queryset = NameEntry.objects.all()
        prefix = self.request.query_params.get('name_prefix', '').strip()
        total_sum = self.request.query_params.get('sum', '').strip()
        recursive_sum = self.request.query_params.get('recursive_sum', '').strip()

        if prefix:
            queryset = queryset.filter(name__istartswith=prefix)
        if total_sum.isdigit():
            queryset = queryset.filter(sum=int(total_sum))
        if recursive_sum.isdigit():
            queryset = queryset.filter(recursive_sum=int(recursive_sum))

        return queryset


class NameEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = NameEntry.objects.all()
    serializer_class = NameEntrySerializer


class UploadDictionaryView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = UploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data.get('file')
        name_value = serializer.validated_data.get('name', '').strip()
        names_text = serializer.validated_data.get('names', '').strip()

        imported = 0
        existing_name_keys = build_existing_name_keys()
        upload_root = Path(settings.MEDIA_ROOT) / 'uploads'
        upload_root.mkdir(parents=True, exist_ok=True)

        if uploaded_file:
            file_path = upload_root / uploaded_file.name
            with open(file_path, 'wb') as handle:
                for chunk in uploaded_file.chunks():
                    handle.write(chunk)
            names = parse_uploaded_file(file_path)
            for name in names:
                if create_name_entry_if_new(name, uploaded_file.name, existing_name_keys):
                    imported += 1

        if names_text:
            for name in parse_names_text(names_text):
                if create_name_entry_if_new(name, 'manual-names', existing_name_keys):
                    imported += 1

        if name_value:
            normalized_name = normalize_name(name_value)
            if create_name_entry_if_new(normalized_name, 'manual', existing_name_keys):
                imported += 1

        return Response({'imported': imported}, status=status.HTTP_201_CREATED)


class UploadFormView(View):
    def get(self, request, *args, **kwargs):
        name_entries = NameEntry.objects.all()
        prefix = request.GET.get('name_prefix', '').strip()
        total_sum = request.GET.get('sum', '').strip()
        recursive_sum = request.GET.get('recursive_sum', '').strip()

        if prefix:
            name_entries = name_entries.filter(name__istartswith=prefix)
        if total_sum.isdigit():
            name_entries = name_entries.filter(sum=int(total_sum))
        if recursive_sum.isdigit():
            name_entries = name_entries.filter(recursive_sum=int(recursive_sum))

        return render(request, 'numerology/upload.html', {
            'name_entries': name_entries,
        })

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        single_name = request.POST.get('name', '').strip()
        names_text = request.POST.get('names', '').strip()
        source_name = uploaded_file.name if uploaded_file else 'manual'

        if not uploaded_file and not single_name and not names_text:
            return render(request, 'numerology/upload.html', {
                'error': 'Please provide a file, a single name, or multiple names to upload.',
                'name_entries': NameEntry.objects.all(),
            })

        existing_name_keys = build_existing_name_keys()
        upload_root = Path(settings.MEDIA_ROOT) / 'uploads'
        upload_root.mkdir(parents=True, exist_ok=True)

        if uploaded_file:
            file_path = upload_root / uploaded_file.name
            with open(file_path, 'wb') as handle:
                for chunk in uploaded_file.chunks():
                    handle.write(chunk)
            names = parse_uploaded_file(file_path)
            for name in names:
                create_name_entry_if_new(name, source_name, existing_name_keys)

        if names_text:
            for name in parse_names_text(names_text):
                create_name_entry_if_new(name, 'manual-names', existing_name_keys)

        if single_name:
            normalized_name = normalize_name(single_name)
            if normalized_name:
                create_name_entry_if_new(normalized_name, 'manual', existing_name_keys)

        return HttpResponseRedirect(reverse('numerology:upload'))
