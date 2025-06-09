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