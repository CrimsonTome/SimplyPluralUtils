# SimplyPluralUtils

> Utilities for working with the Simply Plural API with Python

## System requirements

- Python 3.8 or higher is required to run the tools (tested with 3.13). You can check your Python version by running `python --version` in your terminal. You can install it using your package manager or from the [Python website](https://www.python.org/downloads/). 
- Both Windows 10 and Linux have been tested.
  - MacOS should work as well but has not been tested. 
- It is recommended to use [uv](https://docs.astral.sh/uv/)

## Getting started

Clone the repository and navigate to the project directory.
```
git clone https://git.crimsontome.com/crimsontome/SimplyPluralUtils.git
cd SimplyPluralUtils
```
In order to get data from Simply Plural you will need to rename the `secrets.example.json` file to `secrets.json` and add your Simply Plural API key. You can find your API key by going into settings -> Account -> Tokens -> Add Token. Give it read access and copy the token into the file. 

```json
{
    "SimplyPluralAPIKey": "your_api_key_here"
}
```

Run `uv sync` to install the dependencies. You will need to make your own tests file to call the code from (sample tests may be added later)

## License

SimplyPluralUtils is licensed under the MIT license. The full license text is included in the [LICENSE](LICENSE) file in this repository. Tldr legal have a [great summary](https://www.tldrlegal.com/license/mit-license) of the license if you're interested.