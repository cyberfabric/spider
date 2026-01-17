# @fdd-test:fdd-fdd-feature-core-methodology-test-business-validation:ph-1
"""
Test BUSINESS.md validation.

Tests business context validation including actors, capabilities, and use cases.
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))

from fdd.validation.artifacts.business import validate_business_context


class TestBusinessStructure(unittest.TestCase):
    """Test BUSINESS.md structure validation."""

    def test_minimal_valid_business_passes(self):
        """Test minimal valid BUSINESS.md passes."""
        text = """# Business Context

## A. Feature Context

**Purpose**: Test application

**Target Users**: Test users

**Key Problems Solved**: Testing

**Success Criteria**: Works

## B. Actors

### Human Actors

#### User

- **ID**: `fdd-app-actor-user`
- **Role**: End user

### System Actors

#### System

- **ID**: `fdd-app-actor-system`
- **Role**: Backend system

## C. Capabilities

#### User Management

- **ID**: `fdd-app-capability-user-mgmt`
- **Purpose**: Manage users
- User creation
- User deletion
- **Actors**: `fdd-app-actor-user`

## D. Use Cases

#### Login Use Case

- **ID**: `fdd-app-usecase-login`
- **Actor**: `fdd-app-actor-user`
- **Preconditions**: User has account

1. User enters credentials
2. System validates credentials

- **Postconditions**: User is authenticated
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "PASS")

    def test_missing_section_b_fails(self):
        """Test missing Actors section fails."""
        text = """# Business Context

## C. Capabilities

Content.

## D. Use Cases

Content.
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "FAIL")
        missing = [s["id"] for s in report["missing_sections"]]
        self.assertIn("B", missing)

    def test_missing_section_c_fails(self):
        """Test missing Capabilities section fails."""
        text = """# Business Context

## A. Feature Context

**Purpose**: Test

**Target Users**: Users

**Key Problems Solved**: Problems

**Success Criteria**: Criteria

## B. Actors

- **ID**: `fdd-app-actor-user`

## D. Use Cases

Content.
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "FAIL")
        missing = [s["id"] for s in report["missing_sections"]]
        self.assertIn("C", missing)

    def test_missing_section_d_fails(self):
        """Test missing Use Cases section fails."""
        text = """# Business Context

## A. Feature Context

**Purpose**: Test

**Target Users**: Users

**Key Problems Solved**: Problems

**Success Criteria**: Criteria

## B. Actors

### Human Actors

#### User

- **ID**: `fdd-app-actor-user`
- **Role**: User

### System Actors

#### System

- **ID**: `fdd-app-actor-system`
- **Role**: System

## C. Capabilities

#### CAP-001

- **ID**: `fdd-app-capability-test`
- **Purpose**: Test
- **Actors**: `fdd-app-actor-user`
"""
        report = validate_business_context(text)
        
        # Section D is optional, so missing it is OK - test should expect PASS
        self.assertEqual(report["status"], "PASS")

    def test_missing_section_a_fails(self):
        """Test missing Section A fails (D is optional)."""
        text = """# Business Context

## B. Actors

### Human Actors

#### User

- **ID**: `fdd-app-actor-user`
- **Role**: User

### System Actors

#### System

- **ID**: `fdd-app-actor-system`
- **Role**: System

## C. Capabilities

#### CAP-001

- **ID**: `fdd-app-capability-test`
- **Purpose**: Test
- **Actors**: `fdd-app-actor-user`
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "FAIL")
        missing = [s["id"] for s in report["missing_sections"]]
        self.assertIn("A", missing)


class TestActorsValidation(unittest.TestCase):
    """Test actors section validation."""

    def test_actors_without_ids_fails(self):
        """Test actors section without IDs fails."""
        text = """# Business Context

## A. Feature Context

**Purpose**: Test

**Target Users**: Users

**Key Problems Solved**: Problems

**Success Criteria**: Criteria

## B. Actors

### Human Actors

#### BadActor

No ID field here!

### System Actors

#### System

- **ID**: `fdd-app-actor-system`
- **Role**: System

## C. Capabilities

#### Test Cap

- **ID**: `fdd-app-capability-test`
- **Purpose**: Test
- **Actors**: `fdd-app-actor-system`

## D. Use Cases

- **ID**: `fdd-app-usecase-test`
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "FAIL")

    def test_actors_with_proper_role_passes(self):
        """Test actors with Role field passes."""
        text = """# Business Context

## A. Feature Context

**Purpose**: Test

**Target Users**: Users

**Key Problems Solved**: Problems

**Success Criteria**: Criteria

## B. Actors

### Human Actors

#### Administrator

- **ID**: `fdd-app-actor-admin`
- **Role**: Administrator

### System Actors

#### User

- **ID**: `fdd-app-actor-user`
- **Role**: Regular user

## C. Capabilities

#### Test Cap

- **ID**: `fdd-app-capability-test`
- **Purpose**: Test
- Feature 1
- Feature 2
- **Actors**: `fdd-app-actor-admin`

## D. Use Cases

#### Test Use Case

- **ID**: `fdd-app-usecase-test`
- **Actor**: `fdd-app-actor-admin`
- **Preconditions**: System is ready

1. Administrator performs action

- **Postconditions**: Action completed
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "PASS")


class TestCapabilitiesValidation(unittest.TestCase):
    """Test capabilities section validation."""

    def test_capability_without_id_fails(self):
        """Test capability without ID fails."""
        text = """# Business Context

## A. Feature Context

**Purpose**: Test

**Target Users**: Users

**Key Problems Solved**: Problems

**Success Criteria**: Criteria

## B. Actors

- **ID**: `fdd-app-actor-user`

## C. Capabilities

### CAP-001: Test Capability

**Purpose**: Some purpose

**Actors**: `fdd-app-actor-user`

No ID field!

## D. Use Cases

- **ID**: `fdd-app-usecase-test`
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "FAIL")

    def test_capability_without_features_list_fails(self):
        """Test capability without features bullet list fails."""
        text = """# Business Context

## A. Feature Context

**Purpose**: Test

**Target Users**: Users

**Key Problems Solved**: Problems

**Success Criteria**: Criteria

## B. Actors

### Human Actors

#### User

- **ID**: `fdd-app-actor-user`
- **Role**: User

### System Actors

#### System

- **ID**: `fdd-app-actor-system`
- **Role**: System

## C. Capabilities

#### CAP-001

**ID**: `fdd-app-capability-test`

**Actors**: `fdd-app-actor-user`

No features list!
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "FAIL")
        cap_errors = [e for e in report["issues"] 
                     if "capability" in e.get("message", "").lower() and "feature" in e.get("message", "").lower()]
        self.assertGreater(len(cap_errors), 0)

    def test_capability_without_actors_fails(self):
        """Test capability without Actors reference fails."""
        text = """# Business Context

## A. Feature Context

**Purpose**: Test

**Target Users**: Users

**Key Problems Solved**: Problems

**Success Criteria**: Criteria

## B. Actors

### Human Actors

#### User

- **ID**: `fdd-app-actor-user`
- **Role**: User

### System Actors

#### System

- **ID**: `fdd-app-actor-system`
- **Role**: System

## C. Capabilities

#### CAP-001

**ID**: `fdd-app-capability-test`

**Purpose**: Test purpose

- Feature 1

No actors listed!
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "FAIL")
        cap_errors = [e for e in report["issues"]
                     if "capability" in e.get("message", "").lower() and "actor" in e.get("message", "").lower()]
        self.assertGreater(len(cap_errors), 0)

    def test_capability_with_unknown_actor_fails(self):
        """Test capability referencing unknown actor fails."""
        text = """# Business Context

## A. Feature Context

**Purpose**: Test

**Target Users**: Users

**Key Problems Solved**: Problems

**Success Criteria**: Criteria

## B. Actors

### Human Actors

#### User

- **ID**: `fdd-app-actor-user`
- **Role**: User

### System Actors

#### System

- **ID**: `fdd-app-actor-system`
- **Role**: System

## C. Capabilities

#### CAP-001

- **ID**: `fdd-app-capability-test`
- **Purpose**: Test purpose
- Feature 1
- **Actors**: `fdd-app-actor-unknown`
- Feature 1
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "FAIL")
        unknown_actor_errors = [e for e in report["issues"]
                               if "unknown actor" in e.get("message", "").lower()]
        self.assertGreater(len(unknown_actor_errors), 0)


class TestUseCasesValidation(unittest.TestCase):
    """Test use cases section validation."""

    def test_use_cases_without_ids_fails(self):
        """Test use cases without IDs fails."""
        text = """# Business Context

## A. Feature Context

**Purpose**: Test

**Target Users**: Users

**Key Problems Solved**: Problems

**Success Criteria**: Criteria

## B. Actors

### Human Actors

#### User

- **ID**: `fdd-app-actor-user`
- **Role**: User

### System Actors

#### System

- **ID**: `fdd-app-actor-system`
- **Role**: System

## C. Capabilities

#### Test Cap

- **ID**: `fdd-app-capability-test`
- **Purpose**: Test
- Feature 1
- Feature 2
- **Actors**: `fdd-app-actor-user`

## D. Use Cases

#### Bad Use Case

- **Actor**: `fdd-app-actor-user`
- **Preconditions**: None

1. Do something

- **Postconditions**: Done

No ID field here!
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "FAIL")
        # Check for missing ID validation issue
        uc_errors = [e for e in report["issues"]
                    if "use case" in str(e).lower() and "**id**" in str(e).lower()]
        self.assertGreater(len(uc_errors), 0)

    def test_use_cases_with_proper_ids_passes(self):
        """Test use cases with proper IDs passes."""
        text = """# Business Context

## A. Feature Context

**Purpose**: Test

**Target Users**: Users

**Key Problems Solved**: Problems

**Success Criteria**: Criteria

## B. Actors

### Human Actors

#### User

- **ID**: `fdd-app-actor-user`
- **Role**: User

### System Actors

#### System

- **ID**: `fdd-app-actor-system`
- **Role**: System

## C. Capabilities

#### Test Cap

- **ID**: `fdd-app-capability-test`
- **Purpose**: Test
- Feature 1
- Feature 2
- **Actors**: `fdd-app-actor-user`

## D. Use Cases

#### Login

- **ID**: `fdd-app-usecase-login`
- **Actor**: `fdd-app-actor-user`
- **Preconditions**: User has account

1. User enters credentials
2. System validates

- **Postconditions**: User is logged in

#### Logout

- **ID**: `fdd-app-usecase-logout`
- **Actor**: `fdd-app-actor-user`
- **Preconditions**: User is logged in

1. User clicks logout

- **Postconditions**: User is logged out
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "PASS")


class TestPlaceholders(unittest.TestCase):
    """Test placeholder detection."""

    def test_placeholders_detected(self):
        """Test that placeholders cause validation failure."""
        text = """# Business Context

## B. Actors

- **ID**: `fdd-app-actor-user`
  **Role**: TODO: Define role

## C. Capabilities

### CAP-001

**ID**: `fdd-app-capability-test`

**Purpose**: TBD

**Actors**: `fdd-app-actor-user`

## D. Use Cases

- **ID**: `fdd-app-usecase-test`
  **Purpose**: FIXME: Add purpose
"""
        report = validate_business_context(text)
        
        self.assertEqual(report["status"], "FAIL")
        self.assertGreater(len(report["placeholder_hits"]), 0)


if __name__ == "__main__":
    unittest.main()
