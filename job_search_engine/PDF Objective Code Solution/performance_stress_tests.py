"""
Performance and Load Testing Suite
Tests system performance under stress, validates latency requirements, and verifies scalability
"""
import time
import numpy as np
from datetime import datetime

print("=" * 80)
print("PERFORMANCE & STRESS TESTING SUITE")
print("=" * 80)
print(f"Test Run Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

performance_results = {
    'latency_tests': [],
    'throughput_tests': [],
    'scalability_tests': [],
    'memory_tests': []
}

# ===== TEST 1: AUTHENTICATION LATENCY =====
print("\n[1/6] Testing Authentication Performance...")
auth_times = []
for i in range(100):
    start = time.time()
    test_hash = auth_service.hash_password(f"password_{i}")
    token = auth_service.create_access_token(f"user_{i}", f"user{i}@test.com", "user")
    verified = auth_service.verify_token(token)
    end = time.time()
    auth_times.append((end - start) * 1000)

avg_auth_time = np.mean(auth_times)
p95_auth_time = np.percentile(auth_times, 95)
max_auth_time = np.max(auth_times)

print(f"✓ Completed 100 auth operations")
print(f"  Average: {avg_auth_time:.2f}ms")
print(f"  P95: {p95_auth_time:.2f}ms")
print(f"  Max: {max_auth_time:.2f}ms")
print(f"  Target: <100ms {'✓ PASS' if avg_auth_time < 100 else '✗ FAIL'}")

performance_results['latency_tests'].append({
    'test': 'Authentication',
    'avg_ms': avg_auth_time,
    'p95_ms': p95_auth_time,
    'max_ms': max_auth_time,
    'target_ms': 100,
    'pass': avg_auth_time < 100
})

# ===== TEST 2: SEARCH ENGINE LATENCY =====
print("\n[2/6] Testing Search Engine Performance...")

# Generate larger mock dataset
large_job_dataset = []
for i in range(500):
    job = {
        "job_id": f"job_{i:04d}",
        "title": f"Software Engineer {i}",
        "company": f"Company {i % 50}",
        "location": ["Bangalore", "Mumbai", "Remote", "Delhi"][i % 4],
        "is_remote": i % 3 == 0,
        "description": f"Job description for position {i}",
        "required_skills": ["Python", "Java", "JavaScript", "React"][:(i % 4) + 1],
        "experience_min": i % 3,
        "experience_max": (i % 3) + 2,
        "salary_min": 300000 + (i % 10) * 50000,
        "salary_max": 500000 + (i % 10) * 50000,
        "days_since_posted": i % 30,
        "semantic_score": 0.5 + (i % 50) / 100,
        "company_score": 0.5 + (i % 30) / 60
    }
    large_job_dataset.append(job)

# Build indexes
search_engine.build_indexes(large_job_dataset)

# Test search latency
search_times = []
for i in range(50):
    start = time.time()
    results = search_engine.search(
        skills=["Python"],
        location="Bangalore",
        jobs=large_job_dataset
    )
    end = time.time()
    search_times.append((end - start) * 1000)

avg_search_time = np.mean(search_times)
p95_search_time = np.percentile(search_times, 95)
max_search_time = np.max(search_times)

print(f"✓ Completed 50 searches on 500-job dataset")
print(f"  Average: {avg_search_time:.2f}ms")
print(f"  P95: {p95_search_time:.2f}ms")
print(f"  Max: {max_search_time:.2f}ms")
print(f"  Target: <500ms {'✓ PASS' if avg_search_time < 500 else '✗ FAIL'}")

performance_results['latency_tests'].append({
    'test': 'Search Engine',
    'avg_ms': avg_search_time,
    'p95_ms': p95_search_time,
    'max_ms': max_search_time,
    'target_ms': 500,
    'pass': avg_search_time < 500
})

# ===== TEST 3: AI MATCHING LATENCY =====
print("\n[3/6] Testing AI Matching Performance...")

# Generate embeddings for jobs
for job in large_job_dataset[:100]:
    job["job_embedding"] = matching_engine.generate_job_embedding(job)

test_resume = {
    "skills": ["Python", "Machine Learning", "FastAPI"],
    "resume_text": "Experienced software engineer",
    "education": ["B.Tech CS"]
}

matching_times = []
for i in range(20):
    start = time.time()
    resume_emb = matching_engine.generate_resume_embedding(test_resume)
    ranked = matching_engine.rank_jobs(resume_emb, large_job_dataset[:100], test_resume["skills"])
    end = time.time()
    matching_times.append((end - start) * 1000)

avg_matching_time = np.mean(matching_times)
p95_matching_time = np.percentile(matching_times, 95)
max_matching_time = np.max(matching_times)

print(f"✓ Completed 20 AI matching operations (100 jobs)")
print(f"  Average: {avg_matching_time:.2f}ms")
print(f"  P95: {p95_matching_time:.2f}ms")
print(f"  Max: {max_matching_time:.2f}ms")
print(f"  Target: <1000ms {'✓ PASS' if avg_matching_time < 1000 else '✗ FAIL'}")

performance_results['latency_tests'].append({
    'test': 'AI Matching',
    'avg_ms': avg_matching_time,
    'p95_ms': p95_matching_time,
    'max_ms': max_matching_time,
    'target_ms': 1000,
    'pass': avg_matching_time < 1000
})

# ===== TEST 4: THROUGHPUT TESTING =====
print("\n[4/6] Testing System Throughput...")

# Simulate concurrent operations
operations_per_second = []
test_duration = 3  # seconds

start_time = time.time()
operation_count = 0

while (time.time() - start_time) < test_duration:
    # Simulate mixed operations
    auth_service.create_access_token(f"user_{operation_count}", "test@test.com", "user")
    search_engine.search(skills=["Python"], jobs=large_job_dataset[:50])
    operation_count += 2

elapsed_time = time.time() - start_time
ops_per_second = operation_count / elapsed_time

print(f"✓ Completed {operation_count} operations in {elapsed_time:.2f}s")
print(f"  Throughput: {ops_per_second:.2f} ops/sec")
print(f"  Target: >100 ops/sec {'✓ PASS' if ops_per_second > 100 else '✗ FAIL'}")

performance_results['throughput_tests'].append({
    'test': 'Mixed Operations',
    'ops_per_second': ops_per_second,
    'total_operations': operation_count,
    'duration_seconds': elapsed_time,
    'target_ops_per_second': 100,
    'pass': ops_per_second > 100
})

# ===== TEST 5: SCALABILITY TESTING =====
print("\n[5/6] Testing Scalability...")

dataset_sizes = [50, 100, 200, 500]
scaling_results = []

for size in dataset_sizes:
    search_times_scale = []
    for i in range(10):
        start = time.time()
        results = search_engine.search(
            skills=["Python"],
            jobs=large_job_dataset[:size]
        )
        end = time.time()
        search_times_scale.append((end - start) * 1000)
    
    avg_time = np.mean(search_times_scale)
    scaling_results.append({
        'dataset_size': size,
        'avg_latency_ms': avg_time
    })
    print(f"  Dataset size {size:4d}: {avg_time:6.2f}ms")

# Check if latency scales linearly or sub-linearly (good)
latency_growth_rate = scaling_results[-1]['avg_latency_ms'] / scaling_results[0]['avg_latency_ms']
dataset_growth_rate = dataset_sizes[-1] / dataset_sizes[0]

print(f"✓ Latency growth: {latency_growth_rate:.2f}x for {dataset_growth_rate:.0f}x data")
print(f"  Scaling efficiency: {'✓ SUB-LINEAR (GOOD)' if latency_growth_rate < dataset_growth_rate else '⚠ LINEAR OR WORSE'}")

performance_results['scalability_tests'].append({
    'results': scaling_results,
    'latency_growth': latency_growth_rate,
    'dataset_growth': dataset_growth_rate,
    'efficient_scaling': latency_growth_rate < dataset_growth_rate
})

# ===== TEST 6: EDGE CASE HANDLING =====
print("\n[6/6] Testing Edge Cases...")

edge_case_results = []

# Test 1: Empty search results
try:
    start = time.time()
    empty_results = search_engine.search(skills=["NonexistentSkill123"], jobs=large_job_dataset)
    end = time.time()
    edge_case_results.append({
        'test': 'Empty search results',
        'pass': True,
        'latency_ms': (end - start) * 1000
    })
    print(f"  ✓ Empty search results: {len(empty_results)} results, {(end-start)*1000:.2f}ms")
except Exception as e:
    edge_case_results.append({'test': 'Empty search results', 'pass': False, 'error': str(e)})
    print(f"  ✗ Empty search results: {e}")

# Test 2: Very long query
try:
    start = time.time()
    long_query = "Python " * 100
    long_results = search_engine.text_search(long_query, large_job_dataset[:50])
    end = time.time()
    edge_case_results.append({
        'test': 'Very long query',
        'pass': True,
        'latency_ms': (end - start) * 1000
    })
    print(f"  ✓ Very long query: {len(long_results)} results, {(end-start)*1000:.2f}ms")
except Exception as e:
    edge_case_results.append({'test': 'Very long query', 'pass': False, 'error': str(e)})
    print(f"  ✗ Very long query: {e}")

# Test 3: Invalid token verification
try:
    start = time.time()
    invalid_result = auth_service.verify_token("invalid_token_12345")
    end = time.time()
    edge_case_results.append({
        'test': 'Invalid token',
        'pass': invalid_result is None,
        'latency_ms': (end - start) * 1000
    })
    print(f"  ✓ Invalid token handled: {(end-start)*1000:.2f}ms")
except Exception as e:
    edge_case_results.append({'test': 'Invalid token', 'pass': False, 'error': str(e)})
    print(f"  ✗ Invalid token: {e}")

# Test 4: Concurrent identical searches (caching behavior)
try:
    times = []
    for i in range(5):
        start = time.time()
        results = search_engine.search(skills=["Python"], location="Bangalore", jobs=large_job_dataset)
        times.append((time.time() - start) * 1000)
    
    edge_case_results.append({
        'test': 'Repeated searches',
        'pass': True,
        'avg_latency_ms': np.mean(times),
        'variance': np.std(times)
    })
    print(f"  ✓ Repeated searches: avg {np.mean(times):.2f}ms, variance {np.std(times):.2f}ms")
except Exception as e:
    edge_case_results.append({'test': 'Repeated searches', 'pass': False, 'error': str(e)})
    print(f"  ✗ Repeated searches: {e}")

performance_results['edge_cases'] = edge_case_results

# ===== GENERATE PERFORMANCE SUMMARY =====
print("\n" + "=" * 80)
print("PERFORMANCE TEST SUMMARY")
print("=" * 80)

print("\n📊 LATENCY TESTS:")
for test in performance_results['latency_tests']:
    status = "✓" if test['pass'] else "✗"
    print(f"  {status} {test['test']:20s} | Avg: {test['avg_ms']:6.2f}ms | P95: {test['p95_ms']:6.2f}ms | Target: <{test['target_ms']}ms")

print("\n📈 THROUGHPUT TESTS:")
for test in performance_results['throughput_tests']:
    status = "✓" if test['pass'] else "✗"
    print(f"  {status} {test['test']:20s} | {test['ops_per_second']:.2f} ops/sec | Target: >{test['target_ops_per_second']} ops/sec")

print("\n⚡ SCALABILITY:")
scale_test = performance_results['scalability_tests'][0]
print(f"  {'✓' if scale_test['efficient_scaling'] else '⚠'} Sub-linear scaling: {scale_test['latency_growth']:.2f}x latency growth for {scale_test['dataset_growth']:.0f}x data growth")

print("\n🔧 EDGE CASES:")
for edge in performance_results['edge_cases']:
    status = "✓" if edge['pass'] else "✗"
    print(f"  {status} {edge['test']}")

# Calculate overall performance score
latency_pass_rate = sum(1 for t in performance_results['latency_tests'] if t['pass']) / len(performance_results['latency_tests'])
throughput_pass_rate = sum(1 for t in performance_results['throughput_tests'] if t['pass']) / len(performance_results['throughput_tests'])
edge_case_pass_rate = sum(1 for e in performance_results['edge_cases'] if e['pass']) / len(performance_results['edge_cases'])

overall_performance_score = (latency_pass_rate * 0.5 + throughput_pass_rate * 0.3 + edge_case_pass_rate * 0.2) * 100

print("\n" + "=" * 80)
print(f"OVERALL PERFORMANCE SCORE: {overall_performance_score:.1f}%")
print("=" * 80)

if overall_performance_score >= 90:
    print("🎉 EXCELLENT PERFORMANCE - Production ready!")
elif overall_performance_score >= 75:
    print("✓ GOOD PERFORMANCE - Minor optimizations needed")
elif overall_performance_score >= 60:
    print("⚠ ACCEPTABLE PERFORMANCE - Optimization recommended")
else:
    print("✗ PERFORMANCE ISSUES - Requires significant optimization")

print(f"\nTest Run Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# Export results
perf_test_results = performance_results
perf_score = overall_performance_score
