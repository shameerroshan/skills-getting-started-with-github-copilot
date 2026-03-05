"""Tests for POST /activities/{activity_name}/unregister endpoint"""

import pytest


class TestUnregisterFromActivity:
    """Test the unregister endpoint"""

    def test_unregister_existing_student_succeeds(self, client, reset_activities):
        """Test that an enrolled student can unregister from an activity"""
        # michael@mergington.edu is already in Chess Club
        response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert "michael@mergington.edu" in response.json()["message"]

    def test_unregister_removes_student_from_participants(self, client, reset_activities):
        """Test that unregister actually removes the student"""
        # Sign up new student first
        client.post(
            "/activities/Science Club/signup",
            params={"email": "testuser@mergington.edu"}
        )
        
        # Verify student is signed up
        response = client.get("/activities")
        assert "testuser@mergington.edu" in response.json()["Science Club"]["participants"]
        
        # Unregister
        client.post(
            "/activities/Science Club/unregister",
            params={"email": "testuser@mergington.edu"}
        )
        
        # Verify student is removed
        response = client.get("/activities")
        assert "testuser@mergington.edu" not in response.json()["Science Club"]["participants"]

    def test_unregister_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test that unregistering from nonexistent activity returns 404"""
        response = client.post(
            "/activities/Fake Activity/unregister",
            params={"email": "test@mergington.edu"}
        )
        
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_student_not_signed_up_returns_400(self, client, reset_activities):
        """Test that unregistering a student not in activity returns 400"""
        response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": "notstudent@mergington.edu"}
        )
        
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_preserves_other_participants(self, client, reset_activities):
        """Test that unregistering one student doesn't affect others"""
        # Get initial participants for Chess Club
        response = client.get("/activities")
        initial_participants = response.json()["Chess Club"]["participants"].copy()
        
        # Unregister one student
        client.post(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        
        # Verify other participant is still there
        response = client.get("/activities")
        participants = response.json()["Chess Club"]["participants"]
        
        assert "daniel@mergington.edu" in participants
        assert "michael@mergington.edu" not in participants

    def test_unregister_and_signup_again(self, client, reset_activities):
        """Test that a student can unregister and then sign up again"""
        student_email = "changeable@mergington.edu"
        
        # Sign up
        client.post(
            "/activities/Debate Club/signup",
            params={"email": student_email}
        )
        
        # Unregister
        client.post(
            "/activities/Debate Club/unregister",
            params={"email": student_email}
        )
        
        # Sign up again
        response = client.post(
            "/activities/Debate Club/signup",
            params={"email": student_email}
        )
        
        assert response.status_code == 200
        
        # Verify student is signed up
        response = client.get("/activities")
        assert student_email in response.json()["Debate Club"]["participants"]

    def test_unregister_all_students_from_activity(self, client, reset_activities):
        """Test that all students can be unregistered from an activity"""
        # Get all participants
        response = client.get("/activities")
        initial_participants = response.json()["Music Ensemble"]["participants"].copy()
        
        # Unregister all
        for email in initial_participants:
            client.post(
                "/activities/Music Ensemble/unregister",
                params={"email": email}
            )
        
        # Verify all are removed
        response = client.get("/activities")
        assert len(response.json()["Music Ensemble"]["participants"]) == 0

    def test_cannot_unregister_twice(self, client, reset_activities):
        """Test that unregistering twice fails on second attempt"""
        student_email = "doubleunreg@mergington.edu"
        
        # Sign up
        client.post(
            "/activities/Tennis Club/signup",
            params={"email": student_email}
        )
        
        # First unregister should succeed
        response1 = client.post(
            "/activities/Tennis Club/unregister",
            params={"email": student_email}
        )
        assert response1.status_code == 200
        
        # Second unregister should fail
        response2 = client.post(
            "/activities/Tennis Club/unregister",
            params={"email": student_email}
        )
        assert response2.status_code == 400
        assert "not signed up" in response2.json()["detail"]
