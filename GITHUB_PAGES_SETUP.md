# Setting Up GitHub Pages for Your Dashboard

Follow these steps to deploy your dashboard to GitHub Pages:

## 1. Push the Files to Your Repository

First, add all the files in this repository to your GitHub repository:

```bash
# Add all files
git add .

# Commit the changes
git commit -m "Add GitHub Pages setup"

# Push to GitHub
git push
```

## 2. Configure GitHub Pages

1. Go to your repository on GitHub: https://github.com/Rojlap107/regional-training-dashboard
2. Click on "Settings" tab
3. Scroll down to the "GitHub Pages" section (or click on "Pages" in the left sidebar)
4. Under "Source", select "GitHub Actions"
5. GitHub will automatically use the workflow file at `.github/workflows/static.yml`

## 3. Wait for Deployment

After configuring GitHub Pages, GitHub Actions will automatically deploy your site. You can check the progress by:

1. Going to the "Actions" tab in your repository
2. Looking for the "Deploy Static Dashboard" workflow run
3. Once complete, it will show a green checkmark

## 4. View Your Dashboard

After deployment is complete (usually takes 1-2 minutes), your dashboard will be available at:

```
https://rojlap107.github.io/regional-training-dashboard/
```

## 5. Update Your Dashboard

To update your dashboard:

1. Take a new screenshot of your running dashboard and replace `static/dashboard_preview.png`
2. Commit and push your changes
3. GitHub Actions will automatically redeploy your site

## Troubleshooting

If your site doesn't deploy properly:

1. Check the Actions tab for any error messages
2. Ensure that your repository is public (GitHub Pages is free for public repositories)
3. Verify that the workflow file at `.github/workflows/static.yml` exists and is correctly formatted
4. Make sure the `static` directory contains at least the `index.html` file