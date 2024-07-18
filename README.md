# Sonora
Sonora is an application that leverages Spotify's API to access a Spotify user's liked songs with the goal of sorting the liked songs into playlists by genre.

## <u>Current Progress</u>
Project currently on pause.
* Searching for an appropriate method for accurate music analysis that supports large batch analyses. If you are familiar with a service or algorithm that does this well, such as Cyanite and other such services, please feel free to contact me at bokyere887@gmail.com

## Setting Up the Project

1. Clone the repository.
2. Create a `.env` file in the root directory of the project and add your environment variables. You can use the provided `.env.example` as a template. Please note: **None of these secrets, URLs, URIs, IDs, and tokens are valid, and they should not be used for your project**. There are environment variables for Cyanite in the example template. In the case that Cyanite is sufficient for your purposes, you will have to go to that service to obtain the secret, access token, and to obtain a webhook URL if you do not already have one.

```sh
cp .env.example .env
```

### Setting Up Project Node Dependencies

1. Navigate using `cd` in your terminal to the project's *root directory*.
2. Run `npm install` to install all dependencies listed in the *package.json* file.
  + If you would like to replicate the exact versions in this project using the *package-lock.json* file, run `npm ci`.

### Setting Up Project Python Dependencies

1. Navigate using `cd` in your terminal to the root directory, in which the *venv* file is located.
2. From there, activate the virtual environment:
  + On Windows: .\venv\Scripts\activate
  + On macOS/Linux: source venv/bin/activate
3. Once the virtual environment has been activated,  run `pip install -r requirements.txt`.
4. Congratulations! You can now run the project using  `python app.py`, `python3 app.py`, `flask run`, etc. One of first two should be sufficient.

## Resources and Miscellaneous Info
** **Please disregard the information below!** 🚨

pipenv
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
