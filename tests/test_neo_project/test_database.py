
from udacity.neo_project import main

def test_db_g_exists_w_open_t_contents():
    db = main.main2()
    
    assert db