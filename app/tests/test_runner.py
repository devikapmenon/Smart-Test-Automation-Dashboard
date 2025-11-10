import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

class EnhancedTestRunner:
    def __init__(self):
        self.results = []
    
    async def test_google_homepage(self):
        """Test Google homepage functionality"""
        test_result = {
            'name': 'Google Homepage - Load and Search',
            'status': 'pass',
            'start_time': datetime.now(),
            'error_message': None,
            'steps': []
        }
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Step 1: Load homepage
                test_result['steps'].append('Navigating to Google')
                await page.goto('https://www.google.com', wait_until='networkidle')
                
                # Step 2: Verify page loaded
                title = await page.title()
                test_result['steps'].append(f'Page title: {title}')
                if 'Google' not in title:
                    test_result['status'] = 'fail'
                    test_result['error_message'] = f'Expected "Google" in title, got: {title}'
                
                # Step 3: Test search functionality
                if test_result['status'] == 'pass':
                    test_result['steps'].append('Testing search box')
                    search_box = await page.query_selector('input[name="q"]')
                    if search_box:
                        await search_box.fill('EPAM Systems')
                        await page.keyboard.press('Enter')
                        await page.wait_for_selector('#search', timeout=5000)
                        test_result['steps'].append('Search completed successfully')
                    else:
                        test_result['steps'].append('Search box not found')
                
                await browser.close()
                
        except Exception as e:
            test_result['status'] = 'fail'
            test_result['error_message'] = str(e)
            test_result['steps'].append(f'Error: {str(e)}')
        
        test_result['end_time'] = datetime.now()
        test_result['duration'] = (test_result['end_time'] - test_result['start_time']).total_seconds()
        
        self.results.append(test_result)
        return test_result
    
    async def test_wikipedia_flow(self):
        """Test Wikipedia navigation flow"""
        test_result = {
            'name': 'Wikipedia - Navigation Test',
            'status': 'pass',
            'start_time': datetime.now(),
            'error_message': None,
            'steps': []
        }
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Step 1: Go to Wikipedia main page
                test_result['steps'].append('Loading Wikipedia main page')
                await page.goto('https://www.wikipedia.org', wait_until='networkidle')
                
                # Step 2: Click English version
                test_result['steps'].append('Selecting English Wikipedia')
                english_link = await page.query_selector('#js-link-box-en')
                if english_link:
                    await english_link.click()
                    await page.wait_for_selector('#mp-welcome', timeout=10000)
                    test_result['steps'].append('English Wikipedia loaded')
                else:
                    test_result['status'] = 'fail'
                    test_result['error_message'] = 'English Wikipedia link not found'
                
                # Step 3: Verify we're on English Wikipedia
                if test_result['status'] == 'pass':
                    title = await page.title()
                    test_result['steps'].append(f'English page title: {title}')
                    if 'Wikipedia, the free encyclopedia' not in title:
                        test_result['status'] = 'fail'
                        test_result['error_message'] = 'Not on English Wikipedia homepage'
                
                await browser.close()
                
        except Exception as e:
            test_result['status'] = 'fail'
            test_result['error_message'] = str(e)
            test_result['steps'].append(f'Error: {str(e)}')
        
        test_result['end_time'] = datetime.now()
        test_result['duration'] = (test_result['end_time'] - test_result['start_time']).total_seconds()
        
        self.results.append(test_result)
        return test_result
    
    async def test_ecommerce_demo(self):
        """Test a demo e-commerce website"""
        test_result = {
            'name': 'Demo E-commerce - Product Browse',
            'status': 'pass', 
            'start_time': datetime.now(),
            'error_message': None,
            'steps': []
        }
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Using Sauce Demo (popular test e-commerce site)
                test_result['steps'].append('Loading Sauce Demo website')
                await page.goto('https://www.saucedemo.com', wait_until='networkidle')
                
                # Step 1: Login
                test_result['steps'].append('Attempting login')
                await page.fill('#user-name', 'standard_user')
                await page.fill('#password', 'secret_sauce')
                await page.click('#login-button')
                
                # Step 2: Verify login successful
                await page.wait_for_selector('.inventory_list', timeout=5000)
                products = await page.query_selector_all('.inventory_item')
                test_result['steps'].append(f'Found {len(products)} products')
                
                if len(products) == 0:
                    test_result['status'] = 'fail'
                    test_result['error_message'] = 'No products found after login'
                else:
                    test_result['steps'].append('Login successful, products displayed')
                
                await browser.close()
                
        except Exception as e:
            test_result['status'] = 'fail'
            test_result['error_message'] = str(e)
            test_result['steps'].append(f'Error: {str(e)}')
        
        test_result['end_time'] = datetime.now()
        test_result['duration'] = (test_result['end_time'] - test_result['start_time']).total_seconds()
        
        self.results.append(test_result)
        return test_result
    
    async def run_all_enhanced_tests(self):
        """Run all enhanced test scenarios"""
        tests = [
            self.test_google_homepage(),
            self.test_wikipedia_flow(), 
            self.test_ecommerce_demo()
        ]
        
        results = []
        for test in tests:
            result = await test
            results.append(result)
        
        return results

# Keep the original SimpleTestRunner for backward compatibility
class SimpleTestRunner(EnhancedTestRunner):
    async def run_simple_test(self):
        """Backward compatibility - runs just the Google test"""
        return await self.test_google_homepage()