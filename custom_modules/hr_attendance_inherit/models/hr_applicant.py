from odoo import models, api
import re
import logging
import phonenumbers
import fitz  # PyMuPDF
import docx

_logger = logging.getLogger(__name__)

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        _logger.info("Custom processing of incoming email for recruitment")

        if custom_values is None:
            custom_values = {}

        email_body = msg_dict.get('body', '')
        email_subject = msg_dict.get('subject', '')
        from_email = msg_dict.get('from', '')
        attachments = msg_dict.get('attachments', [])
        _logger.info(f"Email received from: {from_email}")
        _logger.info(f"Email subject: {email_subject}")
        _logger.info(f"Email body: {email_body[:1000]}...")  # Log the first 1000 characters of the email body

        # Extract phone number
        phone_number = self._extract_phone_number(email_body)
        if phone_number:
            custom_values['partner_phone'] = phone_number
            _logger.info(f"Extracted phone number: {phone_number}")

        # Determine job position from email subject or body
        job_id = self._extract_job_id(email_subject, email_body)
        if job_id:
            custom_values['job_id'] = job_id
            _logger.info(f"Linked to job position ID: {job_id}")
        else:
            _logger.warning("Job position could not be linked")

        # Extract info from attachments
        for attachment in attachments:
            _logger.info(f"Processing attachment: {attachment}")
            # Check if the attachment is a tuple
            if isinstance(attachment, tuple) and len(attachment) == 3:
                filename, mimetype, content = attachment
                _logger.info(f"Filename: {filename}, Mimetype: {mimetype}")

                if mimetype == 'application/pdf':
                    extracted_info = self._extract_info_from_pdf(content)
                elif mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    extracted_info = self._extract_info_from_docx(content)
                else:
                    continue  # Skip unsupported file types

                if extracted_info:
                    _logger.info(f"Extracted info from attachment: {extracted_info}")
                    if 'phone_number' in extracted_info and not custom_values.get('partner_phone'):
                        custom_values['partner_phone'] = extracted_info['phone_number']
                    if 'email' in extracted_info and not custom_values.get('email_from'):
                        custom_values['email_from'] = extracted_info['email']
                    if 'full_name' in extracted_info and not custom_values.get('partner_name'):
                        custom_values['partner_name'] = extracted_info['full_name']
            else:
                _logger.warning("Attachment structure is not as expected.")

        # Call the super method to create the applicant with custom values
        return super(HrApplicant, self).message_new(msg_dict, custom_values)

    def _extract_phone_number(self, text):
        _logger.info("Extracting phone number from email content")
        phone_number_regex = re.compile(r'\+?\d[\d -]{8,}\d')
        matches = phone_number_regex.findall(text)
        for number in matches:
            try:
                parsed_number = phonenumbers.parse(number, None)
                if phonenumbers.is_valid_number(parsed_number):
                    return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            except phonenumbers.phonenumberutil.NumberParseException:
                _logger.warning(f"Invalid phone number found: {number}")
        return None

    def _extract_job_id(self, subject, body):
        _logger.info("Extracting job ID from email content")

        # Improved regex to match various ways job titles can be mentioned
        job_title_regex = re.compile(r'\b(?:position|job title|role):?\s*([A-Za-z\s]+)', re.IGNORECASE)
        _logger.info(f"Regex pattern used for job title extraction: {job_title_regex.pattern}")

        match = job_title_regex.search(subject) or job_title_regex.search(body)
        if match:
            job_title = match.group(1).strip()
            _logger.info(f"Extracted job title: {job_title}")

            # Log all job titles in the system for comparison
            jobs = self.env['hr.job'].search([])
            for job in jobs:
                _logger.info(f"Job in system: {job.name}")

            job = self.env['hr.job'].search([('name', 'ilike', job_title)], limit=1)
            if job:
                _logger.info(f"Found job position: {job.name}")
                return job.id
            else:
                _logger.warning(f"No job found for title: {job_title}")
        else:
            _logger.warning("Job position not found in email content")
        return None

    def _extract_info_from_pdf(self, pdf_content):
        pdf_document = fitz.open("pdf", pdf_content)
        text = ''
        for page in pdf_document:
            text += page.get_text()

        return self._parse_extracted_text(text)

    def _extract_info_from_docx(self, docx_content):
        doc = docx.Document(docx_content)
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'

        return self._parse_extracted_text(text)

    def _parse_extracted_text(self, text):
        info = {}
        info['phone_number'] = self._extract_phone_number(text)
        info['email'] = self._extract_email(text)
        info['full_name'] = self._extract_fuffll_name(text)
        return info

    def _extract_email(self, text):
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        match = email_pattern.search(text)
        if match:
            return match.group(0)
        return ''

    def _extract_full_name(self, text):
        # Basic heuristic for extracting name; customize as needed
        lines = text.split('\n')
        for line in lines:
            if re.match(r'^[A-Za-z ]+$', line) and len(line.split()) >= 2:
                return line.strip()
        return ''
