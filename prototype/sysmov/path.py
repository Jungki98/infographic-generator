import sys
import os

def create_path():
    # 'create' 디렉토리를 sys.path에 추가
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    create_dir = os.path.join(parent_dir, 'create')
    if create_dir not in sys.path:
        sys.path.append(create_dir)
