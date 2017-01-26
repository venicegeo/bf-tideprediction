import bftideprediction.data.to_db_fhd as to_db_fhd
import os

def test_to_db_fhd():
    test_file = '/home/barnabas/Documents/work/ATO/edits/bf-tideprediction/test/fixtures/fdh_test.sqlite'
    if os.path.exists(test_file):
        os.remove(test_file)
    to_db_fhd.to_db_fhd(test_file, 'test/fixtures')
    assert os.path.exists(test_file)


def test_to_db_fhd_except():
    test_file = 'test/fixtures/fdh_test.sqlite'
    if os.path.exists(test_file):
        os.remove(test_file)
    to_db_fhd.to_db_fhd(test_file, 'NOTREAL/NOTREAL/POSSIBLYREAL')
    if os.path.exists(test_file):
        os.remove(test_file)


