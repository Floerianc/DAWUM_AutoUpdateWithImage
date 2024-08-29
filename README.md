!! This is a program that uses the DAWUM.de API !!

The main function of this program is to give you automatic updates on the german elections with the most recent official surveys.
As you can see in the code, it uses a Discord webhook to send them to you via Discord.
You can of course change the webhook's URL (Line 93) to your own if you'd like to be updated on the german elections.

I personally use it on my RaspBerry Pi, which is a mini-computer that is 24/7 online and therefore always updates me perfectly on time.
However, you might have to check the code and change a few things to your likings because the program currently only runs between
8am and 11:59pm. You can change the time in the while loop, you'll find it. ^^

The mrs_key.key file always saves the ID of the most recent survey to compare

Here's a image which shows you what the embedded message in Discord could look like:
![Preview](https://github.com/Floerianc/Files/blob/main/image.png?raw=true)