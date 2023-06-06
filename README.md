# Cyber Pizza
#### Video Demo:  [YouTube](https://youtu.be/2uCDMSgdFyw)
#### Description:

Hi, my name is Anatoliy, and this is my final project for CS50.

[Here you can see how I did "map" for my final project.](https://imgur.com/a/aeWUO3W)

At first I had plan to create simple website where you can sign up, log in and do something more
with database. But I had no idea what my site can be and what it will do.

I saw random YT video about AI, and was kinda inpired by that. I went to MiddleJourney Discord channel, and
generated some pictures. Those were pretty random, but one of them was that guy with pizza from home page of my site.

And here is how the idea came to my head. Then I was thinking about how would I implement this. And since I want to
complete CS50 web programmign course, I thought that it would be better, if I will not lear something new for now, and just try to build my own app on Flask. I use jinja loops for my item cards, so it doesn't matter how much items you want to show on page. And also I tried to make variebles everywhere, where some code would be changed more than in one place. 

My app has multiple templates for Log in/Sign up, for order and for cart/empty cart. I did not use any css libraries, because I think for this project, for me it was easier to write styles by myself.

Also my app has pizza.db, that contains all data about users and their carts. I chose to create unic id for every user, and unic hash for every cart for every uer's session for every user. And I spent couple hours on optimizing form, so there will not be two users with one email, or if user will try to change html values of forms, it will be rejected. 

I learned some new things during this project, but the hardest was to make my db work with python, for some reason. I though that it would be easy as in cs50 finance, but in reality it was a little bit harder. Or maybe I just did not find the right way. 

Basically, this project does not have any value, and does not make user's life easier, but the main purpose was to make this look nice and make some functionality. 

I had experience in creating html and css landing pages, so it wasn't too hard for me. But it was really interesting to see how my website becomes interactive. Actually I had more ideas which I wanted to implement, but it is tremendous hard in my country right now. Because of every day russians missles flying and destroying our electricity infrastructure.

I don't know if it's normal that cs50 took me that much time (almost 3 month), but I hope that next course will be a lot faster. And I would've recomend cs50 to my friends, but none of them understand english at sufficient level. But my english, I think, not as good as I want it to be also.

I want to thank the team of CS50, I was amazed of how scale of this course. The lectures and shorts are amazing. There is a feeling like after watching a good TV series, you want to go down this road again. 

Technologies that I used:
1. HTML
2. CSS
3. SQLite3
4. Flask
5. Design in figma
6. Characters by MiddleJourney AI

Here's my thoughts in proccess:

So for now I want to make a simple site for ordering pizza. I want all pictures to be AI generated, or from stock images sites. So plan is:

- create a hero section of web-site, that contain the name and some text with pizza image

- creating some easy form for registering user by taking their
• e-mail
• password (store it as hash)
Then redirect user to next page that:

- ONLY IF USER HAD LOGED IN create a section where user can choose the pizza he/she want and choose some options for pizza and then redirect user to the next page where:

- user set the point in Google maps and it is where pizza should be "delivered", and after that user receives e-mail with confirmation 

At this moment I'm planning to make simple front end with HTML and vanilla CSS, maybe I'll need some JS for cart, but I don’t know how to Implement this for now. And what to use Flask for back end (not sure if flask is bad end, but I mean the interactive part of site). Because I don't have much time left, and I already know the basics of Flask. And have general idea of how to implement this.

So I kinda figured out how to use SQLite with flask, using their documentation. For today I want to create functionality without full html and css, just forms and buttons

So my todo list:
- make sql request for registration
- I understood that I don't have login page, so I should create one, it will be like sign up, but without name
- make possible for user to register and log in

Todo list for tomorrow:
- implement hashing password instead of using actual text
- figure out how to implement cart
- figure out how to track all user’s orders and show his/her history