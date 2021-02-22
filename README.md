# versioncontrolbot

> BEEP BOP BOOP 🤖

My custom Twitch.tv chatbot that I use during my gameplay/programming streams to engage more with the chat. It was built in response to none of the publicly available bots doing exactly what I want, for free, with no strings attached. I just want to talk to my chat and allow them to play sound effects and have a good time.

## Main Features
- A chat-wide currency system. People who engage in chat earn 'gil' over time which they can spend on rewards.
    - Viewers will earn gil for just watching over time.
    - Mods can add gil arbitrarily to viewers with !addgil.
    - !gamble allows Viewers to gamble their gil for more gil.
- The ability for viewers to select and play sound effects, using currency or not, on stream. As long as the stream is capturing desktop sound they will be played back. !sfx is the command.
- Other cool functionality, and the ability to easily build out further.

## Technology
The bot is written in Python 3.7, built upon the [TwitchIO library](https://github.com/TwitchIO/TwitchIO) and utilises an asychronous event system to stay up to date with even a fast flowing chat.

## Getting Started for Developers
Clone the repo, create the environment and generate the required .env file in the root folder.

This .env file should include the following data:

| Name | Description | Example |
| ---- | ------| ------- | 
|TMI_TOKEN | The TMI token you receive from the Twitch developer page  | TMI_TOKEN=oauth:XXXX | 
| CLIENT_ID | The Client ID you receive from the Twitch developer page | |
| CLIENT_SECRET | The Client Secret you receive from the Twitch developer page | |
| BOT_NICK  | The nickname of the bot's Twitch account  | BOT_NICK=versioncontrolbot |
| BOT_PREFIX | The string you want to use as a prefix to bot commands | BOT_PREFIX=! |
| CHANNEL | The name of the channel you want the bot to join | CHANNEL=version_control |
| HELP_STR | The message you want to appear when users type !help | HELP_STR="This is a help message" |
| SFX_HELP_STR | The message you want to appear when the users type !sfxlist | SFX_HELP_STR="This is an SFXList message" |

## License
You are free to clone or fork this repo and make your own bots based on using it as a framework. If you do this, please retain the credit to me in the source code. 
<a href="https://twitch.tv/version_control" target="_blank">Also a follow on Twitch would go a long way <3</a>