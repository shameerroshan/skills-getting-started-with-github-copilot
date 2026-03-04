"""Tests for POST /activities/{activity_name}/signup endpoint"""

import pytest


class TestSignupForActivity:
    """Test the signup endpoint"""

    def test_signup_new_student_succeeds(self, client, reset_activities):
        """Test that a new student can sign up for an activity"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert "newstudent@mergington.edu" in response.json()["message"]

    def test_signup_adds_student_to_participants(self, client, reset_activities):
        """Test that signup actually adds the student to participants"""
        # Sign up new student
        client.post(
            "/activities/Programming Class/signup",
            params={"email": "alice@mergington.edu"}
        )
        
        # Verify student is in participants
        response = client.get("/activities")
        activities_data = response.json()
        assert "alice@mergington.edu" in activities_data["Programming Class"]["participants"]

    def test_signup_multiple_students_same_activity(self, client, reset_activities):
        """Test that multiple different students can sign up for same activity"""
        client.post(
            "/activities/Art Studio/signup",
            params={"email": "student1@mergington.edu"}
        )
        client.post(
            "/activities/Art Studio/signup",
            params={"email": "student2@mergington.edu"}
        )
        
        response = client.get("/activities")
        participants = response.json()["Art Studio"]["participants"]
        
        assert "student1@mergington.edu" in participants
        assert "student2@mergington.edu" in participants

    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test that signing up for nonexistent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "test@mergington.edu"}
        )
        
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_student_returns_400(self, client, reset_activities):
        """Test that a student already signed up cannot sign up again"""
        # michael@mergington.edu is already in Chess Club
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_preserves_existing_participants(self, client, reset_activities):
        """Test that signup preserves existing participants in the activity"""
        # Get initial participants
        response = client.get("/activities")
        initial_participants = response.json()["Basketball Team"]["participants"].copy()
        
        # Sign up new student
        client.post(
            "/activities/Basketball Team/signup",
            params={"email": "newplayer@mergington.edu"}
        )
        
        # Verify initial participants are still there
        response = client.get("/activities")
        participants = response.json()["Basketball Team"]["participants"]
        
        for original_email in initial_participants:
            assert original_email in participants

    def test_signup_different_activities(self, client, reset_activities):
        """Test that a student can sign up for different activities"""
        student_email = "athlete@mergington.edu"
        
        client.post(
            "/activities/Tennis Club/signup",
            params={"email": student_email}
        )
        client.post(
            "/activities/Gym Class/signup",
            params={"email": student_email}
        )
        
        response = client.get("/activities")
        activities_data = response.json()
        
        assert student_email in activities_data["Tennis Club"]["participants"]
        assert student_email in activities_data["Gym Class"]["participants"]
