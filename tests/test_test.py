import pytest 
from overwatch import HTTP

def this():
	return 1

def test_this():
	tmp = 1 
	assert this()==1
