"""Tests for GET /activities endpoint"""

import pytest


class TestGetActivities:
    """Test the GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities"""
        # Arrange: nothing special beyond fixture setup
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities_data = response.json()
        
        # Verify all expected activities are returned
        assert "Chess Club" in activities_data
        assert "Programming Class" in activities_data
        assert "Gym Class" in activities_data
        assert "Basketball Team" in activities_data
        assert "Tennis Club" in activities_data
        assert "Art Studio" in activities_data
        assert "Music Ensemble" in activities_data
        assert "Debate Club" in activities_data
        assert "Science Club" in activities_data

    def test_activity_contains_required_fields(self, client, reset_activities):
        """Test that each activity contains required fields"""
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        # Check Chess Club as representative activity
        chess_club = activities_data["Chess Club"]
        
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club

    def test_activity_participants_is_list(self, client, reset_activities):
        """Test that participants field is a list"""
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity in activities_data.items():
            assert isinstance(activity["participants"], list), \
                f"{activity_name} participants should be a list"

    def test_activity_max_participants_is_integer(self, client, reset_activities):
        """Test that max_participants is an integer"""
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        for activity_name, activity in activities_data.items():
            assert isinstance(activity["max_participants"], int), \
                f"{activity_name} max_participants should be an integer"

    def test_get_activities_has_correct_initial_participants(self, client, reset_activities):
        """Test that activities have expected initial participants"""
        # Act
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert
        # Chess Club should have 2 initial participants
        assert len(activities_data["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in activities_data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in activities_data["Chess Club"]["participants"]
