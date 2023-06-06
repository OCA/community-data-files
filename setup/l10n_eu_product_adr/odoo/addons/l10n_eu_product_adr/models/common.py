TRANSPORT_CATEGORIES = [
    ("0", "0"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("-", "-"),
    ("CARRIAGE_PROHIBITED", "CARRIAGE PROHIBITED"),
    ("NOT_SUBJECT_TO_ADR", "Not subject to ADR"),
]


TUNNEL_RESTRICTION_CODES = [
    ("B", "B"),
    ("B1000C", "B1000C"),
    ("B/D", "B/D"),
    ("B/E", "B/E"),
    ("C", "C"),
    ("C5000D", "C5000D"),
    ("C/D", "C/D"),
    ("C/E", "C/E"),
    ("D", "D"),
    ("D/E", "D/E"),
    ("E", "E"),
    ("-", "-"),
    ("CARRIAGE_PROHIBITED", "CARRIAGE PROHIBITED"),
    ("NOT_SUBJECT_TO_ADR", "Not subject to ADR"),
]


category_points_factor_map = {
    "1": 50,
    "2": 3,
    "3": 1,
    "4": 0,
}


un_number_points_factor_map = {
    "0081": 20,
    "0082": 20,
    "0084": 20,
    "0241": 20,
    "0331": 20,
    "0332": 20,
    "0482": 20,
    "1005": 20,
    "1017": 20,
}
