import sys
import os
# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.school_api.client import JwxtClient

def test_client_initialization():
    client = JwxtClient()
    assert client is not None