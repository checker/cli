# Multi-Site Username Availability Checker

### About
This is a script I made a while back to check the availability of OG words as handles on the various social media platforms. For the most part, it works with any site that has web-based profile pages.

### TODO
- Proxy support
- Multi-threading support
- Windows and Mac executable binary
- Full GUI Application

### Known Supported Services
- Minecraft
- Twitter (IMPROVED in 1.4)
- Instagram* (IMPROVED in 1.4, sometimes doesn't work still)
- Steam ID URLs
- Steam Group URLs
- Mixer (formerly Beam.pro)
- Soundcloud
- Github
- About.me

### Known Unsupported Services
- Snapchat
- Kik

### Comptability
Version `1.4` is only compatible with Python 3+
Verion `1.0-1.3` is compatible with Python 2 & 3

### Installation

1. Download the zip or clone the repo with Git on your local machine.

2. Make sure Python and PIP are installed.

3. Install the dependencies using the following command

    ```
    pip3 install configparser requests termcolor bs4
    ```

4. Edit the `config.ini` with the appropriate values for the site you want to check.

5. Run the script via command line using the following command

    ```
    python3 UsernameChecker.py
    ```

    You can optionally supply some additional command-line arguments for faster use.
    ```
    python3 UsernameChecker.py -l {list filename} -o {output filename} {site number}
    ```
    Example:
    ```
    python3 UsernameChecker.py -l word_lists/HOT-WORDS -o output.txt 2
    ```


### Contributing 
As this is just a personal side project, I only work on it when I have time, so I would love your help to make improvements! Just make a pull request and I'll review the changes as soon as I can. 

If you are not a developer, you can also help me greatly by opening issues with bugs you encounter while running the script.

If you would like to see further improvements and updates for free, please consider donating a few dollars as it really helps me to set aside time out of my busy schedule to work on improving the script. All contributions are great appreciated! 🙂

[PayPal](https://paypal.me/croc)

[Square Cash](https://cash.me/$croc)



