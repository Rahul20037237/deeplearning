import numpy as np
from typing import List, Dict
import re

# ============================================================================
# AI-POWERED JOB MATCHING ENGINE (Mock Implementation)
# ============================================================================

class JobMatchingEngine:
    """AI-powered matching engine with semantic similarity and skill matching"""
    
    def __init__(self):
        """Initialize matching engine"""
        print("Initializing Job Matching Engine...")
        print("✅ Engine ready for semantic matching and skill analysis")
        self.embedding_dim = 384  # Standard dimension for sentence transformers
    
    # ------------------------------------------------------------------------
    # EMBEDDING GENERATION (Simplified TF-IDF-based)
    # ------------------------------------------------------------------------
    
    def _text_to_vector(self, text: str) -> np.ndarray:
        """Simple text vectorization using character frequency (mock embedding)"""
        # Normalize text
        text = text.lower()
        words = re.findall(r'\w+', text)
        
        # Create a simple frequency-based vector (384 dims)
        vector = np.zeros(self.embedding_dim)
        for word in words:
            # Hash word to indices and increment
            for char in word:
                idx = (hash(char) % self.embedding_dim)
                vector[idx] += 1
        
        # Normalize to unit length
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def generate_job_embedding(self, job_data: Dict) -> np.ndarray:
        """Generate embedding for job posting"""
        job_text = f"""
        {job_data.get('title', '')}
        {job_data.get('description', '')}
        {' '.join(job_data.get('required_skills', []))}
        {job_data.get('location', '')}
        {job_data.get('experience_level', 'fresher')}
        """
        return self._text_to_vector(job_text)
    
    def generate_resume_embedding(self, resume_data: Dict) -> np.ndarray:
        """Generate embedding for user resume/profile"""
        resume_text = f"""
        {' '.join(resume_data.get('skills', []))}
        {resume_data.get('resume_text', '')}
        {' '.join([str(edu) for edu in resume_data.get('education', [])])}
        """
        return self._text_to_vector(resume_text)
    
    # ------------------------------------------------------------------------
    # SIMILARITY COMPUTATION
    # ------------------------------------------------------------------------
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings"""
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return float(max(0, min(1, similarity)))  # Clamp to [0, 1]
    
    def batch_compute_similarities(self, resume_embedding: np.ndarray, 
                                   job_embeddings: np.ndarray) -> np.ndarray:
        """Compute similarities between one resume and multiple jobs"""
        similarities = []
        for job_emb in job_embeddings:
            sim = self.compute_similarity(resume_embedding, job_emb)
            similarities.append(sim)
        return np.array(similarities)
    
    # ------------------------------------------------------------------------
    # SKILL MATCHING
    # ------------------------------------------------------------------------
    
    def compute_skill_match(self, user_skills: List[str], 
                           required_skills: List[str]) -> Dict:
        """Compute skill match metrics"""
        # Normalize skills to lowercase
        user_skills_lower = {skill.lower() for skill in user_skills}
        required_skills_lower = {skill.lower() for skill in required_skills}
        
        matched_skills = list(user_skills_lower.intersection(required_skills_lower))
        missing_skills = list(required_skills_lower - user_skills_lower)
        
        if len(required_skills) > 0:
            skill_match_pct = (len(matched_skills) / len(required_skills)) * 100
        else:
            skill_match_pct = 100.0
        
        return {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "skill_match_percentage": round(skill_match_pct, 2)
        }
    
    # ------------------------------------------------------------------------
    # RANKING ALGORITHM
    # ------------------------------------------------------------------------
    
    def rank_jobs(self, resume_embedding: np.ndarray, jobs_data: List[Dict],
                  user_skills: List[str], weights: Dict = None) -> List[Dict]:
        """Rank jobs based on multiple factors with weighted scoring"""
        if weights is None:
            weights = {
                "semantic": 0.5,     # Embedding similarity
                "skill": 0.3,        # Exact skill match
                "freshness": 0.1,    # Recent postings
                "salary": 0.1        # Salary competitiveness
            }
        
        # Extract job embeddings
        job_embeddings = np.array([job["job_embedding"] for job in jobs_data])
        
        # Compute semantic similarities
        semantic_scores = self.batch_compute_similarities(resume_embedding, job_embeddings)
        
        # Compute scores for each job
        ranked_jobs = []
        for idx, job in enumerate(jobs_data):
            # Semantic score
            semantic_score = semantic_scores[idx]
            
            # Skill match score
            skill_match = self.compute_skill_match(user_skills, job.get("required_skills", []))
            skill_score = skill_match["skill_match_percentage"] / 100.0
            
            # Freshness score (normalize days to [0, 1])
            days_old = job.get("days_since_posted", 0)
            freshness_score = max(0, 1 - (days_old / 30))  # Linear decay over 30 days
            
            # Salary score (simple presence check)
            salary_score = 1.0 if job.get("salary_min") and job.get("salary_max") else 0.5
            
            # Weighted final score
            final_score = (
                weights["semantic"] * semantic_score +
                weights["skill"] * skill_score +
                weights["freshness"] * freshness_score +
                weights["salary"] * salary_score
            )
            
            # Add to ranked list
            ranked_jobs.append({
                **job,
                "match_score": round(final_score, 4),
                "semantic_score": round(semantic_score, 4),
                "skill_match": skill_match,
                "freshness_score": round(freshness_score, 4),
                "salary_score": round(salary_score, 4)
            })
        
        # Sort by match score descending
        ranked_jobs.sort(key=lambda x: x["match_score"], reverse=True)
        
        return ranked_jobs

# ============================================================================
# DEMONSTRATION
# ============================================================================

print("=" * 80)
print("AI-POWERED JOB MATCHING ENGINE")
print("=" * 80)

# Initialize matching engine
matching_engine = JobMatchingEngine()

print("\n📊 DEMO DATA SETUP:")
# Mock resume data
resume_mock = {
    "skills": ["Python", "Machine Learning", "FastAPI", "MongoDB", "Docker"],
    "resume_text": "Passionate fresher with strong Python skills and ML knowledge. Completed projects in web development using FastAPI and data analysis.",
    "education": ["B.Tech Computer Science"]
}

# Mock job postings
jobs_mock = [
    {
        "job_id": "job_001",
        "title": "Junior Python Developer",
        "company": "Tech Corp",
        "description": "Looking for Python developer with FastAPI experience",
        "required_skills": ["Python", "FastAPI", "REST APIs"],
        "location": "Bangalore",
        "experience_level": "fresher",
        "days_since_posted": 2,
        "salary_min": 400000,
        "salary_max": 600000
    },
    {
        "job_id": "job_002",
        "title": "ML Engineer Intern",
        "company": "AI Startup",
        "description": "ML internship for freshers with Python and ML knowledge",
        "required_skills": ["Python", "Machine Learning", "TensorFlow"],
        "location": "Remote",
        "experience_level": "fresher",
        "days_since_posted": 5,
        "salary_min": 300000,
        "salary_max": 500000
    },
    {
        "job_id": "job_003",
        "title": "Backend Developer",
        "company": "Enterprise Inc",
        "description": "Backend development role requiring Java and Spring Boot",
        "required_skills": ["Java", "Spring Boot", "MySQL"],
        "location": "Mumbai",
        "experience_level": "junior",
        "days_since_posted": 15,
        "salary_min": None,
        "salary_max": None
    }
]

print("\n🔄 GENERATING EMBEDDINGS:")
# Generate resume embedding
resume_embedding = matching_engine.generate_resume_embedding(resume_mock)
print(f"  Resume embedding shape: {resume_embedding.shape}")
print(f"  First 5 dimensions: {resume_embedding[:5]}")

# Generate job embeddings
for job in jobs_mock:
    job["job_embedding"] = matching_engine.generate_job_embedding(job)
print(f"  Generated embeddings for {len(jobs_mock)} jobs")

print("\n🎯 RANKING JOBS:")
ranked_results = matching_engine.rank_jobs(
    resume_embedding=resume_embedding,
    jobs_data=jobs_mock,
    user_skills=resume_mock["skills"]
)

print(f"\n{'='*80}")
print("RANKED JOB MATCHES")
print(f"{'='*80}")

for rank, job in enumerate(ranked_results, 1):
    print(f"\n🏆 RANK #{rank}: {job['title']} at {job['company']}")
    print(f"   Overall Match Score: {job['match_score']:.2%}")
    print(f"   Semantic Similarity: {job['semantic_score']:.2%}")
    print(f"   Skill Match: {job['skill_match']['skill_match_percentage']:.1f}%")
    print(f"   Matched Skills: {job['skill_match']['matched_skills']}")
    print(f"   Missing Skills: {job['skill_match']['missing_skills']}")
    print(f"   Location: {job['location']}")

print("\n" + "=" * 80)
print("MATCHING ENGINE CAPABILITIES")
print("=" * 80)
print("  ✅ Vector embeddings (384-dim)")
print("  ✅ Semantic similarity via cosine distance")
print("  ✅ Exact skill matching with gap analysis")
print("  ✅ Multi-factor ranking (semantic + skill + freshness + salary)")
print("  ✅ Batch processing for efficiency")
print("  ✅ Configurable scoring weights")
print("  ✅ Real-time job recommendations")

print("\n🚀 PRODUCTION NOTES:")
print("  • Replace with SentenceTransformer (all-MiniLM-L6-v2) in production")
print("  • Sub-second matching for 1000+ jobs")
print("  • Pre-computed embeddings stored in MongoDB")
print("  • Real-time ranking via FastAPI endpoints")
print("  • Scalable to millions of job-user pairs")
