"""
Data export functionality for LinkedIn scraper results
"""
import json
import csv
import os
from datetime import datetime
import pandas as pd
import config


class DataExporter:
    """Handle exporting scraped data to various formats"""

    def __init__(self, output_dir=None):
        """
        Initialize data exporter

        Args:
            output_dir (str): Directory to save output files
        """
        self.output_dir = output_dir or config.OUTPUT_DIRECTORY
        self._ensure_output_directory()

    def _ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"✓ Created output directory: {self.output_dir}")

    def _generate_filename(self, company_name, extension):
        """Generate filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_company_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_company_name = safe_company_name.replace(' ', '_')
        filename = f"linkedin_hr_{safe_company_name}_{timestamp}.{extension}"
        return os.path.join(self.output_dir, filename)

    def export_to_csv(self, data, company_name):
        """
        Export data to CSV format

        Args:
            data (list): List of dictionaries containing profile data
            company_name (str): Company name for filename

        Returns:
            str: Path to saved file
        """
        if not data:
            print("⚠ No data to export")
            return None

        filepath = self._generate_filename(company_name, 'csv')

        try:
            # Define fieldnames
            fieldnames = ['name', 'title', 'location', 'profile_url']

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            print(f"✓ Data exported to CSV: {filepath}")
            return filepath

        except Exception as e:
            print(f"✗ Error exporting to CSV: {str(e)}")
            return None

    def export_to_json(self, data, company_name):
        """
        Export data to JSON format

        Args:
            data (list): List of dictionaries containing profile data
            company_name (str): Company name for filename

        Returns:
            str: Path to saved file
        """
        if not data:
            print("⚠ No data to export")
            return None

        filepath = self._generate_filename(company_name, 'json')

        try:
            export_data = {
                'company': company_name,
                'scraped_at': datetime.now().isoformat(),
                'total_profiles': len(data),
                'profiles': data
            }

            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)

            print(f"✓ Data exported to JSON: {filepath}")
            return filepath

        except Exception as e:
            print(f"✗ Error exporting to JSON: {str(e)}")
            return None

    def export_to_excel(self, data, company_name):
        """
        Export data to Excel format

        Args:
            data (list): List of dictionaries containing profile data
            company_name (str): Company name for filename

        Returns:
            str: Path to saved file
        """
        if not data:
            print("⚠ No data to export")
            return None

        filepath = self._generate_filename(company_name, 'xlsx')

        try:
            # Create DataFrame
            df = pd.DataFrame(data)

            # Reorder columns
            columns_order = ['name', 'title', 'location', 'profile_url']
            df = df[columns_order]

            # Export to Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='HR Contacts', index=False)

                # Auto-adjust column widths
                worksheet = writer.sheets['HR Contacts']
                for idx, col in enumerate(df.columns):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(col)
                    )
                    worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)

            print(f"✓ Data exported to Excel: {filepath}")
            return filepath

        except Exception as e:
            print(f"✗ Error exporting to Excel: {str(e)}")
            return None

    def export(self, data, company_name, format_type=None):
        """
        Export data to specified format

        Args:
            data (list): List of dictionaries containing profile data
            company_name (str): Company name for filename
            format_type (str): Export format (csv, json, excel)

        Returns:
            str: Path to saved file
        """
        format_type = format_type or config.EXPORT_FORMAT

        if format_type.lower() == 'csv':
            return self.export_to_csv(data, company_name)
        elif format_type.lower() == 'json':
            return self.export_to_json(data, company_name)
        elif format_type.lower() in ['excel', 'xlsx']:
            return self.export_to_excel(data, company_name)
        else:
            print(f"⚠ Unknown format: {format_type}. Defaulting to CSV.")
            return self.export_to_csv(data, company_name)

    def export_all_formats(self, data, company_name):
        """
        Export data to all available formats

        Args:
            data (list): List of dictionaries containing profile data
            company_name (str): Company name for filename

        Returns:
            dict: Paths to all saved files
        """
        results = {
            'csv': self.export_to_csv(data, company_name),
            'json': self.export_to_json(data, company_name),
            'excel': self.export_to_excel(data, company_name)
        }
        return results
