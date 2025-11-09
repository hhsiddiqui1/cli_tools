# GitHub Setup Instructions

To upload your project files to GitHub for tracking, with the repository rooted at the `/mnt/c/Users/hhsid/cli_root` level, follow these steps:

### 1. Navigate to the Root Directory
First, change to the directory where you want to create the repository.
```bash
cd /mnt/c/Users/hhsid/cli_root
```

### 2. Initialize a Git Repository
This command creates a new, empty Git repository in the current directory.
```bash
git init
```

### 3. Add Your Project Files
This command stages the entire `monoova_integration` directory for the first commit.
```bash
git add monoova_integration/
```

### 4. Commit Your Files
This saves your staged changes to the local repository's history.
```bash
git commit -m "Initial commit: Add Monoova integration planning documents"
```

### 5. Create a Repository on GitHub
Go to [GitHub.com](https://github.com) and create a new, empty repository. **Do not** initialize it with a README, .gitignore, or license file, as you already have a local repository. GitHub will provide you with a URL for your new repository (e.g., `https://github.com/your-username/your-repo-name.git`).

### 6. Link Your Local Repository to GitHub
This command connects your local repository to the remote one on GitHub. Replace the URL with the one you got from GitHub.
```bash
git remote add origin https://github.com/your-username/your-repo-name.git
```

### 7. Push Your Code to GitHub
This command uploads your committed changes to GitHub.
```bash
git push -u origin master
```
(Note: Your default branch might be `main` instead of `master`. Use `git push -u origin main` if that's the case.)

After completing these steps, your files will be uploaded and tracked on GitHub.
