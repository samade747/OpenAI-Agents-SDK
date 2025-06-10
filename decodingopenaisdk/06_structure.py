"""
Comprehensive Guide: Structured Outputs in OpenAI Agents SDK

This file demonstrates 8 different approaches to structured outputs, from basic to advanced,
showing when to use each approach and the trade-offs involved.

Key Concepts:
1. Strict vs Non-Strict Schemas
2. Simple vs Complex Data Structures  
3. Optional vs Required Fields
4. Nested Models vs Flat Structures
5. Performance vs Flexibility Trade-offs
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional, Union, Literal, Any
from enum import Enum
from datetime import datetime
from agents import Agent, Runner, AgentOutputSchema
import asyncio

# =============================================================================
# USE CASE 1: Basic Strict Schema (Recommended for Production)
# =============================================================================


class BasicUserInfo(BaseModel):
    """
    ✅ STRICT MODE COMPATIBLE
    - Only basic types (str, int, bool)
    - No Optional/Union types
    - All fields have defaults
    - Perfect for simple, reliable outputs
    """
    name: str = ""
    age: int = 0
    is_student: bool = False
    email: str = ""

    model_config = ConfigDict(extra="forbid")

#     ✅ Why use it?
# Perfect for API responses or production environments

# Guarantees schema consistency




# =============================================================================
# USE CASE 2: Enum-Based Strict Schema (Great for Classification)
# =============================================================================

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskClassification(BaseModel):
    """
    ✅ STRICT MODE COMPATIBLE
    - Uses Enums for controlled values
    - Prevents invalid classifications
    - Type-safe and self-documenting
    """
    task_type: Literal["bug", "feature", "documentation", "maintenance"] = "feature"
    priority: Priority = Priority.MEDIUM
    estimated_hours: int = 1
    requires_review: bool = True

# ✅ Why use it?
# Prevents incorrect values for fields like priority

# Very useful for categorization/classification tasks




# =============================================================================
# USE CASE 3: Nested Strict Schema (Complex but Strict-Compatible)
# =============================================================================


class Address(BaseModel):
    street: str = ""
    city: str = ""
    country: str = ""
    postal_code: str = ""

    model_config = ConfigDict(extra="forbid")


class ContactInfo(BaseModel):
    email: str = ""
    phone: str = ""

    model_config = ConfigDict(extra="forbid")


class ComplexUserProfile(BaseModel):
    """
    ✅ STRICT MODE COMPATIBLE
    - Nested Pydantic models instead of dicts
    - No Optional/Union types
    - Uses Field(default_factory) for complex defaults
    - Maintains structure while being strict
    """
    personal_info: BasicUserInfo = Field(default_factory=BasicUserInfo)
    address: Address = Field(default_factory=Address)
    contact: ContactInfo = Field(default_factory=ContactInfo)
    registration_date: str = ""  # ISO format string instead of datetime

    model_config = ConfigDict(extra="forbid")
# =============================================================================

# ✅ Why use it?
# Keeps your data modular and structured

# Enables nested validation for real-world profiles


✅ USE CASE 4: List-Based Strict Schema
python
Copy
Edit
class CourseGrade(BaseModel):
    course_name: str = ""
    grade: str = ""
    credits: int = 0

    model_config = ConfigDict(extra="forbid")
python
Copy
Edit
class StudentTranscript(BaseModel):
    """
    ✅ STRICT MODE COMPATIBLE
    - Lists of Pydantic models work in strict mode
    - Avoids complex dict structures
    - Maintains type safety for collections
    """
    student_id: str = ""
    student_name: str = ""
    gpa: float = 0.0
    courses: List[CourseGrade] = Field(default_factory=list)  # ⬅️ List of nested models
    graduation_status: Literal["enrolled", "graduated", "dropped"] = "enrolled"

    model_config = ConfigDict(extra="forbid")
✅ Why use it?
Excellent for returning batch/tabular-like data (e.g., transcripts, reports)

❌ USE CASE 5: Flexible Non-Strict Schema
python
Copy
Edit
class FlexibleAnalysis(BaseModel):
    """
    ❌ NON-STRICT MODE ONLY
    - Uses Optional/Union types freely
    - More flexible but slower validation
    - Good for prototyping and dynamic data
    """
    analysis_type: str                            # Required field
    confidence_score: Optional[float] = None      # Optional field
    results: Union[dict[str, Any], list[Any], str, None] = None  # Flexible result
    metadata: Optional[dict[str, Any]] = None
    errors: Optional[List[str]] = None
    timestamp: Optional[datetime] = None

    model_config = ConfigDict(extra="allow")  # ✅ Allow unknown fields
⚠️ Trade-offs:
Great for exploration, dynamic data, and debugging

Avoid in production unless you sanitize inputs properly

✅ USE CASE 6: Validated Strict Schema
python
Copy
Edit
class ValidatedOrder(BaseModel):
    """
    ✅ STRICT MODE COMPATIBLE WITH VALIDATION
    - Includes custom validation logic
    - Maintains strict compatibility
    - Enforces business rules
    """
    order_id: str = ""
    customer_email: str = ""
    total_amount: float = 0.0
    currency: Literal["USD", "EUR", "GBP"] = "USD"
    status: Literal["pending", "confirmed", "shipped", "delivered"] = "pending"

    model_config = ConfigDict(extra="forbid")

    # Email validation logic using field_validator
    @field_validator('customer_email')
    @classmethod
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v

    # Business rule: amount must be positive
    @field_validator('total_amount')
    @classmethod
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError('Amount cannot be negative')
        return v
✅ Why use it?
Combine schema validation with custom rules

Crucial for financial systems, ecommerce, logistics

Would you like me to continue with:

✅ Use Case 7: Mixed Types and Union Strategies

✅ Use Case 8: AgentOutputSchema Integration + Live Agent Demo

I can also generate .py files and a PDF summary for all use cases.











Tools



ChatGPT can make mistakes. Check important info.