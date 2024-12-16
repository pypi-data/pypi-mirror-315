# sportmonks-py
Python Package for SportsMonks API

Full details on the SportMonks API can be found [here](https://docs.sportmonks.com/football/) 

### Football

V3 of the SportMonks API is split into defined `Entities`, as listed below

- Fixture
- League, Season, Schedule, Stage and Round
- Team, Player, Squad, Coach and Referee
- Statistic
- Expected
- Standing and Topscorer
- Odd and Prediction
- Other

SportMonks imposes rate limits per entity (3000 per hour), hence this package separates endpoints by entity. More information
on entity rate limits can be viewed in the SportMonks documentation [here](https://docs.sportmonks.com/football/api/rate-limit).

For brevity and ease of use, entities have been mapped to a shortened keyword as below

| Entity Name | API Endpoint |
| ------------|--------------|
| Fixture     | fixture      |
 |League, Season, Schedule, Stage and Round | leagues      |
 | Team, Player, Squad, Coach and Referee | teams        |
| Statistic | statistics   |
| Expected | expected     |
| Standing and Topscorer | standings    |
| Odd and Prediction | odds         |
| Other | misc         |

### Documentation
Full documentation can be found at [ReadTheDocs](https://sportmonks-py.readthedocs.io/en/latest/)

#### Examples

Filtering

The SportMonks API allows for filtering of data using query parameters. Below is an example of how to filter data using the SportMonks API.

```python
from sportmonks_py import APIClient

client = APIClient(sport="football", api_token=f"{SPORTMONKS_API_TOKEN}")

fixture_id = [18528480]
response = client.fixtures.get_fixtures(
        fixture_ids=fixture_id, includes=["venue", "sport", "events.player"]
    )

for page in response:
    print(page)
```

Output
```doctest
{'id': 18528480, 'sport_id': 1, 'league_id': 271, 'season_id': 19686, 'stage_id': 77457696, 'group_id': None, 'aggregate_id': None, 'round_id': 273989, 'state_id': 5, 'venue_id': 1708, 'name': 'AGF vs Viborg', 'starting_at': '2022-07-24 12:00:00', 'result_info': 'AGF won after full-time.', 'leg': '1/1', 'details': None, 'length': 90, 'placeholder': False, 'has_odds': True, 'has_premium_odds': False, 'starting_at_timestamp': 1658664000}
```

Nested includes are also supported. This allows retrieving more information about players who scored a goal, and can be done as below. Full information on includes, filters and selects can be found on the SportMonks [documentation](https://docs.sportmonks.com/football/api/request-options).

```python
from sportmonks_py import APIClient

client = APIClient(sport="football", api_token=f"{SPORTMONKS_API_TOKEN}")

fixture_id = [18528480]
response = client.fixtures.get_fixtures(
        fixture_ids=fixture_id, includes=["venue", "sport", "events.player"]
    )

for page in response:
    print(page)
```

Output
```doctest
{'id': 18528480, 'sport_id': 1, 'league_id': 271, 'season_id': 19686, 'stage_id': 77457696, 'group_id': None, 'aggregate_id': None, 'round_id': 273989, 'state_id': 5, 'venue_id': 1708, 'name': 'AGF vs Viborg', 'starting_at': '2022-07-24 12:00:00', 'result_info': 'AGF won after full-time.', 'leg': '1/1', 'details': None, 'length': 90, 'placeholder': False, 'has_odds': True, 'has_premium_odds': False, 'starting_at_timestamp': 1658664000, 'events': [{'id': 36207309, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2447, 'type_id': 18, 'section': 'event', 'player_id': 37259998, 'related_player_id': 84031, 'player_name': 'S. Berger', 'related_player_name': 'Jeppe Grönning', 'result': None, 'info': None, 'addition': None, 'minute': 74, 'extra_minute': None, 'injured': False, 'on_bench': False, 'coach_id': None, 'sub_type_id': None, 'sort_order': 6, 'player': {'id': 37259998, 'sport_id': 1, 'country_id': 320, 'nationality_id': 320, 'city_id': 94694, 'position_id': 27, 'detailed_position_id': 156, 'type_id': 26, 'common_name': 'S. Brix', 'firstname': 'Sofus Berger', 'lastname': 'Brix', 'name': 'Sofus Berger Brix', 'display_name': 'Sofus Berger', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/30/37259998.png', 'height': 175, 'weight': None, 'date_of_birth': '2003-06-02', 'gender': 'male'}}, {'id': 36207389, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2905, 'type_id': 18, 'section': 'event', 'player_id': 37509380, 'related_player_id': 151709, 'player_name': 'A. Grønbæk', 'related_player_name': 'Sigurd Haugen', 'result': None, 'info': None, 'addition': None, 'minute': 82, 'extra_minute': None, 'injured': False, 'on_bench': False, 'coach_id': None, 'sub_type_id': None, 'sort_order': 7, 'player': {'id': 37509380, 'sport_id': 1, 'country_id': 320, 'nationality_id': 320, 'city_id': None, 'position_id': 26, 'detailed_position_id': None, 'type_id': 26, 'common_name': 'A. Erlykke', 'firstname': 'Albert Grønbæk', 'lastname': 'Erlykke', 'name': 'Albert Grønbæk Erlykke', 'display_name': 'A. Grønbæk', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/4/37509380.png', 'height': 176, 'weight': None, 'date_of_birth': '2001-05-23', 'gender': 'male'}}, {'id': 36207402, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2447, 'type_id': 18, 'section': 'event', 'player_id': 6600016, 'related_player_id': 25679, 'player_name': 'Nils Mortimer', 'related_player_name': 'Jay-Roy Grot', 'result': None, 'info': None, 'addition': None, 'minute': 83, 'extra_minute': None, 'injured': False, 'on_bench': False, 'coach_id': None, 'sub_type_id': None, 'sort_order': 8, 'player': {'id': 6600016, 'sport_id': 1, 'country_id': 32, 'nationality_id': 32, 'city_id': None, 'position_id': 27, 'detailed_position_id': 156, 'type_id': 27, 'common_name': 'N. Mortimer Moreno', 'firstname': 'Nils', 'lastname': 'Mortimer Moreno', 'name': 'Nils Mortimer Moreno', 'display_name': 'Nils Mortimer', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/16/6600016.png', 'height': 178, 'weight': None, 'date_of_birth': '2001-06-11', 'gender': 'male'}}, {'id': 69156851, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2905, 'type_id': 19, 'section': 'event', 'player_id': None, 'related_player_id': None, 'player_name': 'Uwe Rösler', 'related_player_name': None, 'result': None, 'info': 'Argument', 'addition': None, 'minute': 70, 'extra_minute': None, 'injured': None, 'on_bench': True, 'coach_id': 524374, 'sub_type_id': None, 'sort_order': 1, 'player': None}, {'id': 36207258, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2447, 'type_id': 14, 'section': 'event', 'player_id': 13980925, 'related_player_id': 83717, 'player_name': 'T. Bech', 'related_player_name': 'Christian Sörensen', 'result': '2-1', 'info': 'Header', 'addition': '3rd Goal', 'minute': 74, 'extra_minute': None, 'injured': None, 'on_bench': False, 'coach_id': None, 'sub_type_id': 1694, 'sort_order': 3, 'player': {'id': 13980925, 'sport_id': 1, 'country_id': 320, 'nationality_id': 320, 'city_id': None, 'position_id': 27, 'detailed_position_id': 151, 'type_id': 26, 'common_name': 'T. Kristensen', 'firstname': 'Tobias Bech', 'lastname': 'Kristensen', 'name': 'Tobias Bech Kristensen', 'display_name': 'Tobias Bech', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/29/13980925.png', 'height': 189, 'weight': None, 'date_of_birth': '2002-02-19', 'gender': 'male'}}, {'id': 36207297, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2905, 'type_id': 14, 'section': 'event', 'player_id': 83665, 'related_player_id': 84602, 'player_name': 'Patrick Mortensen', 'related_player_name': 'Mads Emil Madsen', 'result': '3-1', 'info': 'Header', 'addition': '4th Goal', 'minute': 76, 'extra_minute': None, 'injured': None, 'on_bench': False, 'coach_id': None, 'sub_type_id': 1694, 'sort_order': 4, 'player': {'id': 83665, 'sport_id': 1, 'country_id': 320, 'nationality_id': 320, 'city_id': None, 'position_id': 27, 'detailed_position_id': 151, 'type_id': 27, 'common_name': 'P. Mortensen', 'firstname': 'Patrick', 'lastname': 'Mortensen', 'name': 'Patrick Mortensen', 'display_name': 'Patrick Mortensen', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/17/83665.png', 'height': 188, 'weight': 81, 'date_of_birth': '1989-07-13', 'gender': 'male'}}, {'id': 36207411, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2905, 'type_id': 19, 'section': 'event', 'player_id': 83665, 'related_player_id': None, 'player_name': 'Patrick Mortensen', 'related_player_name': None, 'result': None, 'info': 'Foul', 'addition': '1st Yellow Card', 'minute': 87, 'extra_minute': None, 'injured': None, 'on_bench': False, 'coach_id': None, 'sub_type_id': None, 'sort_order': 1, 'player': {'id': 83665, 'sport_id': 1, 'country_id': 320, 'nationality_id': 320, 'city_id': None, 'position_id': 27, 'detailed_position_id': 151, 'type_id': 27, 'common_name': 'P. Mortensen', 'firstname': 'Patrick', 'lastname': 'Mortensen', 'name': 'Patrick Mortensen', 'display_name': 'Patrick Mortensen', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/17/83665.png', 'height': 188, 'weight': 81, 'date_of_birth': '1989-07-13', 'gender': 'male'}}, {'id': 36207224, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2905, 'type_id': 18, 'section': 'event', 'player_id': 85680, 'related_player_id': 84570, 'player_name': 'Frederik Brandhof', 'related_player_name': 'Mikael Anderson', 'result': None, 'info': None, 'addition': None, 'minute': 69, 'extra_minute': None, 'injured': False, 'on_bench': False, 'coach_id': None, 'sub_type_id': None, 'sort_order': 4, 'player': {'id': 85680, 'sport_id': 1, 'country_id': 320, 'nationality_id': 320, 'city_id': 84027, 'position_id': 26, 'detailed_position_id': 153, 'type_id': 26, 'common_name': 'F. Brandhof', 'firstname': 'Frederik', 'lastname': 'Brandhof', 'name': 'Frederik Brandhof', 'display_name': 'Frederik Brandhof', 'image_path': 'https://cdn.sportmonks.com/images/soccer/placeholder.png', 'height': 182, 'weight': None, 'date_of_birth': '1996-07-05', 'gender': 'male'}}, {'id': 36207234, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2905, 'type_id': 18, 'section': 'event', 'player_id': 289659, 'related_player_id': 37324853, 'player_name': 'Gift Links', 'related_player_name': 'E. Kahl', 'result': None, 'info': None, 'addition': None, 'minute': 69, 'extra_minute': None, 'injured': False, 'on_bench': False, 'coach_id': None, 'sub_type_id': None, 'sort_order': 5, 'player': {'id': 289659, 'sport_id': 1, 'country_id': 146, 'nationality_id': 146, 'city_id': 76315, 'position_id': 26, 'detailed_position_id': 157, 'type_id': 26, 'common_name': 'G. Links', 'firstname': 'Gift', 'lastname': 'Links', 'name': 'Gift Links', 'display_name': 'Gift Links', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/27/289659.png', 'height': 170, 'weight': None, 'date_of_birth': '1998-10-02', 'gender': 'male'}}, {'id': 36207019, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2905, 'type_id': 14, 'section': 'event', 'player_id': 84602, 'related_player_id': 151709, 'player_name': 'Mads Emil Madsen', 'related_player_name': 'Sigurd Haugen', 'result': '2-0', 'info': 'Shot', 'addition': '2nd Goal', 'minute': 60, 'extra_minute': None, 'injured': None, 'on_bench': False, 'coach_id': None, 'sub_type_id': None, 'sort_order': 2, 'player': {'id': 84602, 'sport_id': 1, 'country_id': 320, 'nationality_id': 320, 'city_id': 83948, 'position_id': 26, 'detailed_position_id': 153, 'type_id': 26, 'common_name': 'M. Madsen', 'firstname': 'Mads Emil', 'lastname': 'Madsen', 'name': 'Mads Emil Madsen', 'display_name': 'Mads Emil Madsen', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/26/84602.png', 'height': 189, 'weight': 82, 'date_of_birth': '1998-01-14', 'gender': 'male'}}, {'id': 36207006, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2447, 'type_id': 18, 'section': 'event', 'player_id': 37455152, 'related_player_id': 25582, 'player_name': 'Mads Söndergaard', 'related_player_name': 'Clint Leemans', 'result': None, 'info': None, 'addition': None, 'minute': 58, 'extra_minute': None, 'injured': False, 'on_bench': False, 'coach_id': None, 'sub_type_id': None, 'sort_order': 3, 'player': {'id': 37455152, 'sport_id': 1, 'country_id': 320, 'nationality_id': 320, 'city_id': 94694, 'position_id': 26, 'detailed_position_id': 153, 'type_id': None, 'common_name': 'M. Clausen', 'firstname': 'Mads Søndergaard', 'lastname': 'Clausen', 'name': 'Mads Søndergaard Clausen', 'display_name': 'Mads Søndergaard', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/16/37455152.png', 'height': 178, 'weight': None, 'date_of_birth': '2002-12-26', 'gender': 'male'}}, {'id': 36207470, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2905, 'type_id': 18, 'section': 'event', 'player_id': 84076, 'related_player_id': 83665, 'player_name': 'Oliver Lund', 'related_player_name': 'Patrick Mortensen', 'result': None, 'info': None, 'addition': None, 'minute': 90, 'extra_minute': 2, 'injured': False, 'on_bench': False, 'coach_id': None, 'sub_type_id': None, 'sort_order': 9, 'player': {'id': 84076, 'sport_id': 1, 'country_id': 320, 'nationality_id': 320, 'city_id': None, 'position_id': 25, 'detailed_position_id': 155, 'type_id': 25, 'common_name': 'O. Lund Poulsen', 'firstname': 'Oliver', 'lastname': 'Lund Poulsen', 'name': 'Oliver Lund Poulsen', 'display_name': 'Oliver Lund', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/12/84076.png', 'height': 188, 'weight': 79, 'date_of_birth': '1990-08-21', 'gender': 'male'}}, {'id': 36207004, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2447, 'type_id': 18, 'section': 'event', 'player_id': 13980925, 'related_player_id': 10310276, 'player_name': 'T. Bech', 'related_player_name': 'Marokhy Ndione\xa0', 'result': None, 'info': None, 'addition': None, 'minute': 57, 'extra_minute': None, 'injured': False, 'on_bench': False, 'coach_id': None, 'sub_type_id': None, 'sort_order': 2, 'player': {'id': 13980925, 'sport_id': 1, 'country_id': 320, 'nationality_id': 320, 'city_id': None, 'position_id': 27, 'detailed_position_id': 151, 'type_id': 26, 'common_name': 'T. Kristensen', 'firstname': 'Tobias Bech', 'lastname': 'Kristensen', 'name': 'Tobias Bech Kristensen', 'display_name': 'Tobias Bech', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/29/13980925.png', 'height': 189, 'weight': None, 'date_of_birth': '2002-02-19', 'gender': 'male'}}, {'id': 36206881, 'fixture_id': 18528480, 'period_id': 4208988, 'participant_id': 2447, 'type_id': 18, 'section': 'event', 'player_id': 37341882, 'related_player_id': 30682, 'player_name': 'I. Said', 'related_player_name': 'Justin Lonwijk', 'result': None, 'info': None, 'addition': None, 'minute': 46, 'extra_minute': None, 'injured': False, 'on_bench': False, 'coach_id': None, 'sub_type_id': None, 'sort_order': 1, 'player': {'id': 37341882, 'sport_id': 1, 'country_id': 716, 'nationality_id': 716, 'city_id': 42844, 'position_id': 27, 'detailed_position_id': 156, 'type_id': 26, 'common_name': 'I. Sa’id', 'firstname': 'Ibrahim', 'lastname': 'Sa’id', 'name': 'Ibrahim Sa’id', 'display_name': 'Ibrahim Said', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/26/37341882.png', 'height': 172, 'weight': None, 'date_of_birth': '2002-06-15', 'gender': 'male'}}, {'id': 36206444, 'fixture_id': 18528480, 'period_id': 4208948, 'participant_id': 2905, 'type_id': 14, 'section': 'event', 'player_id': 151709, 'related_player_id': None, 'player_name': 'Sigurd Haugen', 'related_player_name': None, 'result': '1-0', 'info': 'Shot', 'addition': '1st Goal', 'minute': 9, 'extra_minute': None, 'injured': None, 'on_bench': False, 'coach_id': None, 'sub_type_id': None, 'sort_order': 1, 'player': {'id': 151709, 'sport_id': 1, 'country_id': 1578, 'nationality_id': 1578, 'city_id': 36266, 'position_id': 27, 'detailed_position_id': 151, 'type_id': 27, 'common_name': 'S. Haugen', 'firstname': 'Sigurd Hauso', 'lastname': 'Haugen', 'name': 'Sigurd Hauso Haugen', 'display_name': 'S. Haugen', 'image_path': 'https://cdn.sportmonks.com/images/soccer/players/29/151709.png', 'height': 187, 'weight': None, 'date_of_birth': '1997-07-17', 'gender': 'male'}}
```

The API backend is generic, so the same code can be used for other sports by changing the sport parameter in the client object.

```python
from sportmonks_py import APIClient

client = APIClient(sport="cricket", api_token=f"{SPORTMONKS_API_TOKEN}")

fixture_id = [1000]
response = client.fixtures.get_fixtures(
        fixture_ids=fixture_id
    )

for page in response:
    print(page)
```

Asynhronous support is also included and being improved upon, as can be seen in the example below.

```python
from sportmonks_py import APIClient

client = APIClient(sport="football", api_token=f"{SPORTMONKS_API_TOKEN}")
async for page in  client.teams.get_teams(team_id=100, async_mode=True):
    print(page)

```

Output
```doctest
{'id': 100, 'sport_id': 1, 'country_id': 462, 'venue_id': 1380, 'gender': 'male', 'name': 'Ebbsfleet United', 'short_code': 'EBB', 'image_path': 'https://cdn.sportmonks.com/images/soccer/teams/4/100.png', 'founded': 1946, 'type': 'domestic', 'placeholder': False, 'last_played_at': '2024-12-14 15:00:00'}
```