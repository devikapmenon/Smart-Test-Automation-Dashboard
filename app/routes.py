from flask import Blueprint, render_template, jsonify, request
from app import db
from app.models import TestRun, TestCase
from app.tests.test_runner import EnhancedTestRunner
import asyncio
import uuid
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('dashboard.html')

@main.route('/api/test-runs')
def get_test_runs():
    try:
        runs = TestRun.query.order_by(TestRun.start_time.desc()).limit(10).all()
        return jsonify({
            'success': True,
            'test_runs': [run.to_dict() for run in runs]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/run-simple-test', methods=['POST'])
def run_simple_test():
    try:
        test_run = TestRun(
            run_id=str(uuid.uuid4()),
            test_suite="Google Homepage Test",
            status="running",
            start_time=datetime.utcnow()
        )
        db.session.add(test_run)
        db.session.commit()
        
        asyncio.run(execute_simple_test(test_run.id))
        
        return jsonify({
            'success': True,
            'message': 'Google test started successfully',
            'run_id': test_run.run_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/api/run-enhanced-tests', methods=['POST'])
def run_enhanced_tests():
    try:
        test_run = TestRun(
            run_id=str(uuid.uuid4()),
            test_suite="Enhanced Test Suite (3 Websites)",
            status="running", 
            start_time=datetime.utcnow()
        )
        db.session.add(test_run)
        db.session.commit()
        
        asyncio.run(execute_enhanced_tests(test_run.id))
        
        return jsonify({
            'success': True,
            'message': 'Enhanced test suite started successfully',
            'run_id': test_run.run_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

async def execute_simple_test(test_run_id):
    """Execute single Google test"""
    try:
        runner = EnhancedTestRunner()
        result = await runner.test_google_homepage()
        await save_test_results(test_run_id, [result])
    except Exception as e:
        mark_test_failed(test_run_id, str(e))

async def execute_enhanced_tests(test_run_id):
    """Execute all enhanced tests"""
    try:
        runner = EnhancedTestRunner()
        results = await runner.run_all_enhanced_tests()
        await save_test_results(test_run_id, results)
    except Exception as e:
        mark_test_failed(test_run_id, str(e))

async def save_test_results(test_run_id, results):
    """Save test results to database"""
    test_run = TestRun.query.get(test_run_id)
    
    total_tests = len(results)
    passed_tests = len([r for r in results if r['status'] == 'pass'])
    failed_tests = len([r for r in results if r['status'] == 'fail'])
    
    # Determine overall status
    if failed_tests > 0:
        overall_status = 'failed'
    else:
        overall_status = 'passed'
    
    test_run.status = overall_status
    test_run.end_time = datetime.utcnow()
    test_run.duration = sum(r['duration'] for r in results)
    test_run.total_tests = total_tests
    test_run.passed_tests = passed_tests
    test_run.failed_tests = failed_tests
    
    # Save individual test cases
    for result in results:
        test_case = TestCase(
            test_run_id=test_run_id,
            name=result['name'],
            status=result['status'],
            duration=result['duration'],
            error_message=result['error_message']
        )
        db.session.add(test_case)
    
    db.session.commit()
    print(f"✅ Test suite completed: {passed_tests}/{total_tests} tests passed")

def mark_test_failed(test_run_id, error_message):
    """Mark test run as failed"""
    test_run = TestRun.query.get(test_run_id)
    test_run.status = 'failed'
    test_run.end_time = datetime.utcnow()
    test_run.error_message = error_message
    db.session.commit()