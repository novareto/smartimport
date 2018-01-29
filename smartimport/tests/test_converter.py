from smartimport.converter import as_dict

def test_converter():
    result = as_dict('<xml version="1.0"> <dale> <vorname> Christian </vorname> <nachname> Ferdinand </nachname> </dale></xml>')
    assert 'vorname' in result.keys()
    assert 'Christian' == result['vorname']
    assert 'Ferdinand' == result['nachname']