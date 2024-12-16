from nometa.properties.boolean import _to_bool

def test_none_is_false():
    assert _to_bool(None) == False

def test_empty_string_is_false():
    assert _to_bool('') == False and _to_bool("   ") == False

def test_not_is_false():
    assert _to_bool("no") == False and _to_bool(" not") == False and _to_bool("n  ") == False

def test_0_is_false():
    assert _to_bool(0) == False and _to_bool('0') == False \
        and _to_bool(0.001) == False and _to_bool(0.999) == False \
        and _to_bool("0.001") == False and _to_bool("0.999") == False
    
def test_positive_number_is_true():
    """any number >= 1 is True"""
    assert _to_bool(1) == True and _to_bool('1') == True \
        and _to_bool('2.5') == True and _to_bool(73.3) == True