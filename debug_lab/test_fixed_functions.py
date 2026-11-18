from buggy_functions import format_alert_summary, get_alert_owner, average_response_time
 
 
def test_format_alert_summary_with_int_count():
	assert format_alert_summary(3, "critical") == "There are 3 critical alerts active."
 
 
def test_get_alert_owner_known_team():
	team_directory = {"db-team": "Asha Patel", "api-team": "Jordan Lee"}
	alert = {"id": 6, "owner": "db-team"}
	assert get_alert_owner(alert, team_directory) == "Asha Patel"
 
 
def test_get_alert_owner_unknown_team_returns_fallback():
	"""Confirms the original KeyError case no longer crashes."""
	team_directory = {"db-team": "Asha Patel", "api-team": "Jordan Lee"}
	alert = {"id": 5, "owner": "network-team"}
	assert get_alert_owner(alert, team_directory) == "Unassigned"
 
 
def test_average_response_time_normal_list():
	assert average_response_time([120, 80, 100]) == 100.0
 
 
def test_average_response_time_empty_list_returns_zero():
	"""Confirms the original ZeroDivisionError case no longer crashes."""
	assert average_response_time([]) == 0.0
