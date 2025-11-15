#!/usr/bin/env python3
"""
Test suite for LinkedIn HR Scraper
Tests core functionality without requiring LinkedIn credentials
"""
import unittest
import os
import sys
from validation import (
    validate_company_name,
    validate_email,
    validate_linkedin_url,
    validate_scenario,
    validate_max_results,
    validate_api_key,
    validate_profile,
    sanitize_filename
)


class TestValidation(unittest.TestCase):
    """Test validation functions"""

    def test_company_name_validation(self):
        """Test company name validation"""
        # Valid cases
        self.assertTrue(validate_company_name("Google")[0])
        self.assertTrue(validate_company_name("Microsoft Corporation")[0])
        self.assertTrue(validate_company_name("Company123")[0])
        self.assertTrue(validate_company_name("A-B Company & Co.")[0])

        # Invalid cases
        self.assertFalse(validate_company_name("")[0])
        self.assertFalse(validate_company_name("A")[0])
        self.assertFalse(validate_company_name("@#$%")[0])
        self.assertFalse(validate_company_name("x" * 101)[0])

    def test_email_validation(self):
        """Test email validation"""
        # Valid cases
        self.assertTrue(validate_email("user@example.com")[0])
        self.assertTrue(validate_email("test.user@domain.co.uk")[0])
        self.assertTrue(validate_email("user+tag@example.com")[0])

        # Invalid cases
        self.assertFalse(validate_email("")[0])
        self.assertFalse(validate_email("invalid.email")[0])
        self.assertFalse(validate_email("@example.com")[0])
        self.assertFalse(validate_email("user@")[0])

    def test_linkedin_url_validation(self):
        """Test LinkedIn URL validation"""
        # Valid cases
        self.assertTrue(validate_linkedin_url("https://linkedin.com/in/johndoe")[0])
        self.assertTrue(validate_linkedin_url("http://www.linkedin.com/in/janesmith")[0])

        # Invalid cases
        self.assertFalse(validate_linkedin_url("")[0])
        self.assertFalse(validate_linkedin_url("https://facebook.com/profile")[0])
        self.assertFalse(validate_linkedin_url("ftp://linkedin.com/in/user")[0])

    def test_scenario_validation(self):
        """Test scenario validation"""
        # Valid cases
        self.assertTrue(validate_scenario("job_seeker")[0])
        self.assertTrue(validate_scenario("networking")[0])
        self.assertTrue(validate_scenario("recruiter_outreach")[0])
        self.assertTrue(validate_scenario("informational_interview")[0])

        # Invalid cases
        self.assertFalse(validate_scenario("")[0])
        self.assertFalse(validate_scenario("invalid_scenario")[0])

    def test_max_results_validation(self):
        """Test max results validation"""
        # Valid cases
        self.assertTrue(validate_max_results(1)[0])
        self.assertTrue(validate_max_results(50)[0])
        self.assertTrue(validate_max_results(500)[0])

        # Invalid cases
        self.assertFalse(validate_max_results(0)[0])
        self.assertFalse(validate_max_results(-1)[0])
        self.assertFalse(validate_max_results(501)[0])

    def test_api_key_validation(self):
        """Test API key validation"""
        # OpenAI valid cases
        self.assertTrue(validate_api_key("sk-" + "x" * 40, "openai")[0])

        # OpenAI invalid cases
        self.assertFalse(validate_api_key("", "openai")[0])
        self.assertFalse(validate_api_key("invalid_key", "openai")[0])
        self.assertFalse(validate_api_key("sk-short", "openai")[0])
        self.assertFalse(validate_api_key("your_openai_api_key_here", "openai")[0])

        # Anthropic valid cases
        self.assertTrue(validate_api_key("sk-ant-" + "x" * 40, "anthropic")[0])

        # Anthropic invalid cases
        self.assertFalse(validate_api_key("", "anthropic")[0])
        self.assertFalse(validate_api_key("sk-wrong-prefix", "anthropic")[0])

    def test_profile_validation(self):
        """Test profile validation"""
        # Valid profile
        valid_profile = {
            'name': 'John Doe',
            'title': 'HR Manager at Google',
            'location': 'San Francisco',
            'profile_url': 'https://linkedin.com/in/johndoe'
        }
        self.assertTrue(validate_profile(valid_profile)[0])

        # Invalid profiles
        self.assertFalse(validate_profile({})[0])
        self.assertFalse(validate_profile({'name': 'John'})[0])  # Missing title
        self.assertFalse(validate_profile({'name': '', 'title': 'Manager'})[0])  # Empty name
        self.assertFalse(validate_profile({'name': 'LinkedIn Member', 'title': 'Manager'})[0])  # Invalid name

    def test_filename_sanitization(self):
        """Test filename sanitization"""
        self.assertEqual(sanitize_filename("normal_file.txt"), "normal_file.txt")
        self.assertEqual(sanitize_filename("file<>:name.txt"), "file___name.txt")
        self.assertEqual(sanitize_filename("  file.txt  "), "file.txt")
        self.assertTrue(len(sanitize_filename("x" * 300)) <= 200)


class TestMessageGeneration(unittest.TestCase):
    """Test message generation"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_profile = {
            'name': 'Jane Smith',
            'title': 'Senior HR Manager at Google',
            'location': 'San Francisco Bay Area',
            'profile_url': 'https://linkedin.com/in/janesmith'
        }

        self.custom_data = {
            'your_role': 'Software Engineer',
            'years': '5',
            'skills': 'Python, React, AWS',
            'industry': 'technology'
        }

    def test_template_message_generation(self):
        """Test template-based message generation"""
        from message_generator import MessageGenerator

        generator = MessageGenerator(use_ai=False)
        message = generator.generate_message(
            self.test_profile,
            scenario='job_seeker',
            custom_data=self.custom_data
        )

        # Check message structure
        self.assertIn('recipient_name', message)
        self.assertIn('message', message)
        self.assertIn('char_count', message)
        self.assertIn('scenario', message)

        # Check content
        self.assertEqual(message['recipient_name'], self.test_profile['name'])
        self.assertEqual(message['scenario'], 'job_seeker')
        self.assertGreater(message['char_count'], 0)
        self.assertIsInstance(message['message'], str)

    def test_bulk_message_generation(self):
        """Test bulk message generation"""
        from message_generator import MessageGenerator

        profiles = [self.test_profile] * 3  # Generate 3 messages

        generator = MessageGenerator(use_ai=False)
        messages = generator.generate_bulk_messages(
            profiles,
            scenario='networking',
            custom_data=self.custom_data
        )

        self.assertEqual(len(messages), 3)
        for message in messages:
            self.assertIn('message', message)
            self.assertGreater(message['char_count'], 0)


class TestDataExport(unittest.TestCase):
    """Test data export functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_data = [
            {
                'name': 'John Doe',
                'title': 'HR Manager at Microsoft',
                'location': 'Seattle, WA',
                'profile_url': 'https://linkedin.com/in/johndoe'
            },
            {
                'name': 'Jane Smith',
                'title': 'Recruiter at Amazon',
                'location': 'New York, NY',
                'profile_url': 'https://linkedin.com/in/janesmith'
            }
        ]

    def test_csv_export(self):
        """Test CSV export"""
        from data_exporter import DataExporter

        exporter = DataExporter()
        file_path = exporter.export_to_csv(self.test_data, "TestCompany")

        self.assertIsNotNone(file_path)
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(file_path.endswith('.csv'))

        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_json_export(self):
        """Test JSON export"""
        from data_exporter import DataExporter

        exporter = DataExporter()
        file_path = exporter.export_to_json(self.test_data, "TestCompany")

        self.assertIsNotNone(file_path)
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(file_path.endswith('.json'))

        # Verify JSON structure
        import json
        with open(file_path, 'r') as f:
            data = json.load(f)
            self.assertIn('profiles', data)
            self.assertIn('company', data)
            self.assertEqual(len(data['profiles']), 2)

        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_excel_export(self):
        """Test Excel export"""
        from data_exporter import DataExporter

        exporter = DataExporter()
        file_path = exporter.export_to_excel(self.test_data, "TestCompany")

        self.assertIsNotNone(file_path)
        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(file_path.endswith('.xlsx'))

        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)


class TestConfig(unittest.TestCase):
    """Test configuration"""

    def test_config_loaded(self):
        """Test that config loads without errors"""
        import config

        # Check required settings exist
        self.assertIsNotNone(config.LINKEDIN_EMAIL)
        self.assertIsNotNone(config.LINKEDIN_PASSWORD)
        self.assertIsNotNone(config.OUTPUT_DIRECTORY)
        self.assertIsInstance(config.HR_KEYWORDS, list)
        self.assertGreater(len(config.HR_KEYWORDS), 0)

    def test_hr_keywords(self):
        """Test HR keywords are valid"""
        import config

        for keyword in config.HR_KEYWORDS:
            self.assertIsInstance(keyword, str)
            self.assertGreater(len(keyword), 0)


class TestLogging(unittest.TestCase):
    """Test logging functionality"""

    def test_logger_creation(self):
        """Test logger can be created"""
        from logger import get_logger

        logger = get_logger('test_logger')
        self.assertIsNotNone(logger)

    def test_logging_methods(self):
        """Test logging methods work"""
        from logger import get_logger

        logger = get_logger('test_logger')

        # These should not raise exceptions
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")
        logger.debug("Test debug message")


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestMessageGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestDataExport))
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestLogging))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
