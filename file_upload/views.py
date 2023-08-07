import os

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd

from file_upload.utils.DataProcessing import output_to_excel


class FileUploadView(APIView):
    """
    API endpoint that allows users to upload a file.
    """
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')

        if not file_obj:
            return Response({'error': 'No file received'}, status=400)

        # Get the file's extension
        file_extension = os.path.splitext(file_obj.name)[1].lower()
        # Verify file type
        allowed_extensions = ['.xlsx', '.xls', '.csv']
        if file_extension not in allowed_extensions:
            return Response({'error': 'Invalid file type. Only Excel (.xls/.xlsx) and CSV (.csv) files are allowed.'},
                            status=400)

        try:
            df = pd.read_excel(file_obj, engine='openpyxl') if file_extension in ['.xlsx', '.xls'] else pd.read_csv(
                file_obj)
            data = output_to_excel(df)

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename=output.xlsx'
            with pd.ExcelWriter('output.xlsx') as writer:
                data.to_excel(writer, sheet_name='Sheet1', index=False)

            return Response({'message': file_obj.name}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
