**IN THE TERMINAL:**
1. git add . + ENTER
2. git commit -m "insert message here" + ENTER
3. git push + ENTER

**HOW TO GET AWS CREDENTIALS**
1. Click on AWS logo on the left tab
2. Double click on the key (profile)
3. Select profile:makaning
4. It will automatically open the aws console on a browser; log in with credentials

**WHEN PUSHING TO PROD:**
1. Ensure you change the bot token to the prod environment token (bottom of makanbot.py)
2. Ensure you change client from Window Client to AWS Client (top of makanbot.py AND GetRestaurant.py)