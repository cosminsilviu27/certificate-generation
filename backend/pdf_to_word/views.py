from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.core.serializers import serialize

# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator

from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
import os
import logging
from .models import ConversionRecord
from pdf2docx import Converter

logger = logging.getLogger(__name__)

@api_view(['GET'])
# @cache_page(60 * 15)
def list_word_files(request):
    print(request.user)
    files = ConversionRecord.objects.filter(user=request.user).values(
    'id', 'word_file_name', 'timestamp', 'status'
)
    return JsonResponse(list(files), safe=False)

@api_view(['GET'])
def user_data(request, email):
    try:
        conversion_record = ConversionRecord.objects.get(email=email).values(
            'id', 'email', 'first_name', 'last_name'
        )

        return JsonResponse(conversion_record, safe=False)
    except ConversionRecord.DoesNotExist:
        return JsonResponse({'error': 'Record not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_pdf(request):
    pdf_file = request.FILES.get('pdf_file')
    if not pdf_file:
        return Response({'error': 'PDF file not found in the request.'}, status=status.HTTP_400_BAD_REQUEST)

    pdf_file_name = pdf_file.name
    temp_pdf_path = default_storage.save('temp_pdf.pdf', pdf_file)
    full_temp_pdf_path = os.path.join(settings.MEDIA_ROOT, temp_pdf_path)
    word_file_path = full_temp_pdf_path.replace('.pdf', '.docx')

    try:
        cv = Converter(full_temp_pdf_path)
        cv.convert(word_file_path)
        cv.close()

        with open(word_file_path, 'rb') as word_file:
            ConversionRecord.objects.create(
                user=request.user,
                pdf_file=pdf_file.read(),
                pdf_file_name=pdf_file_name,
                word_file=word_file.read(),
                word_file_name=pdf_file_name.replace('.pdf', '.docx')
            )
    except Exception as e:
        logger.error(f'Error in processing PDF file: {e}', exc_info=True)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        for path in [temp_pdf_path, word_file_path]:
            if path and os.path.exists(path):
                os.remove(path)

    return Response({'message': 'PDF file uploaded and converted successfully.'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def download_word(request, pk):
    try:
        conversion_record = ConversionRecord.objects.get(pk=pk)
        if conversion_record.word_file:
            response = HttpResponse(conversion_record.word_file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{conversion_record.word_file_name}"'
            return response
        return HttpResponse("File not found", status=404)
    except ConversionRecord.DoesNotExist:
        return HttpResponse("Record not found", status=404)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_word(request, pk):
    try:
        conversion_record = ConversionRecord.objects.get(pk=pk, user=request.user)

        conversion_record.delete()
        return Response({'message': 'File deleted successfully'}, status=status.HTTP_200_OK)
    except ConversionRecord.DoesNotExist:
        return Response({'error': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f'Error in deleting file: {e}', exc_info=True)
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
