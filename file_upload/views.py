import os
from io import BytesIO

import pandas as pd
from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from file_upload.Utils.DataProcessing import output_to_excel


class FileUploadViewSet(viewsets.ViewSet):
    parser_classes = (FileUploadParser,)

    def create(self, request, *args, **kwargs):
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

            buffer = BytesIO()
            with pd.ExcelWriter(buffer) as writer:
                data.to_excel(writer, sheet_name='Sheet1', index=False)
            buffer.seek(0)

            response = FileResponse(buffer,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=output.xlsx'

            return response
        except Exception as e:
            return Response({'error': str(e)}, status=400)
