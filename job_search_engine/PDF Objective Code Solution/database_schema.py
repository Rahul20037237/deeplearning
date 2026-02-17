from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from enum import Enum

# ============================================================================
# DATABASE SCHEMA MODELS (MongoDB/Pydantic)
# ============================================================================

class ExperienceLevel(str, Enum):
    """Experience level classification"""
    FRESHER = "fresher"  # 0-1 years
    JUNIOR = "junior"    # 1-2 years
    MID = "mid"         # 2-5 years
    SENIOR = "senior"   # 5+ years

class JobType(str, Enum):
    """Job type classification"""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"
    CONTRACT = "contract"
    REMOTE = "remote"

class ApplicationStatus(str, Enum):
    """Application tracking statuses"""
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFERED = "offered"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

# ----------------------------------------------------------------------------
# USER SCHEMA
# ----------------------------------------------------------------------------

class UserProfile(BaseModel):
    """User profile and authentication"""
    user_id: str = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User email")
    password_hash: str = Field(..., description="Hashed password")
    full_name: str = Field(..., description="Full name")
    phone: Optional[str] = None
    
    # Profile details
    location: Optional[str] = None
    preferred_locations: List[str] = Field(default_factory=list)
    expected_salary_min: Optional[float] = None
    expected_salary_max: Optional[float] = None
    
    # Resume data
    resume_url: Optional[str] = None  # S3/storage URL
    resume_text: Optional[str] = None  # Extracted text
    extracted_skills: List[str] = Field(default_factory=list)
    education: List[Dict] = Field(default_factory=list)
    experience: List[Dict] = Field(default_factory=list)
    
    # ML embeddings
    profile_embedding: Optional[List[float]] = None  # 384-dim vector
    
    # Metadata
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "usr_123",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "extracted_skills": ["Python", "Machine Learning", "FastAPI"],
                "location": "Bangalore"
            }
        }

# ----------------------------------------------------------------------------
# JOB SCHEMA
# ----------------------------------------------------------------------------

class Job(BaseModel):
    """Job posting schema"""
    job_id: str = Field(..., description="Unique job identifier")
    
    # Basic info
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    company_logo_url: Optional[str] = None
    location: str = Field(..., description="Job location")
    is_remote: bool = False
    
    # Job details
    description: str = Field(..., description="Full job description")
    responsibilities: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    
    # Experience & education
    experience_min: float = Field(..., ge=0, le=2, description="Min years (0-2)")
    experience_max: float = Field(..., ge=0, le=2, description="Max years (0-2)")
    experience_level: ExperienceLevel = ExperienceLevel.FRESHER
    education_required: List[str] = Field(default_factory=list)
    
    # Compensation
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str = "INR"
    
    # Job type & metadata
    job_type: JobType = JobType.FULL_TIME
    job_url: str = Field(..., description="Original job posting URL")
    source: str = Field(..., description="Job portal source")
    
    # ML embeddings
    job_embedding: Optional[List[float]] = None  # 384-dim vector
    
    # Tracking
    posted_date: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    view_count: int = 0
    application_count: int = 0
    
    # Status
    is_active: bool = True
    is_verified: bool = False
    is_featured: bool = False
    
    # Search optimization
    search_keywords: List[str] = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "job_456",
                "title": "Junior Python Developer",
                "company": "Tech Corp",
                "location": "Bangalore",
                "required_skills": ["Python", "FastAPI", "MongoDB"],
                "experience_min": 0,
                "experience_max": 1,
                "salary_min": 300000,
                "salary_max": 500000
            }
        }

# ----------------------------------------------------------------------------
# APPLICATION SCHEMA
# ----------------------------------------------------------------------------

class Application(BaseModel):
    """Job application tracking"""
    application_id: str = Field(..., description="Unique application ID")
    user_id: str = Field(..., description="Applicant user ID")
    job_id: str = Field(..., description="Job ID")
    
    # Match data
    match_score: float = Field(..., ge=0, le=1, description="AI match score")
    skill_match_percentage: float = Field(..., ge=0, le=100)
    missing_skills: List[str] = Field(default_factory=list)
    
    # Application details
    status: ApplicationStatus = ApplicationStatus.APPLIED
    cover_letter: Optional[str] = None
    resume_version: Optional[str] = None  # Version used for application
    
    # Timeline tracking
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    status_updated_at: datetime = Field(default_factory=datetime.utcnow)
    interview_dates: List[datetime] = Field(default_factory=list)
    
    # Notes
    notes: List[Dict] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "application_id": "app_789",
                "user_id": "usr_123",
                "job_id": "job_456",
                "match_score": 0.87,
                "status": "interview"
            }
        }

# ----------------------------------------------------------------------------
# SKILL GAP ANALYSIS SCHEMA
# ----------------------------------------------------------------------------

class SkillGapAnalysis(BaseModel):
    """Skill gap detection and recommendations"""
    analysis_id: str = Field(..., description="Analysis ID")
    user_id: str = Field(..., description="User ID")
    job_id: str = Field(..., description="Target job ID")
    
    # Gap analysis
    user_skills: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    
    # Recommendations
    learning_recommendations: List[Dict] = Field(default_factory=list)
    estimated_learning_time: Optional[int] = None  # in hours
    priority_skills: List[str] = Field(default_factory=list)
    
    # Resources
    course_suggestions: List[Dict] = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ----------------------------------------------------------------------------
# ADMIN & MODERATION SCHEMA
# ----------------------------------------------------------------------------

class AdminUser(BaseModel):
    """Admin user for moderation"""
    admin_id: str = Field(..., description="Admin ID")
    email: str
    password_hash: str
    full_name: str
    role: str = "moderator"  # moderator, admin, super_admin
    permissions: List[str] = Field(default_factory=list)
    
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

class ModerationAction(BaseModel):
    """Track moderation actions"""
    action_id: str
    admin_id: str
    target_type: str  # "job", "user", "company"
    target_id: str
    action_type: str  # "approve", "reject", "flag", "ban"
    reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ----------------------------------------------------------------------------
# ANALYTICS SCHEMA
# ----------------------------------------------------------------------------

class SearchAnalytics(BaseModel):
    """Track search queries for analytics"""
    search_id: str
    user_id: Optional[str] = None
    query_text: Optional[str] = None
    filters: Dict = Field(default_factory=dict)
    results_count: int = 0
    clicked_jobs: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# MONGODB COLLECTIONS STRUCTURE
# ============================================================================

schema_collections = {
    "users": {
        "model": "UserProfile",
        "indexes": [
            {"fields": ["email"], "unique": True},
            {"fields": ["user_id"], "unique": True},
            {"fields": ["extracted_skills"]},
            {"fields": ["created_at"]},
        ]
    },
    "jobs": {
        "model": "Job",
        "indexes": [
            {"fields": ["job_id"], "unique": True},
            {"fields": ["required_skills"]},
            {"fields": ["location"]},
            {"fields": ["experience_min", "experience_max"]},
            {"fields": ["posted_date"]},
            {"fields": ["is_active"]},
            {"fields": ["search_keywords"], "type": "text"},
        ]
    },
    "applications": {
        "model": "Application",
        "indexes": [
            {"fields": ["application_id"], "unique": True},
            {"fields": ["user_id"]},
            {"fields": ["job_id"]},
            {"fields": ["status"]},
            {"fields": ["applied_at"]},
        ]
    },
    "skill_gaps": {
        "model": "SkillGapAnalysis",
        "indexes": [
            {"fields": ["analysis_id"], "unique": True},
            {"fields": ["user_id"]},
            {"fields": ["job_id"]},
        ]
    },
    "admins": {
        "model": "AdminUser",
        "indexes": [
            {"fields": ["admin_id"], "unique": True},
            {"fields": ["email"], "unique": True},
        ]
    },
    "moderation_actions": {
        "model": "ModerationAction",
        "indexes": [
            {"fields": ["action_id"], "unique": True},
            {"fields": ["target_type", "target_id"]},
            {"fields": ["admin_id"]},
        ]
    },
    "search_analytics": {
        "model": "SearchAnalytics",
        "indexes": [
            {"fields": ["search_id"], "unique": True},
            {"fields": ["user_id"]},
            {"fields": ["timestamp"]},
        ]
    }
}

# ============================================================================
# SCHEMA SUMMARY
# ============================================================================

print("=" * 80)
print("DATABASE SCHEMA DESIGN - COMPLETE")
print("=" * 80)

print("\n📊 COLLECTIONS OVERVIEW:")
for collection_name, config in schema_collections.items():
    print(f"\n  • {collection_name.upper()}")
    print(f"    Model: {config['model']}")
    print(f"    Indexes: {len(config['indexes'])} defined")

print("\n\n🔑 KEY FEATURES:")
print("  ✅ Pydantic models for validation and type safety")
print("  ✅ MongoDB-optimized schema with proper indexing")
print("  ✅ Support for ML embeddings (384-dim vectors)")
print("  ✅ Complete application tracking workflow")
print("  ✅ Skill gap analysis integration")
print("  ✅ Admin moderation system")
print("  ✅ Search analytics for insights")
print("  ✅ RBAC-ready permission structure")

print("\n\n📐 DATA RELATIONSHIPS:")
print("  • Users → Applications (1:many)")
print("  • Jobs → Applications (1:many)")
print("  • Users → SkillGaps (1:many)")
print("  • Jobs → SkillGaps (1:many)")
print("  • Admins → ModerationActions (1:many)")

print("\n\n🎯 OPTIMIZATION FEATURES:")
print("  • Compound indexes for fast querying")
print("  • Text search on job keywords")
print("  • Skill-based indexing for matching")
print("  • Location and experience filters")
print("  • Temporal indexes for analytics")

print("\n✅ Schema ready for FastAPI integration and MongoDB deployment")
