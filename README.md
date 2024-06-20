# Blogging Application

This project is a simple blogging application built with a Django backend and a plain HTML/CSS/JavaScript frontend. It aims to test capabilities in Django, database querying, and basic frontend development.

## Part 1: Backend Development

### Models

- **User**: Use Django's built-in User model.
- **Post**:
  - `title`: CharField
  - `content`: TextField
  - `author`: ForeignKey to User
  - `created_at`: DateTimeField
  - `updated_at`: DateTimeField
- **Comment**:
  - `post`: ForeignKey to Post
  - `author`: ForeignKey to User
  - `content`: TextField
  - `created_at`: DateTimeField

### API Endpoints

#### Auth
- **User Registration**: Endpoint to create a new user.
- **Authentication**: Use Django Rest Framework's token authentication.
#### Posts
- **Create Post**: Authenticated users can create a post.
- **List Posts**: List all posts.
- **Most Commented Posts**: An endpoint that returns the top 5 most commented blog posts.
- **Retrieve Post**: Get details of a specific post.
- **Update Post**: Authenticated users can update their own posts.
- **Delete Post**: Authenticated users can delete their own posts.
#### Comments 
- **Create Comment**: Authenticated users can comment on a post.
- **List Comments**: List all comments for a specific post.
- **Retrieve Comment**: Get details of a specific comment.
- **Update Comment**: Authenticated users can update their own comments.
- **Delete Comment**: Authenticated users can delete their own comments.

### Validation

- Ensure users cannot edit or delete posts or comments they do not own.
- Ensure all fields are properly validated (e.g., title should not be empty, content should not be too short).

### Testing

- I'm write unit tests for the models and views.

### Documentation

- Include a `README.md` with instructions on setting up and running the project.
- API documentatiin Postman [Postman Collection](./.postman.json).

## Part 2: Frontend Development

### Pages

- **Home Page**: Display a list of all blog posts with titles and excerpts.
- **Most Commented Posts Page**: Display the top 5 most commented posts.
- **Post Detail Page**: Display the full content of a single post, along with its comments.
- **Login/Register Page**: Allow users to register and log in.
- **Create/Edit Post Page**: Form to create a new post or edit an existing one.

### Functionality

- **User Authentication**: Allow users to log in and register. Use tokens for authenticated API requests.
- **Create/Edit/Delete Posts**: Allow authenticated users to create, edit, and delete their posts.
- **Create/Edit/Delete Comments**: Allow authenticated users to comment on posts and manage their comments.

### Technologies

- Use plain HTML, CSS, and JavaScript (I'm use Vue.js to simplify implementation).

## Setup Instructions (for unix kernel)

1. **Clone the repository**:
    ```bash
    git clone git@github.com:yaacovdev/blog_app.git
    cd blog_app
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```

4. **Apply migrations**:
    ```bash
    python backend/manage.py migrate
    ```

5. **Run the development server**:
    ```bash
    python backend/manage.py runserver
    ```

6. **Frontend**:
    - Open `frontend/index.html` in a web browser to view the frontend.

## Running Tests

To run the tests, execute:
```bash
python backend/manage.py test
```
