# This project is unmantained!
# Aerosmith

Aerosmith is a quick and (extremely) dirty python script for posting strava activities to canvas assignments.

## Installation
1. Get your api keys from strava and canvas

2. Modify the code to point to your class and assignments.

3. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies. [Then add to aws lambda. ](https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/)

4. [Create a role that lets the function access the db.](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_lambda-access-dynamodb.html)

5. Create a table called `Strava`.

6. Set the environment variables.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## Roadmap
This project was a one off. Anyone who wants to use this code as a starter for something more complex or mantain it is welcome to.  
Features necessary to consider it "complete" not just good enough include (but are not limited to):
   * User input
   * Better security
   * OAuth2 flows
   * ~~Good~~ less bad deployment to AWS lambda
   * Multiple users per aws function/db table so users don't have to be technically savvy.
## License
[MIT](https://choosealicense.com/licenses/mit/)