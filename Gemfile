source "https://rubygems.org"

# Jekyll 4 — built by GitHub Actions, not the GitHub Pages native builder,
# so we are not restricted to github-pages gem versions.
gem "jekyll", "~> 4.3"

# Required for Ruby 3+ (WEBrick was removed from stdlib).
gem "webrick", "~> 1.8"

group :jekyll_plugins do
  gem "jekyll-remote-theme", "~> 0.4"   # fetches al-folio at build time
  gem "jekyll-feed",         "~> 0.17"
  gem "jekyll-sitemap",      "~> 1.4"
end
