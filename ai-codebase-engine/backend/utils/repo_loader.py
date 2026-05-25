import os
import git
import zipfile
import shutil
from pathlib import Path

class RepoLoader:
    """Handles repository loading from various sources."""
    
    def __init__(self, data_dir: str = "data/repos"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _rmtree(self, path: Path):
        import stat
        def remove_readonly(func, path, _):
            import os
            os.chmod(path, stat.S_IWRITE)
            try:
                func(path)
            except Exception:
                pass
        if path.exists():
            shutil.rmtree(path, onerror=remove_readonly)
    
    def load_from_github(self, repo_url: str, repo_id: str) -> Path:
        """Clone GitHub repository."""
        repo_path = self.data_dir / repo_id
        
        self._rmtree(repo_path)
        
        try:
            git.Repo.clone_from(repo_url, repo_path, depth=1)
            self._cleanup_git_folder(repo_path)
            return repo_path
        except Exception as e:
            raise Exception(f"Failed to clone repository: {str(e)}")
    
    def load_from_zip(self, zip_path: str, repo_id: str) -> Path:
        """Extract ZIP file."""
        repo_path = self.data_dir / repo_id
        
        self._rmtree(repo_path)
        
        repo_path.mkdir(parents=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            self._safe_extract(zip_ref, repo_path)
        
        # Handle nested folders (common in GitHub ZIPs)
        subdirs = [d for d in repo_path.iterdir() if d.is_dir()]
        if len(subdirs) == 1:
            for item in subdirs[0].iterdir():
                shutil.move(str(item), str(repo_path))
            self._rmtree(subdirs[0])
        
        return repo_path

    def _safe_extract(self, zip_ref: zipfile.ZipFile, destination: Path):
        """Extract ZIP members without allowing path traversal outside destination."""
        destination = destination.resolve()

        for member in zip_ref.infolist():
            member_path = (destination / member.filename).resolve()
            try:
                member_path.relative_to(destination)
            except ValueError:
                raise ValueError(f"Unsafe path in zip archive: {member.filename}")

        zip_ref.extractall(destination)
    
    def load_from_local(self, local_path: str, repo_id: str) -> Path:
        """Copy local folder."""
        repo_path = self.data_dir / repo_id
        
        self._rmtree(repo_path)
        
        shutil.copytree(local_path, repo_path, 
                       ignore=shutil.ignore_patterns('.git', '__pycache__', 
                                                     'node_modules', 'venv'))
        return repo_path
    
    def _cleanup_git_folder(self, repo_path: Path):
        """Remove .git folder to save space."""
        import stat
        def remove_readonly(func, path, _):
            import os
            os.chmod(path, stat.S_IWRITE)
            try:
                func(path)
            except Exception:
                pass

        git_folder = repo_path / ".git"
        if git_folder.exists():
            shutil.rmtree(git_folder, onerror=remove_readonly)
    
    def get_file_structure(self, repo_path: Path) -> dict:
        """Generate file tree structure."""
        def build_tree(path: Path, prefix: str = "") -> dict:
            tree = {"name": path.name, "path": str(path), "children": []}
            
            if path.is_file():
                tree["type"] = "file"
                tree["size"] = path.stat().st_size
                return tree
            
            tree["type"] = "directory"
            
            try:
                for item in sorted(path.iterdir()):
                    if item.name.startswith('.'):
                        continue
                    if item.name in ['node_modules', '__pycache__', 'venv', '.git']:
                        continue
                    tree["children"].append(build_tree(item, prefix + "  "))
            except PermissionError:
                pass
            
            return tree
        
        return build_tree(repo_path)
