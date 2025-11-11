"""
LinkedIn message sender integration
Handles sending messages to HR contacts (manual review workflow)
"""
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import config


class LinkedInMessenger:
    """Send messages to LinkedIn contacts"""

    def __init__(self, driver):
        """
        Initialize messenger with existing driver

        Args:
            driver: Selenium WebDriver instance (already logged in)
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def can_message_profile(self, profile_url):
        """
        Check if we can send a message to this profile

        Args:
            profile_url (str): LinkedIn profile URL

        Returns:
            dict: Information about messaging availability
        """
        try:
            self.driver.get(profile_url)
            time.sleep(random.uniform(2, 4))

            # Look for "Message" button
            try:
                message_button = self.driver.find_element(
                    By.XPATH,
                    "//button[contains(@class, 'message') or contains(., 'Message')]"
                )
                return {
                    'can_message': True,
                    'type': 'direct_message',
                    'button_found': True
                }
            except NoSuchElementException:
                pass

            # Check for "Connect" button (need to connect first)
            try:
                connect_button = self.driver.find_element(
                    By.XPATH,
                    "//button[contains(., 'Connect')]"
                )
                return {
                    'can_message': False,
                    'type': 'connection_required',
                    'button_found': True,
                    'action': 'send_connection_request'
                }
            except NoSuchElementException:
                pass

            # Check for InMail option (premium feature)
            try:
                inmail_button = self.driver.find_element(
                    By.XPATH,
                    "//button[contains(., 'InMail')]"
                )
                return {
                    'can_message': True,
                    'type': 'inmail',
                    'requires_premium': True,
                    'button_found': True
                }
            except NoSuchElementException:
                pass

            return {
                'can_message': False,
                'type': 'unknown',
                'button_found': False
            }

        except Exception as e:
            return {
                'can_message': False,
                'error': str(e)
            }

    def send_connection_request(self, profile_url, message=None):
        """
        Send a connection request with optional note

        Args:
            profile_url (str): LinkedIn profile URL
            message (str): Optional connection note (max 300 chars)

        Returns:
            dict: Result of connection request
        """
        try:
            self.driver.get(profile_url)
            time.sleep(random.uniform(2, 4))

            # Find and click Connect button
            connect_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Connect')]"))
            )
            connect_button.click()
            time.sleep(2)

            # If message provided, add note
            if message:
                try:
                    # Click "Add a note" button
                    add_note_button = self.driver.find_element(
                        By.XPATH,
                        "//button[contains(., 'Add a note')]"
                    )
                    add_note_button.click()
                    time.sleep(1)

                    # Enter message (max 300 characters)
                    note_textarea = self.driver.find_element(
                        By.ID,
                        "custom-message"
                    )

                    # Trim message if too long
                    if len(message) > 300:
                        message = message[:297] + "..."

                    note_textarea.send_keys(message)
                    time.sleep(1)

                except NoSuchElementException:
                    print("    Note: Could not add custom message")

            # Click Send button
            send_button = self.driver.find_element(
                By.XPATH,
                "//button[contains(@aria-label, 'Send') or contains(., 'Send')]"
            )
            send_button.click()
            time.sleep(2)

            return {
                'success': True,
                'action': 'connection_request_sent',
                'message_included': message is not None
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def send_direct_message(self, profile_url, message):
        """
        Send a direct message to a connection

        Args:
            profile_url (str): LinkedIn profile URL
            message (str): Message to send

        Returns:
            dict: Result of message sending
        """
        try:
            self.driver.get(profile_url)
            time.sleep(random.uniform(2, 4))

            # Click Message button
            message_button = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@class, 'message') or contains(., 'Message')]"
                ))
            )
            message_button.click()
            time.sleep(2)

            # Find message input box
            message_box = self.wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "div[role='textbox']"
                ))
            )

            # Type message
            message_box.send_keys(message)
            time.sleep(1)

            # Click Send button
            send_button = self.driver.find_element(
                By.XPATH,
                "//button[contains(@type, 'submit') and contains(., 'Send')]"
            )
            send_button.click()
            time.sleep(2)

            return {
                'success': True,
                'action': 'direct_message_sent'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def review_and_send(self, profile, message, auto_send=False):
        """
        Review message before sending (safety feature)

        Args:
            profile (dict): HR profile data
            message (str): Generated message
            auto_send (bool): If True, send without confirmation

        Returns:
            dict: Result of sending
        """
        print(f"\n{'='*60}")
        print(f"To: {profile['name']}")
        print(f"Title: {profile['title']}")
        print(f"URL: {profile['profile_url']}")
        print(f"\nMessage:\n{message}")
        print(f"{'='*60}")

        if not auto_send:
            response = input("\nSend this message? (yes/no/edit/skip): ").lower().strip()

            if response == 'edit':
                print("\nEnter your edited message (press Ctrl+D when done):")
                import sys
                edited_lines = []
                try:
                    while True:
                        line = input()
                        edited_lines.append(line)
                except EOFError:
                    message = '\n'.join(edited_lines)

                # Ask again after editing
                return self.review_and_send(profile, message, auto_send=False)

            elif response == 'skip':
                return {'success': False, 'action': 'skipped_by_user'}

            elif response != 'yes':
                return {'success': False, 'action': 'cancelled_by_user'}

        # Check if we can message
        profile_url = profile['profile_url']
        message_availability = self.can_message_profile(profile_url)

        if message_availability['can_message']:
            if message_availability['type'] == 'direct_message':
                return self.send_direct_message(profile_url, message)
            elif message_availability['type'] == 'inmail':
                print("    Note: This requires InMail (LinkedIn Premium)")
                # InMail sending would go here
                return {'success': False, 'action': 'inmail_required'}
        else:
            # Need to send connection request first
            # Use first 300 chars of message as connection note
            connection_note = message[:300] if len(message) > 300 else message
            return self.send_connection_request(profile_url, connection_note)

    def batch_send_messages(self, messages_data, auto_send=False, delay_range=(10, 20)):
        """
        Send messages to multiple profiles with rate limiting

        Args:
            messages_data (list): List of dicts with 'profile' and 'message'
            auto_send (bool): If True, send without confirmation
            delay_range (tuple): Random delay between messages (min, max) in seconds

        Returns:
            dict: Summary of sending results
        """
        results = {
            'total': len(messages_data),
            'sent': 0,
            'failed': 0,
            'skipped': 0,
            'details': []
        }

        for idx, data in enumerate(messages_data, 1):
            print(f"\n\nProcessing {idx}/{len(messages_data)}...")

            profile = data['profile']
            message = data['message']

            result = self.review_and_send(profile, message, auto_send)
            results['details'].append({
                'profile': profile['name'],
                'result': result
            })

            if result.get('success'):
                results['sent'] += 1
            elif result.get('action') in ['skipped_by_user', 'cancelled_by_user']:
                results['skipped'] += 1
            else:
                results['failed'] += 1

            # Rate limiting - random delay between messages
            if idx < len(messages_data):
                delay = random.uniform(*delay_range)
                print(f"\n    Waiting {delay:.1f} seconds before next message...")
                time.sleep(delay)

        return results


def create_messaging_workflow(scraper_results, messages, output_file='messaging_workflow.json'):
    """
    Create a workflow file with profiles and messages ready for review

    Args:
        scraper_results (list): HR profile data
        messages (list): Generated messages
        output_file (str): Output file path

    Returns:
        str: Path to workflow file
    """
    import json

    workflow = []
    for profile, message_data in zip(scraper_results, messages):
        workflow.append({
            'profile': profile,
            'message': message_data['message'],
            'scenario': message_data['scenario'],
            'status': 'pending',
            'generated_at': message_data['generated_at']
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'workflow': workflow,
            'total_messages': len(workflow),
            'created_at': time.strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=2, ensure_ascii=False)

    print(f"✓ Messaging workflow saved to: {output_file}")
    return output_file
