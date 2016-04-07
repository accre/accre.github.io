# Jekyll files for GitHub generated website

## OS X

To setup Jekyll on OS X, first install [homebrew](http://brew.sh).

Once [homebrew](http://brew.sh) is installed, install `rbenv`.

```brew install rbenv ruby-build```

Add `eval "$(rbenv init -)"` to your shell profile script, and either reload your shell or run `rbenv init -` directly before proceeding.

Install the latest version of Ruby via rbenv. At the time of this writing that it is version 2.3.0. Once installed, set it as the default Ruby instance.

```
rbenv install 2.3.0
rbenv global 2.3.0
```

Clone this repository and install Jekyll using Ruby Bundler.

```
git clone git@github.com:accre/accre.github.io.git
cd accre.github.io
gem install bundle
rbenv rehash
bundle install
rbenv rehash
```

To view the rendered website locally, run `jekyll serve` from the `accre.github.io` directory and point your web browser to http://localhost:4000.

The site doesn't have to be rendered locally. Creating content, and then committing and pushing that content to GitHub is all that is required. The GitHub Pages system automatically detects the update, and regenerates the site.



