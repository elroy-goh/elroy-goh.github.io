## Quantitative Research Dossier Website

This repository contains the source code for a personal quantitative research website built with [Jekyll](https://jekyllrb.com) and the **al‑folio** theme. The goal of the site is to present three deep research memos, a research engineering primer, a statement of research hygiene, a CV and contact information. It follows the strategy and sitemap recommended in the accompanying research brief.

### Local development

The site uses GitHub Pages–compatible dependencies. To build the site locally you need Ruby and Bundler installed. Alternatively you can use Docker to avoid installing Ruby on your host.

#### Using Bundler

```bash
# install dependencies
bundle install

# serve the site on http://localhost:4000/
bundle exec jekyll serve
```

This command watches for file changes and rebuilds automatically. When ready for deployment, run:

```bash
bundle exec jekyll build
```

The generated static site will be output to the `_site` directory.

#### Using Docker

If you prefer an isolated environment, you can run Jekyll inside a container. The following command mounts your working directory into the container and serves the site at port 4000:

```bash
docker run --rm -it -p 4000:4000 -v $(pwd):/srv/jekyll jekyll/jekyll:4 jekyll serve --watch --drafts
```

### Deployment

This repository is designed to be hosted on **GitHub Pages** using a GitHub Actions workflow. To deploy the site:

1. Create a public repository named `<username>.github.io` where `<username>` is your GitHub handle.
2. Commit and push the contents of this folder to the `main` branch of your new repository.
3. Enable GitHub Actions for the repository (Settings → Actions).
4. Create a workflow file at `.github/workflows/deploy.yml` similar to the following:

   ```yaml
   name: Deploy site
   on:
     push:
       branches: [ main ]
   jobs:
     build-and-deploy:
       runs-on: ubuntu-latest
       steps:
         - name: Check out source
           uses: actions/checkout@v3
         - name: Set up Ruby
           uses: ruby/setup-ruby@v1
           with:
             ruby-version: '3.1'
         - name: Install dependencies
           run: |
             gem install bundler
             bundle install --jobs 4 --retry 3
         - name: Build site
           run: bundle exec jekyll build
         - name: Deploy to GitHub Pages
           uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./_site
   ```

5. Push the workflow file to the repository. The action will run on each commit to `main`, build the site and publish it to the `gh-pages` branch using a built‑in token. Finally, set your repository’s **Pages** source to the `gh-pages` branch in the repository settings.

Once the workflow completes successfully, your site will be available at `https://<username>.github.io`.

### Customisation

Edit `_config.yml` to update your name, email and other metadata. Page content lives in `_pages/` and research memos live in `_projects/`. Static assets such as PDFs and images live under the `assets/` directory. Replace the placeholder text and images with your own work.

### License

This template is provided as a starting point for building a professional quant research profile. You are free to use and adapt it for your own personal site.