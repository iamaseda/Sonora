pipenv
python3
Flask
requests
js2py
pip install Flask-SQLAlchemy psycopg2-binary
Host common css and js files in Flask for development. Once traffic begins to impact server performance in production, or to prevent it, host common css and js files in React app.
To start postgresql@14 now and restart at login:
  brew services start postgresql@14
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/postgresql@14/bin/postgres -D /opt/homebrew/var/postgresql@14
==> node@16
node@16 is keg-only, which means it was not symlinked into /opt/homebrew,
because this is an alternate version of another formula.

If you need to have node@16 first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/node@16/bin:$PATH"' >> ~/.zshrc

For compilers to find node@16 you may need to set:
  export LDFLAGS="-L/opt/homebrew/opt/node@16/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/node@16/include"

brew services start postgresql
brew services stop postgresql
