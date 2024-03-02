import os
import io
from django.core.management.base import BaseCommand
from pdf_to_word.models import ConversionRecord

class Command(BaseCommand):
    help = 'Extract and save PDF files to base_dir/media/pdfs folder'

    def handle(self, *args, **options):
        destination_folder = os.path.join('base_dir', 'media', 'pdfs')

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        conversion_records = ConversionRecord.objects.all()

        for record in conversion_records:
            pdf_content = record.pdf_content

            if pdf_content:
                try:
                    if isinstance(pdf_content, bytes):  # Check if the content is a bytes-like object
                        import fitz  # PyMuPDF library
                        pdf_document = fitz.open(stream=pdf_content)
                        if pdf_document.page_count > 0:
                            # PDF is valid
                            destination_path = os.path.join(destination_folder, f"{record.pk}.pdf")

                            with open(destination_path, 'wb') as destination_file:
                                destination_file.write(pdf_content)

                            self.stdout.write(self.style.SUCCESS(f'Successfully extracted PDF for record {record.pk}'))
                        else:
                            self.stdout.write(self.style.WARNING(f'Invalid PDF content for record {record.pk}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Invalid PDF content type for record {record.pk}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error processing record {record.pk}: {str(e)}'))
            else:
                self.stdout.write(self.style.WARNING(f'PDF content not found or empty for record {record.pk}'))
