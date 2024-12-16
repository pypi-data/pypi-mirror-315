# ~/thisgoeshardasfuck/tests/test_thisgoeshardasfuck.py
import pytest
import thisgoeshardasfuck

def test_thisgoeshardasfuck():
    try:
        thisgoeshardasfuck()
        assert True
    except Exception as e:
        assert False, f"this does not go hard as fuck: {str(e)}"
