# LPS - Last Price Saver

Gets specified quote prices every second & saves it to a mysql database.

I can't find 'free' reliable data like this online... So I wrote this containerized app to begin collecting data for me.

## Usage

### Configuration

Rename `.env.example` to `.env` or duplicate the file with the name `.env`...

Register for a TDAmeritrade Developer account & create a new application from their site [here](https://developer.tdameritrade.com/). Then paste in your Application API Key & Redirect URI into the `.env` file.

Also write in whichever stocks you want to keep track of - comma delimited in the `.env` file as-well.

### Authentication

Prior to deploying this application to a headless server, you need to run the authentication script locally. The authentication script uses [Selenium](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiihffnwPHtAhWqp1kKHVTuDgkQFjAAegQIARAC&url=https%3A%2F%2Fwww.selenium.dev%2F&usg=AOvVaw38IyEsg2ARkRX6lSh_KzqM) webdriver & expects Chrome to be installed on your machine... You can modify the script yourself to use Firefox, or whichever browser you prefer (I don't think newer versions of Safari support it)...

```bash
make auth
```

### Deployment

After successfully running the authentication script above, you can either clone this repo to your server & copy over the generate secrets/token.json file; or copy the local version of this repo that already has the token.json file...

### Building

Just incase you already have an older built version, throw the clean on there.

```bash
make clean && make build
```

### Running

After building, you can run the application simply with:

```bash
make run
```

### Exporting

Want to export the data to .CSV format? There's already a small script here that lets you do that by ticker & date (daily).
You'll be prompted for that information after running the below:

```bash
make csv
```

### Metrics

WIP.
