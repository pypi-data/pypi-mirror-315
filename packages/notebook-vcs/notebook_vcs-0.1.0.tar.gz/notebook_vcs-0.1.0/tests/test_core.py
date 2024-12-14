"""Tests for the core VCS functionality."""
import os
import json
import tempfile
import shutil
from pathlib import Path
import pytest
from notebook_vcs.core import NotebookVCS


@pytest.fixture
def temp_notebook_dir():
    """Create a temporary directory for notebook testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def vcs(temp_notebook_dir):
    """Create a VCS instance for testing."""
    return NotebookVCS(temp_notebook_dir)


def test_init(vcs, temp_notebook_dir):
    """Test VCS initialization."""
    vcs.init()
    
    # Check directory structure
    assert os.path.exists(vcs.repo_dir)
    assert os.path.exists(vcs.objects_dir)
    assert os.path.exists(vcs.refs_dir)
    assert os.path.exists(os.path.join(vcs.repo_dir, "logs"))
    
    # Check index file
    with open(vcs.index_file, "r") as f:
        index = json.load(f)
        assert index["head"] is None
        assert "main" in index["branches"]
        assert index["branches"]["main"] is None


def test_commit(vcs, temp_notebook_dir):
    """Test commit creation."""
    vcs.init()
    
    # Create a test notebook state
    notebook_state = {
        "cells": [
            {
                "id": 1,
                "content": "print('Hello, World!')",
                "output": "Hello, World!"
            }
        ],
        "variables": {"x": 42}
    }
    
    # Create commit
    commit_hash = vcs.commit(notebook_state, "Test commit")
    
    # Verify commit
    assert commit_hash is not None
    
    # Check commit file
    commit_path = os.path.join(vcs.objects_dir, commit_hash)
    assert os.path.exists(commit_path)
    
    with open(commit_path, "r") as f:
        commit = json.load(f)
        assert commit["message"] == "Test commit"
        assert commit["notebook_state"] == notebook_state


def test_get_commit(vcs, temp_notebook_dir):
    """Test retrieving a commit."""
    vcs.init()
    
    # Create test commit
    notebook_state = {"cells": [], "variables": {}}
    commit_hash = vcs.commit(notebook_state, "Test commit")
    
    # Get commit
    commit = vcs.get_commit(commit_hash)
    
    assert commit is not None
    assert commit["message"] == "Test commit"
    assert commit["notebook_state"] == notebook_state


def test_get_history(vcs, temp_notebook_dir):
    """Test commit history retrieval."""
    vcs.init()
    
    # Create test commits
    states = [
        ({"cells": [], "variables": {"x": i}}, f"Commit {i}")
        for i in range(3)
    ]
    
    commit_hashes = []
    for state, message in states:
        commit_hash = vcs.commit(state, message)
        commit_hashes.append(commit_hash)
    
    # Get history
    history = vcs.get_history()
    
    assert len(history) == 3
    assert history[0].hash == commit_hashes[-1]  # Most recent first
    assert history[-1].hash == commit_hashes[0]  # Oldest last


def test_revert(vcs, temp_notebook_dir):
    """Test reverting to a previous commit."""
    vcs.init()
    
    # Create initial commit
    initial_state = {
        "cells": [{"id": 1, "content": "x = 1"}],
        "variables": {"x": 1}
    }
    initial_hash = vcs.commit(initial_state, "Initial commit")
    
    # Create second commit
    second_state = {
        "cells": [{"id": 1, "content": "x = 2"}],
        "variables": {"x": 2}
    }
    vcs.commit(second_state, "Second commit")
    
    # Revert to initial commit
    success = vcs.revert(initial_hash)
    assert success
    
    # Verify HEAD points to initial commit
    assert vcs.get_head_commit() == initial_hash 