# Movieflix
## Creators
1. [Paritosh Panda](https://github.com/Tashi21)
2. [Adit Dhawan](https://github.com/aditd)
3. [Shriman Visahan](https://github.com/Shriman02)

## About the Project
### Tech Stack
1. [Django Framework](https://www.djangoproject.com/)
2. [Python](https://www.python.org/)
3. [Bootstrap v5](https://getbootstrap.com/)
4. [SQlLite](https://www.sqlite.org)

### Local Setup
You should have Python 3.9 installed on your system. You can get the latest version from [here](https://www.python.org/downloads/). You should also have [pipenv](https://pypi.org/project/pipenv/), a virtual environment manager for Python. It will ensure that you download the required dependencies in a virtual environment and not globally.

```
pip install --user pipenv
```

Here is how you can set up the entire project on your system from the command line:

```
git clone https://github.com/Tashi21/Movieflix.git
cd movieflix
pipenv install
pipenv shell
python manage.py runserver
```

### Overview
This is a simple e-commerce website made for our Advanced Programming course, taught by Professor Anirban Mondal, in our 3rd semester at Ashoka. The backend for the website was developed by Adit and Paritosh, and the frontend by Shriman and Paritosh.

We divided the work by breaking the website down into the required pages and each person took up the task for the backend and frontend both for the page they were assigned. This proved to be difficult as some pages required other pages to have been set up first. This caused confusion and delays, which is why we switched to a backend-frontend basis of division. This helped our workflow and sped up the development process.

Paritosh finally compiled all the code together and linked the backend to the frontend.

To create our dummy database, Adit wrote a python script that webscraped IMDb and got a list of movies, their genres, actors, directors, runtime, rating, release year, and summary.

### From Paritosh
I faced many challenges while making this website. The biggest was figuring out the user registration flow. I used a Django app called [django-allauth](https://django-allauth.readthedocs.io/en/latest/) to allow me to sign in users using Google OAuth 2.0. It made it simple to link the Google OAuth API to my project but the app had its own set of user registration flows that it forced me to use. When clicking the link to sign up with google, it first takes the user to a confirmation page and then to the Google page where the user logs in. After numerous tries I had to settle by designing the frontned for that page and letting it be part of the final website. Many other hiccups this app caused was redirecting users to a confirm email page after signing up, not logging in with Google in certain situations, throwing many errors because the sign up form was not valid for them (but it was for my purposes) and many others. All of this required extensively poring over the documentation of both Django and django-allauth.

This project helped me understand many key aspects of web-development. What workflow works and doesn't, how I should first structure the website and which parts I should start building first. I now understand a little better how form validation works, how to structure my logic to handle this validation and what should be rendered for the user in different situations. Using Bootstrap made it very easy to design a simple but elegant looking front end. But while it makes it easy to make the website look a certain way, when writing the HTML for it, I had to be very careful of how my div tags and other elements were structured because otherwise it would render on top of each other or to the side of the page or sometimes it would not be visible.  

This was my first big project that I created from scratch. It was a lot of effort, all-nighters, scraping StackOverflow, the Django documentation, and Google for ways to solve millions of problems. But at the end of it, I feel more capable as a developer and programmer. I have learnt a lot about this web-development framework and how to code in Python. I realised just how much a programmer needs to scroll through the internet to find ways to solve trivial seeming problems. But that "aha!" moment makes it all worth it when the code works how you want it to. This was one of my most fun and insightful experiences as a programmer. I am excited to improve my skills as a programmer and to tackle all the roadblocks that come with it.

I would like to come back to this project again sometime and host it online on platforms like Heroku. I would also like to clean up and organize the entire codebase. But for now, my final exams are keeping me busy.
