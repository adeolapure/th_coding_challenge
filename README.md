# divvydose-git-profile


## What's This?

A solution for the DivvyDose coding challenge


## Installation


### Using Pipenv

```bash
$pipenv install
```


### Using Plain Pip

_Note: I usually would not include a `requirements.txt` file along with Pipenv files, but I'm not sure what tools are
standard at DivvyDose._

```bash
$ python3.6 -m venv /path/to/venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```


## Usage

This application provides functionality which can either be executed via an HTTP API or a CLI program. 


### API Usage


#### Starting the Server

In your virtual environment, use the binary provided by Flask to run a development server:

```bash
$ FLASK_APP=api.api flask run
```

Note the API base url (by default, http://127.0.0.1:5000) which will be printed when you start the development server.


#### Making Requests

A single endpoint is provided by this API: `<BASE URL>/v1/git-metrics`. When making requests to this endpoint,
you can include the following querystring parameters, all of which are optional:

- `github_usernames`: One or more valid GitHub profile usernames to include in the aggregated metrics response.
Multiple values should be separated with a comma by default.
-  `bitbucket_usernames`: One or more valid Bitbucket profile usernames to include in the aggregated metrics response.
Multiple values should be separated with a comma by default.
- `username_delimiter`: A character by which multiple provided GitHub and Bitbucket usernames will be delimited.
By default, the API expects comma-separated values, but you can use this parameter to override the behavior.
Note that if you are only aggregating (up to) one GitHub and Bitbucket profile each, setting this parameter has no 
effect.


##### Examples

**Note:** You must replace the `<values>` in the below examples with appropriate real-world examples in order for them
to run successfully! 

- Get metrics for a single GitHub user:
    ```bash
    $ curl <base url>/v1/git-metrics?github_usernames=<MyUsername> -v
    ``` 
- Get aggregated metrics for a single GitHub user and a single Bitbucket user:
    ```bash
    $ curl <base url>/v1/git-metrics?github_usernames=<MyUsername>&bitbucket_usernames=<MyOtherUsername> -v
    ```
- Get aggregated metrics for two GitHub users and a single Bitbucket user:
    ```bash
    $ curl <base url>/v1/git-metrics?github_usernames=<OldUsername>,<NewUsername>&bitbucket_usernames=<BbUsername> -v
    ```


### CLI Usage

In your virtual environment, invoke the command-line interface via the `app.cli` module.


#### Examples

- Show usage details:
    ```bash
    $ python -m app.cli --help
    ```
- Get metrics for a single GitHub user:
    ```bash
    $ python -m app.cli --github-username MyUsername 
    ``` 
- Get aggregated metrics for a single GitHub user and a single Bitbucket user:
    ```bash
    $ python -m app.cli --github-username MyUsername --bitbucket-username MyOtherUsername
    ```
- Get aggregated metrics for two GitHub users and a single Bitbucket user:
    ```bash
    $ python -m app.cli -g OldUsername -g NewUsername -b BbUsername
    ```


## Testing


### Install Test Requirements


#### Using Pipenv

```bash
$ pipenv install --dev
```


#### Using Plain Pip

```bash
$ python3.6 -m venv /path/to/venv
$ . venv/bin/activate
$ pip install -r requirements-dev.txt
```


### Run the Tests

In your virtual environment, simply run the following command:

```bash
$ python -m unittest discover
```


## Next Steps

Given more time, I would make the following changes/improvements to the service in the following areas:


### Testing

- More unit test coverage, generally
- Integration tests using the tools provided by the Flask framework in `tests/app/test_api.py`


### Documentation

- Add a Swagger/OpenAPI specification file
- Add Sphinx boilerplate to generate a static documentation site


### GraphQL

GitHub provides a GraphQL API, which would be much more appropriate for fulfilling this service's use-case than the
REST API which is currently being used. Specifically, the GraphQL API is for optimizing what currently requires
many verbose RESTful API calls by providing an option to make fewer, more targeted requests which specify exactly
which fields should be included in the response. In particular, optimized performance would be apparent when retrieving
metrics for GitHub profiles associated with large numbers of repositories and would bottleneck request time around
the number of profiles being retrieved rather than the size of each given profile.


### Missing Features

Notably, the following features are missing from this service:

- **Total number of commits to all repositories in a generated report.** This was excluded due to concerns related
to performance and API rate limits. If the GraphQL API was leveraged ([see above](#graphql)), it would go a long way
to making this metric more reasonable to incorporate.
- **Total size of multiple Git service accounts.** I'm not entirely sure what this metric should represent- number of
bytes? files? lines of code? In a real-world scenario, this would be a detail that I would clarify with stakeholders
and better understand the desire for this information.
