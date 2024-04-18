# Discord SnailMail Bot

This Discord bot simulates the act of sending and receiving letters as if you were sending physical mail using a postal service.

## Features

Users can register with the bot to enable sending and receiving letters to others.

Users can write and send letters to other users, and those letters will be delivered after a certain amount of time has passed (typically days) to simulate the real-world transit of mail.

The receiving user can check their mailbox and read any letter that was delivered to them.

## Commands

```/register``` - Register to start sending and receiving letters.

```/mailbox``` - Check your mailbox for new mail.

```/read [user]``` - Read the oldest unread letter from a user.

```/send [recipient] [message] ``` - Send a letter to someone.

## Examples

### Registering:
![Alice registers](demo/register.gif)

### Sending A Letter:
![Alice sends a letter to Bob](demo/send.gif)

### Checking Mailbox / Reading Letters:
![Bob checks the mailbox and reads the letter from Alice](demo/mailboxread.gif)
